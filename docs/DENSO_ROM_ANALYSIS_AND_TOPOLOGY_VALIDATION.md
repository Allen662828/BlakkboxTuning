# DENSO ROM Analysis and Topology Validation

## Target Platform
- Toyota Denso Diesel 2
- Engine family: 2KD
- Software ID: 89663-0K383
- ROM size validation required

## Objective
Provide a safe ROM analysis framework focused on:
- structural validation
- checksum integrity
- LE16 topology discovery
- map candidate identification
- interpolation continuity analysis
- OEM surface preservation

## ROM Validation
Required checks:
- exact file-size alignment
- endian consistency
- checksum-domain validation
- offset integrity
- contiguous modified-region analysis

Reject ROM if:
- fragmented corruption exists
- offset drift exists
- checksum structure invalid

## LE16 Structural Analysis
Analyze:
- monotonic ramps
- rectangular data regions
- contiguous structured regions
- smooth gradient candidates
- axis-like progression

## Candidate Classification
Identify probable:
- torque-related structures
- pressure-related structures
- duration-related structures
- interpolation surfaces

## Topology Validation
Validate:
- row continuity
- column continuity
- directional gradients
- curvature continuity
- edge-anchor preservation

Reject structures showing:
- abrupt discontinuities
- isolated spikes
- plateau collapse
- curvature inversion
- unstable interpolation

## OEM Preservation Rules
Always preserve:
- untouched OEM bytes
- interpolation continuity
- checksum integrity
- contiguous structure behavior
- stable progression behavior

## Output Artifacts
Generate:
- diff_report.md
- checksum_report.txt
- block_summary.csv
- topology_validation.txt
- structured_region_summary.csv

## Engineering Direction
Future implementation target:
- automated DENSO table discovery
- semantic structure classification
- topology-aware reconstruction validation
- OEM surface continuity analysis
