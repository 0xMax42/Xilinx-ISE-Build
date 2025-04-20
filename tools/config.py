from tools.paths import ROOT, PROJECT_CFG, VHDL_LS_TOML
from pathlib import Path
from typing import Dict, List, Optional
import toml
import re
from typing import Tuple
from tools.defaults import with_defaults

def parse_vhdl_ls_toml(toml_path: Optional[Path] = None) -> Dict[str, List[Path]]:
    if toml_path is None:
        toml_path = VHDL_LS_TOML

    if not toml_path.exists():
        raise FileNotFoundError(f"{toml_path} not found.")

    with open(toml_path, "r", encoding="utf-8") as f:
        raw = toml.load(f)

    libraries = raw.get("libraries", {})
    parsed: Dict[str, List[Path]] = {}

    for libname, content in libraries.items():
        if content.get("is_third_party", False):
            continue
        files = content.get("files", [])
        actual_libname = "work" if libname == "lib" else libname
        parsed[actual_libname] = [Path(f) for f in files]

    return parsed


def parse_project_cfg(cfg_path: Optional[Path] = None) -> Dict[str, str]:
    cfg_path = cfg_path or PROJECT_CFG

    if not cfg_path.exists():
        raise FileNotFoundError(f"{cfg_path} not found.")

    result: Dict[str, str] = {}
    ignored_keys = {"VHDSOURCE", "VSOURCE", "VHDTEST", "VTEST"}

    with cfg_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            # Kommentare und Leerzeilen überspringen
            if not line or line.startswith("#"):
                continue

            if "+=" in line:
                key, value = map(str.strip, line.split("+=", 1))
                if key in ignored_keys:
                    continue
                if key in result:
                    result[key] += f" {value}"
                else:
                    result[key] = value
            elif "=" in line:
                key, value = map(str.strip, line.split("=", 1))
                if key in ignored_keys:
                    continue
                result[key] = value

    return result

def get_vhdl_sources_and_tests() -> Tuple[Dict[str, List[Path]], Dict[str, List[Path]]]:
    cfg = with_defaults(parse_project_cfg())
    test_filter = cfg.get("TEST_FILTER", r"^tests/|_tb\.vhd$")  # Default-Fallback

    try:
        pattern = re.compile(test_filter)
    except re.error as e:
        raise ValueError(f"Invalid TEST_FILTER regex: {e}")

    all_sources = parse_vhdl_ls_toml()

    normal_sources: Dict[str, List[Path]] = {}
    test_sources: Dict[str, List[Path]] = {}

    for lib, files in all_sources.items():
        for file in files:
            # relative Pfade als Strings prüfen
            rel_path = str(file)
            if pattern.search(rel_path):
                test_sources.setdefault(lib, []).append(file)
            else:
                normal_sources.setdefault(lib, []).append(file)

    return normal_sources, test_sources