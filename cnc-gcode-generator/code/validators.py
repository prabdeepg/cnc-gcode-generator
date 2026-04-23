"""
G-code validator — checks for common programming errors.
"""
import re


def validate_gcode(lines):
    """
    Check a list of G-code lines for common errors.
    Returns list of (line_no, warning_message) tuples.
    """
    warnings = []
    has_m30 = False
    has_percent_end = False
    last_z = None
    modal_plane = "G17"
    crc_active = False
    crc_code = None

    for i, line in enumerate(lines, 1):
        line = line.strip().upper()
        if not line or line.startswith('(') or line.startswith(';'):
            continue
        if line == '%':
            has_percent_end = True
            continue

        # Check M30
        if 'M30' in line:
            has_m30 = True

        # Track CRC
        if 'G41' in line or 'G42' in line:
            crc_active = True
            crc_code = 'G41' if 'G41' in line else 'G42'
        if 'G40' in line:
            crc_active = False

        # Extract Z value
        z_match = re.search(r'Z(-?\d+\.?\d*)', line)
        if z_match:
            z_val = float(z_match.group(1))
            # Warn if rapid move goes below Z0 (likely unsafe)
            if 'G00' in line and z_val < 0:
                warnings.append((i, f"G00 rapid move to negative Z={z_val:.3f} — verify this is intentional"))
            last_z = z_val

        # Check for feed rate on G01 moves
        if 'G01' in line and 'F' not in line:
            # Only warn if this doesn't look like the first G01 (modal F already set)
            if last_z is not None and last_z < 0:
                warnings.append((i, f"G01 move without F word — relies on modal feed rate"))

    if not has_m30:
        warnings.append((len(lines), "No M30 found — program may not end properly"))
    if crc_active:
        warnings.append((len(lines), f"CRC ({crc_code}) not cancelled with G40 before end of program"))

    return warnings
