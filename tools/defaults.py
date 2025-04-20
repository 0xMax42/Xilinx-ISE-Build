# tools/defaults.py
from typing import Dict

def get_default_config() -> Dict[str, str]:
    return {
        "TOPLEVEL": "",  # wird dynamisch ersetzt
        "CONSTRAINTS": "",
        "BUILD_DIR": "working",
        "REPORT_DIR": "reports",
        "COMMON_OPTS": "-intstyle xflow",
        "XST_OPTS": "",
        "NGDBUILD_OPTS": "",
        "MAP_OPTS": "-detail",
        "PAR_OPTS": "",
        "BITGEN_OPTS": "",
        "TRACE_OPTS": "-v 3 -n 3",
        "FUSE_OPTS": "-incremental",
        "ISIM_OPTS": "-gui",
        "ISIM_CMD": "",
        "PROGRAMMER": "none",
        "PROGRAMMER_PRE": "",
        "IMPACT_OPTS": "-batch impact.cmd",
        "DJTG_EXE": "djtgcfg",
        "DJTG_DEVICE": "DJTG_DEVICE-NOT-SET",
        "DJTG_INDEX": "0",
        "DJTG_FLASH_INDEX": "1",
        "XC3SPROG_EXE": "xc3sprog",
        "XC3SPROG_CABLE": "none",
        "XC3SPROG_OPTS": "",
    }

def with_defaults(project_cfg: Dict[str, str]) -> Dict[str, str]:
    merged = get_default_config()
    merged.update(project_cfg)

    # Fallbacks sicherstellen (kein leerer oder None-Wert bleibt erhalten)
    if not merged.get("TOPLEVEL"):
        merged["TOPLEVEL"] = merged.get("PROJECT", "")
    if not merged.get("CONSTRAINTS"):
        merged["CONSTRAINTS"] = f"{merged.get('PROJECT', '')}.ucf"

    # Alle Felder final auf gültigen string casten (zur Sicherheit)
    return {k: (v if isinstance(v, str) else str(v)) for k, v in merged.items()}
