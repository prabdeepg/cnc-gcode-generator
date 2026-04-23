# G-Code Reference — FANUC/Haas Format

## Preparatory (G) Codes Used

| Code | Description | Modal? |
|---|---|---|
| G00 | Rapid positioning | Yes |
| G01 | Linear interpolation | Yes |
| G02 | Circular interpolation CW | Yes |
| G03 | Circular interpolation CCW | Yes |
| G17 | XY plane selection | Yes |
| G20 | Inch units | Yes |
| G21 | Metric units (mm) | Yes |
| G28 | Return to reference point | No |
| G40 | Cancel cutter radius compensation | Yes |
| G41 | Cutter radius comp — left | Yes |
| G42 | Cutter radius comp — right | Yes |
| G43 | Tool length compensation | Yes |
| G90 | Absolute coordinate mode | Yes |
| G91 | Incremental coordinate mode | Yes |
| G94 | Feed per minute mode | Yes |

## Miscellaneous (M) Codes Used

| Code | Description |
|---|---|
| M03 | Spindle on — clockwise (forward) |
| M04 | Spindle on — counter-clockwise |
| M05 | Spindle stop |
| M06 | Tool change |
| M08 | Coolant on |
| M09 | Coolant off |
| M30 | End of program + rewind |

## Address Words

| Letter | Meaning | Example |
|---|---|---|
| X, Y, Z | Axis coordinates | X50.000 |
| F | Feed rate (mm/min or in/min) | F600.0 |
| S | Spindle speed (RPM) | S3000 |
| T | Tool number | T01 |
| H | Tool length offset register | H01 |
| D | Cutter radius offset register | D01 |
| N | Block number (optional) | N0010 |
| O | Program number | O0001 |

## Program Structure Template

```gcode
%                           ← Program start marker
O0001 (program name)        ← Program number + comment
(setup comments)
G21 G17 G90 G94             ← Mode settings
G28 G91 Z0                  ← Home Z
G28 G91 X0 Y0               ← Home XY
G90                         ← Absolute mode
T01 M06                     ← Tool change
G43 H01                     ← Tool length comp activate
S3000 M03                   ← Spindle on
M08                         ← Coolant on
(tool path blocks)
M09                         ← Coolant off
G28 G91 Z0                  ← Return Z to home
M30                         ← End of program
%                           ← End marker
```

## Cutter Radius Compensation (CRC)

CRC offsets the tool path by the tool radius so you program the actual part contour, not the tool center path.

```gcode
G42 D01       ← Activate CRC right (outside of CW contour)
G01 X... Y... ← Tool center offset D01 mm to the right of programmed path
G40           ← Cancel CRC (return to programmed path)
```

Rules:
- G41 = tool left of programmed path (inside of CCW contour / outside of CW contour from above)
- G42 = tool right of programmed path
- Must have at least one G00/G01 move after G41/G42 before cutting (lead-in)
- Cancel with G40 before rapid moves and program end
