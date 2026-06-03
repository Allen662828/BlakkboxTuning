# DENSO Delta Workflow Rules

## Core Processing Sequence
1. Verify SW ID
2. Verify ROM structure
3. Verify exact BIN size alignment
4. Detect contiguous modified regions only
5. Preserve untouched OEM bytes 1:1
6. Analyze torque hierarchy consistency
7. Synchronize boost and fuel behavior
8. Moderate rail pressure transitions
9. Apply interpolation-safe smoothing
10. Export processed calibration only

## Delta Filtering
- Δ0–5 keep
- Δ5–8 ×0.80
- Δ>8 ×0.55
- Remove spikes
- Smooth jagged transitions
- Preserve interpolation continuity

## Structural Preservation Rules
- Untouched OEM regions must remain byte-for-byte identical
- No offset drift allowed
- Preserve OEM fail-safe behavior
- Preserve diagnostic logic structure
- Preserve OEM emissions logic structure

## Protected Regions
Never modify:
- EGR maps
- DTC regions
- Diagnostic masks
- OEM monitor logic
- 0-group values from MOD file

## Enhancement Scope
Apply enhancement only to:
- torque
- boost
- fuel
- rail pressure
- driver demand
- limiter harmonization

## Stability Targets
- No excessive smoke at idle
- No unstable low-load combustion
- No harsh idle knock
- Stable transient torque delivery
- Smooth table interpolation behavior
