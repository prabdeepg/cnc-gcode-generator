# Usage Guide — CNC G-Code Generator

## Basic Usage

```bash
# Run built-in demo (square + hexagon profiles)
python code/gcode_generator.py

# Load a JSON profile file
python code/gcode_generator.py --profile examples/square_pocket.json

# Custom depth, passes, and tool diameter
python code/gcode_generator.py --profile examples/hex_profile.json --depth 8 --passes 4 --tool 6
```

## Profile JSON Format

```json
{
  "name": "my_profile",
  "description": "My custom 2D contour",
  "units": "mm",
  "points": [
    {"x": 0,   "y": 0},
    {"x": 100, "y": 0},
    {"x": 100, "y": 50},
    {"x": 0,   "y": 50}
  ]
}
```

Points should define the part contour (not the tool center path — CRC handles the offset).

## GCodeGenerator Parameters

| Parameter | Default | Description |
|---|---|---|
| program_no | 1 | Program number (O####) |
| tool_no | 1 | Tool number (T##) |
| tool_dia | 10.0 | Tool diameter [mm] |
| spindle_rpm | 3000 | Spindle speed [RPM] |
| feed_cut | 600 | Cutting feed rate [mm/min] |
| feed_plunge | 150 | Plunge feed rate [mm/min] |
| depth_total | 5.0 | Total depth of cut [mm] |
| n_passes | 1 | Number of depth passes |
| clearance_z | 5.0 | Z clearance above part [mm] |
| use_crc | True | Enable cutter radius compensation |
| use_coolant | True | Add M08/M09 coolant blocks |
| units | "metric" | "metric" (G21) or "inch" (G20) |

## Output Files

G-code files are saved to `results/` as `.nc` files (standard CNC program extension).

## Simulating Before Running

**Recommended simulators (free):**
- **Camotics** (camotics.org) — open source, visualizes tool paths in 3D
- **NC Viewer** (ncviewer.com) — browser-based, no install
- **G-Wizard Editor** — commercial, best for beginners

Never run generated G-code on a machine without first simulating it in software.
