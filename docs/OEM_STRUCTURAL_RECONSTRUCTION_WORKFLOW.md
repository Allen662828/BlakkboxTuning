# OEM Structural Reconstruction Workflow

## Objective
Eliminate byte-linear smoothing behavior and replace it with topology-aware OEM calibration reconstruction.

---

# Core Philosophy

FINAL = ORIGINAL + STRUCTURED_FILTERED_DELTA

Rules:
- Preserve OEM structure
- Preserve axis behavior
- Preserve interpolation continuity
- Preserve torque hierarchy
- Preserve combustion stability
- Preserve rail-pressure progression
- Preserve boost/fuel synchronization
- Preserve fail-safe behavior
- Preserve contiguous calibration geometry

Never:
- Blind percentage scaling
- Global byte smoothing
- Random attenuation
- Non-structural flattening
- Destructive map collapsing

---

# Correct DENSO Workflow

## STEP 1 — SW Verification
Verify:
- SW ID
- ROM size
- checksum region
- endian structure
- map layout consistency

Reject processing if:
- offset drift exists
- ROM sizes mismatch
- fragmented corruption exists

---

## STEP 2 — Structural Delta Detection
Detect:
- contiguous modified regions
- LE16 coherent calibration structures
- axis-aligned modification zones
- repeated table signatures

Classification:
- isolated bytes
- structured table edits
- axis regions
- checksum zones
- non-calibration regions

---

# STEP 3 — Table Geometry Reconstruction

CRITICAL:
Never smooth raw binary globally.

The workflow must reconstruct REAL 2D table behavior.

Required:
- preserve OEM curvature vectors
- preserve row energy distribution
- preserve column progression
- preserve axis gradients
- preserve edge anchors
- preserve torque surface topology

Forbidden:
- flat averaging
- binary-wide smoothing
- linear collapse
- edge destruction
- high-load flattening

---

# STEP 4 — Axis-Aware Processing

## Row Processing
Rows represent:
- load progression
- injection quantity progression
- torque request structure

Rules:
- smooth inside row only
- preserve row curvature
- maintain monotonic behavior
- preserve edge reference cells

## Column Processing
Columns represent:
- rail pressure progression
- RPM progression
- boost structure

Rules:
- preserve pressure gradient continuity
- prevent abrupt pressure cliffs
- maintain OEM response ramp

---

# STEP 5 — Weighted Delta Reconstruction

Instead of:
NEW = OEM + global_scaled_delta

Use:
NEW = OEM + directional_filtered_delta

Directional filtering:
- center-weighted attenuation
- edge protection
- topology-preserving blending
- local gradient stabilization

---

# STEP 6 — Spike Suppression Logic

Detect:
- isolated islands
- sharp second derivatives
- discontinuous interpolation zones
- abrupt gradient inversions

Repair:
- directional blending
- local topology reconstruction
- neighbor-weighted interpolation

Never flatten entire region.

---

# STEP 7 — OEM Surface Validation

Validate:
- 3D surface continuity
- smooth torque progression
- smooth rail-pressure ramps
- combustion-safe transitions
- realistic DENSO map appearance

Reject if:
- plateau collapse exists
- stair-step artifacts exist
- isolated peaks remain
- row energy imbalance exists
- curvature inversion exists

---

# STEP 8 — Checksum Reconstruction

Required:
- checksum-aware rebuild
- additive correction validation
- checksum patch logging
- final hash validation

Validation:
- ROM size exact match
- checksum exact match
- untouched OEM regions identical

---

# STEP 9 — Required Output Artifacts

Generate:
- diff_report.md
- diff_ranges.csv
- le16_changes.csv
- block_summary.csv
- checksum_report.txt
- topology_validation.txt
- processed_output.bin

---

# STEP 10 — OEM Economy Calibration Strategy

## Injection Duration
- reduce excessive high-load duration
- preserve idle smoothness
- preserve pilot stability
- preserve transient combustion quality

## Torque Structure
- preserve OEM pedal hierarchy
- reduce unnecessary low-RPM spikes
- maintain drivability smoothness

## Boost Control
- reduce unnecessary boost demand
- maintain airflow balance
- avoid compressor surge regions

## Rail Pressure
- stabilize ramps
- preserve pressure continuity
- avoid oscillatory transitions

---

# Final Validation Standard

A valid DENSO economy calibration MUST:
- visually resemble OEM topology
- preserve directional gradients
- maintain interpolation smoothness
- avoid flattened surfaces
- avoid random spike edits
- maintain combustion-safe structure
- preserve OEM engineering behavior
