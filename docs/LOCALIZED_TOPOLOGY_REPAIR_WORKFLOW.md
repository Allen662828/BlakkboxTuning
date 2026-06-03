# Localized Topology Repair Workflow

## Target
Toyota Denso Diesel 2
SW#89663-0K383

## Objective
Repair structurally coherent calibration regions using localized topology-aware reconstruction instead of global binary smoothing.

## Confirmed Observations
Pilot injection map topology remains recoverable:
- pressure-axis decay remains monotonic
- load progression remains coherent
- edge anchors remain mostly intact
- curvature continuity partially preserved

Localized spike contamination exists mainly in:
- mid/high load rows
- 320–1600 bar pressure region

## Structural Validation
Confirmed:
- ROM size valid
- checksum correction valid
- LE16 structures coherent
- contiguous modified regions detected
- modification density approximately 1.78%

## Workflow Logic

### Stage 1 — Table Boundary Preservation
Never smooth globally.

Required:
- preserve table geometry
- preserve edge vectors
- preserve OEM curvature
- preserve row energy balance

### Stage 2 — Axis Preservation
Pressure-axis behavior must remain:
- monotonic
- directionally smooth
- interpolation-safe

Load-axis behavior must remain:
- torque-coherent
- progressively decaying
- free from isolated sink regions

### Stage 3 — Localized Spike Repair
Only repair:
- isolated peaks
- abrupt second derivatives
- discontinuous local harmonics

Never flatten:
- entire plateaus
- valid OEM gradients
- edge anchors

### Stage 4 — Directional Reconstruction
Apply:
- row-direction continuity validation
- column-direction continuity validation
- curvature-preserving interpolation
- localized harmonic blending

### Stage 5 — Surface Validation
Reject calibration if:
- sink regions appear
- plateau collapse exists
- curvature inversion exists
- pressure cliffs appear
- interpolation instability exists

## Required Outputs
- topology_validation.txt
- structured_region_summary.csv
- checksum_report.txt
- processed_output.bin

## Engineering Direction
Future execution must become:
- true map-aware
- axis-aware
- topology-aware
- interpolation-aware
- checksum-aware
