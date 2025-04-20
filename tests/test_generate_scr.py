from pathlib import Path
from tasks.generate_scr import generate_scr


def write_file(path: Path, content: str):
    path.write_text(content.strip(), encoding="utf-8")


def test_generate_scr_basic(tmp_path):
    cfg_path = tmp_path / "project.cfg"
    scr_path = tmp_path / "working" / "MyProject.scr"

    write_file(cfg_path, """
        PROJECT = MyProject
        TARGET_PART = xc3s50-4-pq208
        XILINX = /some/path
    """)

    generate_scr(scr_path, cfg_path)

    content = scr_path.read_text()
    assert "-ifn MyProject.prj" in content
    assert "-ofn MyProject.ngc" in content
    assert "-top MyProject" in content
    assert "-p xc3s50-4-pq208" in content


def test_generate_scr_with_top_and_opts(tmp_path):
    cfg_path = tmp_path / "project.cfg"
    scr_path = tmp_path / "working" / "MyProject.scr"

    write_file(cfg_path, """
        PROJECT = MyProject
        TARGET_PART = xc3s200-5-ft256
        TOPLEVEL = TopModule
        XST_OPTS = -opt_mode Speed -opt_level 2
        XILINX = /some/path
    """)

    generate_scr(scr_path, cfg_path)

    content = scr_path.read_text()
    assert "-top TopModule" in content
    assert "-opt_mode Speed -opt_level 2" in content
