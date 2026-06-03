# Blakkbox Calibration Refinement Rules

These rules apply to every Denso diesel calibration package added to this repository.

## Required Objective

Every MOD package must prioritize:

- Maximum drivability
- Clean smoke control
- Reduced fuel knock and combustion harshness
- OEM-like torque delivery
- Stable boost, rail, fuel, and torque transitions
- Structural integrity of the original calibration

## Non-Negotiable Protections

- Original files are read-only.
- SW ID must match between ORIGINAL, MOD, and manifest.
- ECU family must be declared.
- Engine and transmission must be declared.
- Untouched OEM regions must remain byte-for-byte unchanged.
- Axis data must not be edited unless explicitly identified and justified.
- DTC, EGR, failsafe, switch logic, and zero-value groups must not be edited.
- No blind whole-file smoothing is allowed.
- No random byte changes are allowed.
- Checksum correction must be documented.

## Modified-Region-Only Rule

Final calibration packages must be traceable as:

```text
FINAL = ORIGINAL + REVIEWED_MOD_DELTA + DOCUMENTED_CHECKSUM_CORRECTION
```

If a byte changes, it must belong to one of these categories:

- Existing MOD delta
- Reviewed refinement inside a known modified map region
- Documented checksum/correction byte

## Smoke Control Rule

Every package must include a smoke-control review statement covering:

- No black smoke at start
- No black smoke at idle
- No black smoke at low load
- No black smoke at mid load
- No black smoke at high load
- Boost-before-fuel behavior preserved
- Rich transient spikes reviewed

## Fuel Knock And Combustion Rule

Every package must include a combustion review statement covering:

- Cold-start rattle risk
- Idle rattle risk
- Low-RPM fuel knock risk
- Abrupt injection-duration jumps
- Pilot-main transition continuity
- Combustion pressure-rise stability

## Surface Quality Rule

Every package must include a surface-quality review statement covering:

- Torque cliffs
- Stair-step transitions
- Sharp gradients
- Neighboring-cell discontinuities
- Boost/fuel synchronization
- Rail/fuel synchronization
- Smoke limiter continuity

## Required Files Per Calibration Package

Each calibration package should include a manifest:

```text
calibrations/<sw_id>/manifest.json
```

The manifest must declare:

- `sw_id`
- `ecu`
- `engine`
- `transmission`
- `original_file`
- `mod_file`
- `final_file`
- `checksum_method`
- `checksum_correction_offset`
- `review.smoke_control`
- `review.fuel_knock`
- `review.combustion_stability`
- `review.surface_quality`
- `review.structural_integrity`

## Human Review Required

This repository workflow can enforce package discipline, but it cannot prove a tune is safe to flash. A human tuner must review map definitions, datalogs, and vehicle behavior before use.
