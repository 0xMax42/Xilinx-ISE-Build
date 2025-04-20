import tempfile
from pathlib import Path
from tasks.generate_prj import generate_prj


def write_file(path: Path, content: str):
    path.write_text(content.strip(), encoding="utf-8")


def test_generate_prj_single_lib(tmp_path):
    cfg_path = tmp_path / "project.cfg"
    toml_path = tmp_path / "vhdl_ls.toml"
    prj_path = tmp_path / "working" / "MyProject.prj"

    write_file(cfg_path, "PROJECT = MyProject\nTARGET_PART = dummy\nXILINX = /some/path")
    write_file(toml_path, """
        [libraries.lib]
        files = ["src/main.vhd"]
    """)

    generate_prj(prj_path, cfg_path, toml_path)

    assert prj_path.exists()
    content = prj_path.read_text()
    assert "vhdl work ../src/main.vhd" in content


def test_generate_prj_multiple_libs(tmp_path):
    cfg_path = tmp_path / "project.cfg"
    toml_path = tmp_path / "vhdl_ls.toml"
    prj_path = tmp_path / "working" / "MyProject.prj"

    write_file(cfg_path, "PROJECT = MyProject\nTARGET_PART = dummy\nXILINX = /some/path")
    write_file(toml_path, """
        [libraries.lib]
        files = ["src/A.vhd", "src/B.vhd"]

        [libraries.otherlib]
        files = ["src/C.vhd"]
    """)

    generate_prj(prj_path, cfg_path, toml_path)

    content = prj_path.read_text()
    assert "vhdl work ../src/A.vhd" in content
    assert "vhdl work ../src/B.vhd" in content
    assert "vhdl otherlib ../src/C.vhd" in content
