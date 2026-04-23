"""
CNC G-Code Generator
Prabdeep Singh Ghatora | github.com/prabdeepg

Generates FANUC/Haas-compatible G-code from 2D XY profile coordinates.

Usage:
  python gcode_generator.py                              # demo (square)
  python gcode_generator.py --profile examples/hex_profile.json
  python gcode_generator.py --profile ex.json --depth 5 --passes 3 --tool 10
"""
import math, sys, os, json
from datetime import date
sys.path.insert(0, os.path.dirname(__file__))
from geometry import close_profile, ensure_ccw, polygon_regular, polygon_circle
from validators import validate_gcode


def fmt(v, dec=3):
    return f"{v:.{dec}f}"


class GCodeGenerator:
    def __init__(self, program_no=1, profile_name="profile",
                 tool_no=1, tool_dia=10.0, material="6061-T6 Al",
                 spindle_rpm=3000, feed_cut=600, feed_plunge=150,
                 depth_total=5.0, n_passes=1,
                 clearance_z=5.0, retract_z=50.0,
                 use_crc=True, use_coolant=True,
                 units="metric"):
        self.program_no   = program_no
        self.profile_name = profile_name
        self.tool_no      = tool_no
        self.tool_dia     = tool_dia
        self.material     = material
        self.spindle_rpm  = spindle_rpm
        self.feed_cut     = feed_cut
        self.feed_plunge  = feed_plunge
        self.depth_total  = depth_total
        self.n_passes     = n_passes
        self.clearance_z  = clearance_z
        self.retract_z    = retract_z
        self.use_crc      = use_crc
        self.use_coolant  = use_coolant
        self.units        = units
        self.lines        = []

    def _add(self, line):
        self.lines.append(line)

    def _comment(self, text):
        self._add(f"({text})")

    def preamble(self):
        self._add("%")
        self._add(f"O{self.program_no:04d} (CNC G-CODE GENERATOR - Prabdeep Singh Ghatora)")
        self._comment(f"Profile: {self.profile_name} | Tool: T{self.tool_no:02d} D={self.tool_dia}mm | Material: {self.material}")
        self._comment(f"Date: {date.today().isoformat()}")
        g21_g20 = "G21" if self.units == "metric" else "G20"
        self._add(f"{g21_g20} G17 G90 G94")   # metric/inch, XY plane, absolute, feed/min
        self._add("G28 G91 Z0")                # home Z
        self._add("G28 G91 X0 Y0")             # home XY
        self._add("G90")                        # back to absolute
        self._add(f"T{self.tool_no:02d} M06")  # tool change
        self._add(f"G43 H{self.tool_no:02d}")  # tool length compensation

    def spindle_on(self):
        self._add(f"S{self.spindle_rpm} M03")
        if self.use_coolant:
            self._add("M08")

    def rapid_to(self, x, y):
        self._add(f"G00 X{fmt(x)} Y{fmt(y)}")

    def rapid_z(self, z):
        self._add(f"G00 Z{fmt(z)}")

    def feed_z(self, z):
        self._add(f"G01 Z{fmt(z)} F{fmt(self.feed_plunge, 1)}")

    def crc_on(self, side="right"):
        code = "G42" if side == "right" else "G41"
        self._add(f"{code} D{self.tool_no:02d}")

    def crc_off(self):
        self._add("G40")

    def cut_profile(self, points, feed=None):
        f = feed or self.feed_cut
        first = True
        for p in points:
            if first:
                self._add(f"G01 X{fmt(p[0])} Y{fmt(p[1])} F{fmt(f, 1)}")
                first = False
            else:
                self._add(f"G01 X{fmt(p[0])} Y{fmt(p[1])}")

    def end_program(self):
        if self.use_coolant:
            self._add("M09")
        self._add("G28 G91 Z0")
        self._add("M30")
        self._add("%")

    def generate(self, profile_points):
        """
        Full G-code generation for 2D contour milling.
        profile_points: list of (x,y) tuples defining the contour.
        """
        points = close_profile(ensure_ccw(profile_points))
        start  = points[0]

        self.preamble()
        self.spindle_on()

        depth_per_pass = self.depth_total / self.n_passes
        for pass_num in range(1, self.n_passes + 1):
            z_depth = -(pass_num * depth_per_pass)
            feed_this_pass = self.feed_cut * (0.8 if pass_num < self.n_passes else 1.0)
            self._comment(f"Pass {pass_num}/{self.n_passes}  Z={z_depth:.3f}")
            self.rapid_z(self.clearance_z)
            self.rapid_to(start[0], start[1])
            self.rapid_z(1.0)
            self.feed_z(z_depth)
            if self.use_crc:
                self.crc_on("right")
            self.cut_profile(points, feed=feed_this_pass)
            if self.use_crc:
                self.crc_off()
            self.rapid_z(self.clearance_z)

        self.end_program()
        return self.lines

    def to_string(self):
        return "\n".join(self.lines)

    def save(self, filepath):
        with open(filepath, "w") as f:
            f.write(self.to_string())
        print(f"G-code saved → {filepath}")
        # Validate
        warnings = validate_gcode(self.lines)
        if warnings:
            print("Validation warnings:")
            for lineno, msg in warnings:
                print(f"  Line {lineno}: {msg}")
        else:
            print("Validation: No issues found.")


def demo():
    import os
    os.makedirs("results", exist_ok=True)

    # Demo 1: Square profile
    square = [(10,10),(90,10),(90,90),(10,90)]
    gen = GCodeGenerator(
        program_no=1, profile_name="square_pocket",
        tool_no=1, tool_dia=10, material="6061-T6 Al",
        spindle_rpm=3000, feed_cut=600, feed_plunge=150,
        depth_total=5.0, n_passes=3, use_crc=True
    )
    gen.generate(square)
    gen.save("results/square_pocket.nc")
    print(f"  Lines: {len(gen.lines)}")

    # Demo 2: Hexagon profile
    hex_pts = [(round(x,4), round(y,4)) for x,y in
               __import__('code.geometry', fromlist=['polygon_regular']).polygon_regular(6, 40, 50, 50, 30)]
    gen2 = GCodeGenerator(
        program_no=2, profile_name="hex_profile",
        tool_no=2, tool_dia=6, material="4140 Steel",
        spindle_rpm=1500, feed_cut=300, feed_plunge=80,
        depth_total=8.0, n_passes=4
    )
    gen2.generate(hex_pts)
    gen2.save("results/hex_profile.nc")

    print("\nSquare pocket G-code preview (first 20 lines):")
    for line in gen.lines[:20]:
        print(f"  {line}")
    print("  ...")


def load_and_generate(profile_path, **kwargs):
    with open(profile_path) as f:
        data = json.load(f)
    points = [(p["x"], p["y"]) for p in data["points"]]
    name   = data.get("name", os.path.splitext(os.path.basename(profile_path))[0])
    gen = GCodeGenerator(profile_name=name, **kwargs)
    gen.generate(points)
    out = profile_path.replace(".json", ".nc").replace("examples/", "results/")
    gen.save(out)


if __name__ == "__main__":
    if "--profile" in sys.argv:
        idx = sys.argv.index("--profile")
        pf  = sys.argv[idx+1]
        depth   = float(next((sys.argv[i+1] for i,a in enumerate(sys.argv) if a=="--depth"),   5.0))
        passes  = int(  next((sys.argv[i+1] for i,a in enumerate(sys.argv) if a=="--passes"),  1))
        tool    = float(next((sys.argv[i+1] for i,a in enumerate(sys.argv) if a=="--tool"),    10.0))
        load_and_generate(pf, tool_dia=tool, depth_total=depth, n_passes=passes)
    else:
        demo()
