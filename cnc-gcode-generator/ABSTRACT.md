# Abstract — CNC G-Code Generator

## Problem Statement
Generating correct G-code for simple 2D profiles is time-consuming when done manually, especially for prototype parts where the full CAD/CAM workflow (SolidWorks → HSMWorks → post-processor) is overkill. A lightweight Python script that converts XY coordinate lists directly to verified G-code fills this gap for simple contours.

## Objective
Build a Python G-code generator that takes a 2D profile as a JSON coordinate list and produces machine-ready G-code with a complete, safe preamble, configurable depth passes, cutter radius compensation, and proper end-of-program sequences.

## Methodology
- Defined G-code structure following FANUC 0i-MF / Haas control format (most common on VMCs)
- Implemented profile traversal: convert (x,y) list to G01 linear moves
- Added multi-pass depth logic: rough passes at (depth/n) increments, finish pass at final depth
- Implemented cutter radius compensation lead-in/lead-out (G41/G42 with tangent approach)
- Built G-code validator to check for common errors (missing G40, no M30, Z-level sequencing)
- Tested output on Haas VF-2 simulator and Camotics open-source simulator

## Key Results
- Generated G-code for 4 standard profiles: square, hexagon, circle, custom cam lobe
- Validated in Camotics: all 4 programs run without syntax errors or unsafe moves
- Square pocket (80×80mm, 5mm depth, 3 passes, 10mm end mill): 47 lines of G-code vs. ~300+ in typical CAM output (leaner, easier to read and edit)
- Cutter radius compensation correctly offset the tool path 5mm (D=10mm) from programmed contour on all test cases
- Feed rate overrides applied correctly per pass (rough: 80% of finish feed)

## Skills Demonstrated
Python · CNC programming · G-code (FANUC/Haas format) · CNC machining operations · Manufacturing process planning
