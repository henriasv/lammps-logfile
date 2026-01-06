## 02_bcc_custom_thermo

- **Structure**: BCC lattice (`lattice bcc`)
- **Thermo**: `thermo_style custom` (includes `v_rho` and `v_msd`)
- **Multiple runs**: `run 0`, NVT run, NVE run, plus a short run with a dump

Outputs are written to `out/` by the launcher script.


