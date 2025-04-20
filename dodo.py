from pathlib import Path
from tasks.generate_prj import generate_prj
from tasks.generate_scr import generate_scr
from tools.config import parse_project_cfg
from tools.defaults import with_defaults
import subprocess
import os
from pathlib import Path

HERE = Path(__file__).parent.resolve()  # Verzeichnis, in dem dodo.py liegt
CFG_PATH = HERE.parent / "project.cfg"
TOML_PATH = HERE.parent / "vhdl_ls.toml"


def _get_project_name(cfg_path: Path) -> str:
    return with_defaults(parse_project_cfg(cfg_path))["PROJECT"]


def task_generate_prj():
    cfg_path = Path(CFG_PATH)
    toml_path = Path(TOML_PATH)
    project = _get_project_name(cfg_path)
    prj_path = Path("working") / f"{project}.prj"

    return {
        "actions": [(generate_prj, [prj_path, cfg_path, toml_path])],
        "file_dep": [cfg_path, toml_path],
        "targets": [prj_path],
        "verbosity": 2,
    }


def task_generate_scr():
    cfg_path = Path(CFG_PATH)
    project = _get_project_name(cfg_path)
    scr_path = Path("working") / f"{project}.scr"

    return {
        "actions": [(generate_scr, [scr_path, cfg_path])],
        "file_dep": [cfg_path],
        "targets": [scr_path],
        "verbosity": 2,
    }


def task_xst():
    """Run XST synthesizer"""
    cfg_path = Path(CFG_PATH)
    cfg = with_defaults(parse_project_cfg(cfg_path))

    build_dir = Path(cfg["BUILD_DIR"])
    project = cfg["PROJECT"]
    scr_file = f"{project}.scr"
    scr_path = build_dir / scr_file
    prj_path = build_dir / f"{project}.prj"
    xilinx_path = Path(cfg["XILINX"])
    xilinx_platform = "lin64"  # TODO: dynamisch ermitteln, falls nötig

    xst_exe = xilinx_path / "bin" / xilinx_platform / "xst"
    common_opts = cfg.get("COMMON_OPTS", "")

    def action():
        print(f"============ Running XST ============")
        print(f"> {xst_exe} {common_opts} -ifn {scr_file}")
        subprocess.run(
            [str(xst_exe), "-ifn", scr_file],
            cwd=build_dir,
            check=True
        )


    return {
        "actions": [action],
        "file_dep": [scr_path, prj_path],  # <== beides!
        "targets": [Path(cfg["REPORT_DIR"]) / f"{project}.SynthesisReport"],
        "verbosity": 2,
        "task_dep": ["generate_scr", "generate_prj"],
    }
