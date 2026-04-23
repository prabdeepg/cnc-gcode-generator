"""
Tests for G-code generator.
Run: python -m pytest tests/ -v
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))
from gcode_generator import GCodeGenerator
from geometry import close_profile, ensure_ccw, profile_area, polygon_regular
from validators import validate_gcode

SQUARE = [(10,10),(90,10),(90,90),(10,90)]

def make_gen(**kwargs):
    defaults = dict(program_no=1, profile_name="test", tool_no=1, tool_dia=10,
                    spindle_rpm=3000, feed_cut=600, feed_plunge=150,
                    depth_total=5.0, n_passes=1, use_crc=False, use_coolant=False)
    defaults.update(kwargs)
    return GCodeGenerator(**defaults)

def test_program_starts_with_percent():
    g = make_gen()
    lines = g.generate(SQUARE)
    assert lines[0] == "%"

def test_program_ends_with_m30():
    g = make_gen()
    lines = g.generate(SQUARE)
    assert any("M30" in l for l in lines)

def test_program_ends_with_percent():
    g = make_gen()
    lines = g.generate(SQUARE)
    assert lines[-1] == "%"

def test_validator_no_warnings_clean_program():
    g = make_gen()
    lines = g.generate(SQUARE)
    warnings = validate_gcode(lines)
    assert len(warnings) == 0, f"Unexpected warnings: {warnings}"

def test_multi_pass_generates_multiple_z_levels():
    g = make_gen(n_passes=3, depth_total=6.0)
    lines = g.generate(SQUARE)
    z_lines = [l for l in lines if l.startswith("G01 Z-")]
    assert len(z_lines) == 3, f"Expected 3 plunge moves, got {len(z_lines)}"

def test_close_profile():
    pts = [(0,0),(10,0),(10,10),(0,10)]
    closed = close_profile(pts)
    assert closed[-1] == closed[0]

def test_ensure_ccw():
    cw = [(0,0),(0,10),(10,10),(10,0)]  # CW in standard coords
    ccw = ensure_ccw(cw)
    assert profile_area(ccw) > 0

def test_polygon_regular_hexagon():
    pts = polygon_regular(6, 40, 50, 50)
    assert len(pts) == 6
    # All points should be ~40mm from center
    import math
    for x,y in pts:
        r = math.sqrt((x-50)**2 + (y-50)**2)
        assert abs(r - 40) < 0.01

print("Tests defined. Run: python -m pytest tests/ -v")
