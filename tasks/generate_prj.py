import os
from tools.config import get_vhdl_sources_and_tests
from tools.paths import REL_FROM_WORKING_TO_ROOT as REL_ROOT, ROOT, WORKING
from pathlib import Path

def generate_prj(prj_path: Path, *_):
    sources, _ = get_vhdl_sources_and_tests()
    prj_path.parent.mkdir(parents=True, exist_ok=True)

    with prj_path.open("w", encoding="utf-8") as f:
        for libname, files in sources.items():
            for file in files:
                rel_path = os.path.relpath(ROOT / file, WORKING)
                f.write(f"vhdl {libname} {rel_path}\n")
