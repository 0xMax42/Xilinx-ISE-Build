from tools.config import parse_vhdl_ls_toml
from pathlib import Path
import tempfile
import textwrap
import pytest


def test_parsing_skips_third_party_libs():
    content = textwrap.dedent("""
        [libraries.lib]
        files = ["src/main.vhd"]

        [libraries.XILINX]
        files = ["/opt/Xilinx/abc.vhd"]
        is_third_party = true
    """)
    with tempfile.NamedTemporaryFile("w+", suffix=".toml", delete=False) as f:
        f.write(content)
        f.flush()
        result = parse_vhdl_ls_toml(Path(f.name))

    assert "work" in result
    assert "XILINX" not in result
    assert result["work"] == [Path("src/main.vhd")]


def test_parsing_multiple_libraries():
    content = textwrap.dedent("""
        [libraries.lib]
        files = ["src/foo.vhd", "src/bar.vhd"]

        [libraries.myip]
        files = ["ipcore/top.vhd"]
    """)
    with tempfile.NamedTemporaryFile("w+", suffix=".toml", delete=False) as f:
        f.write(content)
        f.flush()
        result = parse_vhdl_ls_toml(Path(f.name))

    assert "work" in result
    assert "myip" in result
    assert result["work"] == [Path("src/foo.vhd"), Path("src/bar.vhd")]
    assert result["myip"] == [Path("ipcore/top.vhd")]


def test_empty_toml_file():
    with tempfile.NamedTemporaryFile("w+", suffix=".toml", delete=False) as f:
        f.write("")  # Empty file
        f.flush()
        result = parse_vhdl_ls_toml(Path(f.name))

    assert result == {}


def test_missing_file_raises_error():
    with pytest.raises(FileNotFoundError):
        parse_vhdl_ls_toml(Path("nonexistent.toml"))


def test_libname_translation_to_work():
    content = textwrap.dedent("""
        [libraries.lib]
        files = ["src/xyz.vhd"]
    """)
    with tempfile.NamedTemporaryFile("w+", suffix=".toml", delete=False) as f:
        f.write(content)
        f.flush()
        result = parse_vhdl_ls_toml(Path(f.name))

    assert "work" in result
    assert "lib" not in result
    assert result["work"] == [Path("src/xyz.vhd")]
