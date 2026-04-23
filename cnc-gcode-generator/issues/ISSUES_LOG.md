# Issues Log — CNC G-Code Generator

---

## ISSUE-001 — CRC Lead-In Not Implemented (Abrupt Entry)
**Status:** Partial Fix  
**Severity:** Medium  

**Description:**  
G41/G42 requires a linear or arc lead-in move before the cutter contacts the part. The initial implementation activated CRC and immediately began the contour — some controls (Fanuc 0i-MB) raise alarm PS0039 (illegal plane change with CRC) or gouge the part on activation.

**Root Cause:**  
CRC compensation becomes fully active only after the first G00/G01 move following the G41/G42 block. If that first move is the first contour point, the tool approaches with an offset that may not be tangent to the profile.

**Fix:**  
Added a configurable lead-in distance (default 5mm). Before the first contour point, the generator adds a G01 move 5mm outside the start point in the direction perpendicular to the first contour segment. This allows CRC to fully activate before cutting begins. Lead-out is symmetric.

**Verification:**  
Tested in Camotics — no gouge observed on square and hexagon profiles with 10mm tool.

---

## ISSUE-002 — No Arc (G02/G03) Support — Only Linear Interpolation
**Status:** Known Limitation  
**Severity:** Medium  

**Description:**  
Current generator only outputs G01 linear moves. Circle profiles are approximated as polygons (36-point default), producing faceted toolpaths. For truly round parts, native G02/G03 arc blocks are needed.

**Fix (Planned):**  
Implement arc fitting: detect 3 consecutive collinear points within a specified angle threshold, fit a circle, output G02/G03 with I/J center offsets. Planned in `geometry.py` as `fit_arcs()`.

---

## ISSUE-003 — Absolute vs. Incremental Mode Confusion
**Status:** Resolved  
**Severity:** Low  

**Description:**  
The G28 home sequence uses G91 (incremental) mode temporarily: `G28 G91 Z0`. After this block, the tool is in G91 mode — subsequent moves were incremental instead of absolute, causing position errors.

**Root Cause:**  
G28 with G91 is intentional (move to home relative to current position), but the modal state remains G91.

**Fix:**  
Added explicit `G90` block after both G28 home sequences to restore absolute mode. Verified in Camotics: all subsequent XY moves are now absolute.

---

## ISSUE-004 — Profile Not Closed Causes Open Contour
**Status:** Resolved  
**Severity:** High  

**Description:**  
If the last profile point doesn't match the first point, the generated G-code traces an open contour — the end mill lifts without returning to the start, leaving a shoulder on the part.

**Fix:**  
Added `close_profile()` in `geometry.py`: checks if last point == first point (within 1e-6mm tolerance). If not, appends the first point to close the loop. Applied automatically in `generate()`.
