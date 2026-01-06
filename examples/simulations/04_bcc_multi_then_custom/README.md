## 04_bcc_multi_then_custom

- **Structure**: BCC lattice (`lattice bcc`)
- **Thermo**: starts with `thermo_style multi`, switches to `thermo_style custom`, then back to `multi`
- **Multiple runs**: several `run` segments, includes NVT and NVE

This one is useful for testing parsing across **thermo style changes** within a single log.


