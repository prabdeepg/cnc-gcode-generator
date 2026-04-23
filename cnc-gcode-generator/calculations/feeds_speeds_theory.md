# Feeds & Speeds in G-Code Context

## How Speed (S word) Maps to RPM

The S word sets spindle speed in RPM directly:
```
S3000 → 3000 RPM
```

Corresponding surface cutting speed (for reference):
```
V (m/min) = π × D (mm) × N (rpm) / 1000
```

For a 10mm end mill at 3000 RPM:
```
V = π × 10 × 3000 / 1000 = 94.25 m/min
```

For 6061-T6 aluminum with coated carbide, recommended V = 150–200 m/min.
3000 RPM on a 10mm tool = 94 m/min — slightly conservative (safe for prototype work).

Optimal RPM for 150 m/min:
```
N = V × 1000 / (π × D) = 150,000 / (π × 10) = 4,775 RPM
```

## How Feed (F word) Sets Table Travel Speed

```
F600 → 600 mm/min feed rate
```

Corresponding chip load (feed per tooth):
```
fz = F / (N × z)
```

For F=600, N=3000, z=2 flutes:
```
fz = 600 / (3000 × 2) = 0.10 mm/tooth
```

Recommended chip load for 10mm 2-flute end mill in 6061-T6: 0.05–0.15 mm/tooth ✓

## Multi-Pass Strategy

For the rough passes, feed is reduced to 80% of finish feed:
- Rough: F × 0.80 = F480 (more conservative, higher axial depth)
- Finish: F × 1.00 = F600 (full feed, final surface quality pass)

The last pass (finish) runs at the full programmed depth with full feed rate for best surface finish.
