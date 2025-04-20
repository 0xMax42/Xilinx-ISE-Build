import subprocess
from tools.paths import WORKING, REPORTS, PROJECT_CFG
from tools.config import parse_project_cfg
from tools.defaults import with_defaults
from pathlib import Path


def run_xst():
    cfg = with_defaults(parse_project_cfg(PROJECT_CFG))

    project = cfg["PROJECT"]
    scr_file = f"{project}.scr"
    scr_path = WORKING / scr_file
    xilinx_path = Path(cfg["XILINX"])
    xilinx_platform = "lin64"  # TODO: Optional dynamisch machen
    xst_exe = xilinx_path / "bin" / xilinx_platform / "xst"
    common_opts = cfg.get("COMMON_OPTS", "")

    if not xst_exe.exists():
        raise FileNotFoundError(f"xst executable not found at {xst_exe}")

    if not scr_path.exists():
        raise FileNotFoundError(f"SCR file not found: {scr_path}")

    print(f"\n============ Running XST ============\n")
    print(f"> {xst_exe} {common_opts} -ifn {scr_file}\n")

    subprocess.run(
        [str(xst_exe), *common_opts.split(), "-ifn", scr_file],
        cwd=WORKING,
        check=True
    )
