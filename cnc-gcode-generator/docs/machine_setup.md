# Machine Setup Notes

## Coordinate System Setup

Before running the program:
1. Set work offset G54 (or G55/G56) with X0 Y0 at a known reference point on the part/fixture
2. Set Z0 at the top surface of the part
3. Measure and enter tool length offset in H## register

## Tool Length Offset

G43 H01 activates tool length compensation using the value stored in H01 offset register.

To measure:
1. Touch off tool to Z0 surface using a tool setter or paper feeler
2. Set H01 = machine Z coordinate at that point (usually negative)

## Cutter Radius Offset

D01 register stores the cutter radius value used by G41/G42.

For a 10mm diameter end mill: D01 = 5.0mm

Note: Some operators enter the full diameter and use G41/G42 D-word differently — check your machine's manual. FANUC 0i-MF uses D = tool radius.

## Feed Rate Override

Most controls have a feed rate override knob (0–200%). Start at 50% override for first run of a new program, confirm path looks correct, then increase to 100%.

## Common Setup Mistakes
- Forgetting to set G54 (parts crash because machine is still in G53 machine coordinates)
- Z0 set to table surface instead of part top surface (full depth cuts on first pass)
- D register set to diameter instead of radius (double cutter offset, parts are undersized)
- No M06 tool change on first block (program tries to cut with whatever tool is loaded)
