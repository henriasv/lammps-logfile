## 03_fcc_custom_longlog

- **Structure**: FCC lattice (`lattice fcc`)
- **Thermo**: `thermo_style custom` (not multi), `thermo 1`
- **Multiple runs**: three `run 10000` segments
- **Purpose**: produce a **large log file** (typically a few MB) via per-step thermo output with many columns

Outputs are written to `out/` by the launcher script.


