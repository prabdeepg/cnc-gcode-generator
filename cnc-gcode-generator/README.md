# CNC G-Code Generator

A Python tool that takes a 2D profile (list of XY coordinates) and generates valid G-code for CNC milling or turning operations. Outputs ready-to-run G-code with proper preamble, tool change, feed/speed blocks, cutter radius compensation, and safe retract sequences.

## Features
- 2D contour milling from XY coordinate list or DXF-like input
- Supports G00 (rapid), G01 (linear), G02/G03 (arc interpolation)
- Cutter Radius Compensation: G41 (left), G42 (right), G40 (cancel)
- Tool change block: M06 T##
- Spindle speed + direction: S#### M03/M04
- Coolant control: M08/M09
- Safe Z retract and Z plunge with configurable clearance
- Multiple depth passes (roughing + finish pass)
- Output validated against standard G-code format
- Supports inch and metric modes (G20/G21)

## Quick Start
```bash
python code/gcode_generator.py
python code/gcode_generator.py --profile examples/square_pocket.json
python code/gcode_generator.py --profile examples/hex_profile.json --depth 5 --passes 3
```

## Example Output
```gcode
%
O0001 (CNC G-CODE GENERATOR - Prabdeep Singh Ghatora)
(Profile: square_pocket | Tool: T01 D=10mm | Material: 6061-T6 Al)
(Date: 2025-01-15)
G21 G17 G90 G94
G28 G91 Z0
G28 G91 X0 Y0
G90
T01 M06
G43 H01
S3000 M03
M08
G00 Z5.000
G00 X10.000 Y10.000
G00 Z1.000
G01 Z-2.000 F150.0
G42 D01
G01 X10.000 Y10.000 F600.0
G01 X90.000 Y10.000
G01 X90.000 Y90.000
G01 X10.000 Y90.000
G01 X10.000 Y10.000
G40
G00 Z5.000
M09
G28 G91 Z0
M30
%
```

## Repository Structure
```
cnc-gcode-generator/
├── code/
│   ├── gcode_generator.py       # Main G-code generator
│   ├── geometry.py              # Arc fitting, coordinate transforms
│   └── validators.py            # G-code syntax checker
├── examples/
│   ├── square_pocket.json       # Square contour profile
│   ├── hex_profile.json         # Hexagonal profile
│   └── circle_profile.json      # Circular profile
├── calculations/
│   ├── feeds_speeds_theory.md   # How speeds/feeds are embedded
│   └── gcode_reference.md      # G-code command reference
├── bom/
│   ├── BOM.md
│   └── bom.csv
├── docs/
│   ├── usage_guide.md
│   └── machine_setup.md
├── issues/
│   └── ISSUES_LOG.md
├── results/
│   └── RESULTS.md
└── tests/
    └── test_gcode.py
```

## Safety Notice
Always simulate generated G-code in a machine simulator (e.g., CNCSimulator Pro, Camotics) before running on actual hardware. Verify tool paths, clearance heights, and feed rates match your machine and fixturing.

## Author
Prabdeep Singh Ghatora | [github.com/prabdeepg](https://github.com/prabdeepg)
