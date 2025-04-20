from build.tools.config import parse_project_cfg
from pathlib import Path
import tempfile
import textwrap


def test_parse_complex_project_cfg_correctly():
    cfg = textwrap.dedent("""
        ## Main settings.. ##
        PROJECT = SpriteChannel
        TARGET_PART = xc3s1200e-4-fg320
        XILINX = /opt/Xilinx/14.7/ISE_DS/ISE
        TOPLEVEL = SpriteChannel
        CONSTRAINTS = src/SpriteChannel.ucf

        # Sources (should be ignored)
        VHDSOURCE += src/GenericCounter.vhd
        VSOURCE += src/something.v
        VHDTEST += test/SpriteChannel_tb.vhd

        # Options
        XST_OPTS += -opt_mode Speed
        XST_OPTS += -opt_level 2
        MAP_OPTS = -detail -timing -ol high
        PAR_OPTS = -ol high
        BITGEN_OPTS = -g StartupClk:JtagClk

        # Programmer
        PROGRAMMER = digilent
    """)

    with tempfile.NamedTemporaryFile("w+", suffix=".cfg", delete=False) as f:
        f.write(cfg)
        f.flush()
        result = parse_project_cfg(Path(f.name))

    assert result["PROJECT"] == "SpriteChannel"
    assert result["TARGET_PART"] == "xc3s1200e-4-fg320"
    assert result["XILINX"] == "/opt/Xilinx/14.7/ISE_DS/ISE"
    assert result["TOPLEVEL"] == "SpriteChannel"
    assert result["CONSTRAINTS"] == "src/SpriteChannel.ucf"
    assert result["XST_OPTS"] == "-opt_mode Speed -opt_level 2"
    assert result["MAP_OPTS"] == "-detail -timing -ol high"
    assert result["PAR_OPTS"] == "-ol high"
    assert result["BITGEN_OPTS"] == "-g StartupClk:JtagClk"
    assert result["PROGRAMMER"] == "digilent"

    # Sicherstellen, dass SOURCE-Felder ignoriert wurden
    assert "VHDSOURCE" not in result
    assert "VSOURCE" not in result
    assert "VHDTEST" not in result
