from tools.config import parse_project_cfg
from pathlib import Path


def generate_scr(scr_path: Path, cfg_path: Path):
    cfg = parse_project_cfg(cfg_path)

    project = cfg["PROJECT"]
    top = cfg.get("TOPLEVEL", project)
    target_part = cfg["TARGET_PART"]
    xst_opts = cfg.get("XST_OPTS", "")

    # SCR-Datei vollständig in einer Zeile, wie im Makefile
    scr_parts = [
        "run",
        f"-ifn {project}.prj",
        f"-ofn {project}.ngc",
        "-ifmt mixed",
    ]

    # Optional: Optionen aus XST_OPTS hinzufügen
    if xst_opts.strip():
        scr_parts += xst_opts.strip().split()

    scr_parts += [
        f"-top {top}",
        "-ofmt NGC",
        f"-p {target_part}",
    ]

    scr_line = " ".join(scr_parts).replace("\n", " ").replace("\r", " ")
    scr_path.parent.mkdir(parents=True, exist_ok=True)
    scr_path.write_text(scr_line, encoding="utf-8")
