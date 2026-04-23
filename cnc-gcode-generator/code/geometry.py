"""
2D geometry utilities for G-code generation.
"""
import math


def distance(p1, p2):
    return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)


def close_profile(points):
    """Ensure profile is closed (last point = first point)."""
    if distance(points[0], points[-1]) > 1e-6:
        return points + [points[0]]
    return list(points)


def offset_profile(points, offset):
    """
    Simple inward/outward offset for convex polygons.
    offset > 0: outward; offset < 0: inward.
    For complex profiles use proper offsetting library.
    """
    n = len(points)
    result = []
    for i in range(n):
        p0 = points[(i-1) % n]
        p1 = points[i]
        p2 = points[(i+1) % n]
        # Inward normal at p1
        dx1, dy1 = p1[0]-p0[0], p1[1]-p0[1]
        dx2, dy2 = p2[0]-p1[0], p2[1]-p1[1]
        n1 = math.sqrt(dx1**2+dy1**2)
        n2 = math.sqrt(dx2**2+dy2**2)
        if n1 < 1e-10 or n2 < 1e-10:
            result.append(p1); continue
        nx1, ny1 = -dy1/n1, dx1/n1
        nx2, ny2 = -dy2/n2, dx2/n2
        nx = (nx1+nx2)/2; ny = (ny1+ny2)/2
        nm = math.sqrt(nx**2+ny**2)
        if nm < 1e-10:
            result.append(p1); continue
        result.append((p1[0] + offset*nx/nm, p1[1] + offset*ny/nm))
    return result


def profile_area(points):
    """Shoelace formula for polygon area. Positive = CCW."""
    n = len(points)
    area = 0
    for i in range(n):
        j = (i+1) % n
        area += points[i][0]*points[j][1]
        area -= points[j][0]*points[i][1]
    return area / 2


def ensure_ccw(points):
    """Return points in counter-clockwise order."""
    if profile_area(points) < 0:
        return list(reversed(points))
    return list(points)


def polygon_regular(n_sides, radius, cx=0, cy=0, rotation_deg=0):
    """Generate regular polygon vertices."""
    rot = math.radians(rotation_deg)
    points = []
    for i in range(n_sides):
        angle = rot + 2*math.pi*i/n_sides
        points.append((cx + radius*math.cos(angle),
                        cy + radius*math.sin(angle)))
    return points


def polygon_circle(radius, n_points=36, cx=0, cy=0):
    """Approximate circle with polygon."""
    return polygon_regular(n_points, radius, cx, cy)
