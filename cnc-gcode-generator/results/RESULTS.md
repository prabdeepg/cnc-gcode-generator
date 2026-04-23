# Results — CNC G-Code Generator

## Demo Run 1: Square Pocket (80×80mm)

**Parameters:** Tool T01 Ø10mm, 6061-T6 Al, S3000, F600, depth 5mm, 3 passes

| Parameter | Value |
|---|---|
| Total G-code lines | 47 |
| Depth per pass | 1.667mm |
| Rough feed (passes 1–2) | 480 mm/min |
| Finish feed (pass 3) | 600 mm/min |
| Program O-number | O0001 |

**Simulated in Camotics:** ✓ No gouges, no air cuts, correct pocket boundary.

Sample output excerpt:
```gcode
%
O0001 (CNC G-CODE GENERATOR - Prabdeep Singh Ghatora)
G21 G17 G90 G94
G28 G91 Z0
G28 G91 X0 Y0
G90
T01 M06
G43 H01
S3000 M03
M08
(Pass 1/3  Z=-1.667)
G00 Z5.000
G00 X10.000 Y10.000
G00 Z1.000
G01 Z-1.667 F150.0
G42 D01
G01 X10.000 Y10.000 F480.0
G01 X90.000 Y10.000
G01 X90.000 Y90.000
G01 X10.000 Y90.000
G01 X10.000 Y10.000
G40
G00 Z5.000
...
M09
G28 G91 Z0
M30
%
```

---

## Demo Run 2: Hexagon Profile (R=40mm, centered 50,50)

**Parameters:** Tool T02 Ø6mm, 4140 Steel, S1500, F300, depth 8mm, 4 passes

| Parameter | Value |
|---|---|
| Total G-code lines | 58 |
| Depth per pass | 2.0mm |
| Passes | 4 |

**Simulated in Camotics:** ✓ Clean hexagonal contour.

---

## Validation Summary

| Profile | Lines | Camotics Result | Validator |
|---|---|---|---|
| square_pocket | 47 | ✓ Pass | No warnings |
| hex_profile | 58 | ✓ Pass | No warnings |
| circle_profile | 91 | ✓ Pass | No warnings |
