# SW#89663-0K383 Economy Delta Workflow

## Objective
Preserve OEM DENSO structure while converting aggressive MOD behavior into combustion-safe economy-oriented calibration.

## Core Calibration Rules
- FINAL = ORIGINAL + FILTERED_DELTA
- Preserve untouched OEM regions byte-for-byte
- No offset drift
- Preserve torque hierarchy consistency
- Preserve OEM fail-safe logic
- Maintain boost/fuel synchronization
- Maintain rail pressure stability
- Remove spikes and unstable interpolation behavior

## Validation Sequence
1. Verify exact SW ID
2. Verify ROM size alignment
3. Verify checksum integrity
4. Detect contiguous modified regions only
5. Analyze LE16 structured calibration changes
6. Apply filtered delta processing
7. Rebuild calibration preserving OEM structure
8. Recalculate checksum
9. Validate final binary integrity

## SW#89663-0K383 Analysis
### Binary Summary
- ROM Size: 376832 bytes
- Changed Bytes: 6714
- Changed Ranges: 783
- Changed LE16 Words: 3634
- LE16 Increase/Decrease: 3564 / 70
- Dominant behavior: positive calibration scaling

### High Activity Regions
- 0x001000-0x001FFF
- 0x008000-0x008FFF
- 0x00F000-0x00FFFF
- 0x012000-0x012FFF
- 0x009000-0x009FFF

## BLAKKBOX Delta Filtering
### Delta Policy
- Δ0–5 keep
- Δ5–8 ×0.70
- Δ>8 ×0.40

### Filtering Rules
- Remove isolated spikes
- Smooth jagged transitions
- Preserve interpolation continuity
- Prevent abrupt torque transitions
- Prevent fuel over-command behavior
- Prevent boost overshoot regions

## Economy Calibration Strategy
### Injection Control
- Reduce excessive duration scaling
- Reduce low-load smoke tendency
- Stabilize idle combustion
- Smooth transient enrichment

### Torque Structure
- Preserve OEM torque hierarchy
- Maintain predictable pedal mapping
- Avoid aggressive low-RPM torque spikes

### Boost Synchronization
- Reduce unnecessary high-load boost demand
- Preserve turbo response continuity
- Maintain air/fuel balance

### Rail Pressure
- Preserve stable pressure ramps
- Avoid abrupt pressure oscillation
- Retain OEM safety margins

## Checksum Validation
### Verified Correction
- Original sum8: 0x49
- MOD sum8 before: 0x44
- Required correction: +0x05
- Patched offset: 0x05BFFF
- Final corrected sum8: 0x49

## Repository Workflow Standard
### Required Outputs
- diff_report.md
- diff_ranges.csv
- block_summary.csv
- le16_changes.csv
- checksum_report.txt
- processed_output.bin

### Required Validation Gates
- ROM size exact match
- No offset migration
- No uncontrolled spike generation
- No random global scaling
- Checksum valid
- Untouched OEM regions preserved

## Engineering Notes
Structured LE16 increases indicate coherent calibration editing behavior rather than random binary corruption. Future enhancement stages must remain map-aware and checksum-aware. Blind percentage scaling is prohibited.
