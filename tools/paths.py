import os
from pathlib import Path
import sys

# Ermittle absoluten Pfad dieser Datei
HERE = Path(__file__).resolve()

# Gehe zurück von tools/ → build/ → Projekt-Root
ROOT = HERE.parent.parent.parent

# Abgeleitete Pfade
BUILD = ROOT / "build"
WORKING = BUILD / "working"
REPORTS = BUILD / "reports"

# Relativer Pfad von WORKING zurück zur Projektwurzel
REL_FROM_WORKING_TO_ROOT = Path(os.path.relpath(ROOT, WORKING))

# Standard-Konfigurationsdateien
PROJECT_CFG = ROOT / "project.cfg"
VHDL_LS_TOML = ROOT / "vhdl_ls.toml"
