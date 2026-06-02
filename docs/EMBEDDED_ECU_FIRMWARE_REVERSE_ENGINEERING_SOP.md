# EMBEDDED ECU FIRMWARE REVERSE ENGINEERING & CALIBRATION DISCOVERY SOP

## Document Type
Standard Operating Procedure

## Scope
Static firmware analysis, calibration discovery, map identification, integrity verification, and structured firmware modeling for embedded ECU systems.

## Primary Toolchain
- IDA Pro
- Ghidra
- WinOLS
- TunerPro

---

# 1. OBJECTIVE

Establish a repeatable workflow for:

- Firmware normalization
- Hardware fingerprinting
- Memory segmentation
- Static code analysis
- Calibration structure discovery
- Axis and map inference
- Integrity verification
- Confidence-ranked export generation

Primary priorities:

- Structural correctness
- Low false-positive rate
- Reproducibility
- OEM layout preservation
- Deterministic analysis behavior

---

# 2. ACCEPTED INPUT FORMATS

Supported formats:

- Raw binary (*.bin)
- Intel HEX (*.hex)
- Motorola S-record (*.s19, *.mot)
- ELF engineering artifacts (*.elf)

All formats shall be normalized into flat binary form before analysis.

---

# 3. REQUIRED TOOLCHAIN

## Reverse Engineering
- IDA Pro
- Ghidra

## Calibration Visualization
- WinOLS
- TunerPro

## Supporting Utilities
- Hex editor
- CRC/checksum analyzers
- Signature scanners
- Python automation scripts
- CAN/logging interfaces
- Flash programmers

---

# 4. WORKFLOW OVERVIEW

## STAGE 1
Firmware normalization

OUTPUT:
Flat binary

## STAGE 2
Hardware fingerprinting

OUTPUT:
MCU/layout hypothesis

## STAGE 3
Memory segmentation

OUTPUT:
Region map

## STAGE 4
Static code analysis

OUTPUT:
Function map

## STAGE 5
Structural extraction

OUTPUT:
Strings/pointers/XREFs

## STAGE 6
Axis/map inference

OUTPUT:
Candidate calibrations

## STAGE 7
Integrity analysis

OUTPUT:
CRC/checksum model

## STAGE 8
Protected-region analysis

OUTPUT:
Compression/encryption flags

## STAGE 9
Confidence scoring

OUTPUT:
Ranked structures

## STAGE 10
Structured export

OUTPUT:
Final analysis model

---

# 5. FIRMWARE NORMALIZATION PROCEDURE

## 5.1 IMPORT

Import source without modification.

Record:
- Original file name
- Original format
- File size
- Base address assumptions
- Known MCU family
- Read method

## 5.2 DECODE

Convert HEX/S-record formats into flat binary while preserving address continuity.

## 5.3 VERIFY

Confirm:
- No truncation
- No offset drift
- Stable byte count
- Correct padding behavior

---

# 6. HARDWARE FINGERPRINTING PROCEDURE

## 6.1 ARCHITECTURE IDENTIFICATION

Determine probable MCU family using:
- Reset vectors
- Interrupt table layout
- Opcode patterns
- Known signatures
- Address spacing

Examples:
- SH705x
- SH725xx
- MPC5xx
- TriCore
- RH850

## 6.2 ENDIANNESS INFERENCE

Evaluate:
- Pointer validity
- String alignment
- Checksum field behavior
- Instruction decoding stability

Select byte order producing:
- Logical pointers
- Valid disassembly
- Consistent structure interpretation

---

# 7. MEMORY SEGMENTATION PROCEDURE

Segment binary into probable regions:

## BOOTLOADER
Indicators:
- Reset vectors
- Startup routines

## APPLICATION
Indicators:
- Dense executable code

## CALIBRATION
Indicators:
- Structured smooth tables

## NVM
Indicators:
- Flags
- Counters
- Adaptation storage

## PROTECTED/COMPRESSED
Indicators:
- High entropy

## 7.1 ENTROPY ANALYSIS

Classification:
- Low entropy = structured data
- Medium entropy = executable code
- High entropy = encrypted/compressed

---

# 8. STATIC CODE ANALYSIS PROCEDURE

## 8.1 LOAD INTO RE PLATFORM

Import binary into:
- IDA Pro
- Ghidra

Apply:
- Correct architecture
- Endianness
- Base address assumptions

## 8.2 ANALYZE

Perform:
- Function discovery
- Cross-reference analysis
- Pointer tracing
- Call graph analysis
- Data reference extraction

## 8.3 STRING EXTRACTION

Extract ASCII/Unicode strings.

Flag:
- Calibration identifiers
- Software IDs
- DTC labels
- Diagnostic text
- Build metadata

---

# 9. CALIBRATION DISCOVERY PROCEDURE

## 9.1 AXIS CANDIDATE DETECTION

Identify sequences exhibiting:
- Monotonic increase
- Logical scaling
- Consistent step spacing
- Valid engineering progression

Typical formats:
- 8-bit
- 16-bit

## 9.2 MAP CANDIDATE DETECTION

Identify rectangular blocks with:
- Smooth interpolation behavior
- Gradient continuity
- Neighbor consistency
- Non-random variance

## 9.3 DIMENSION VALIDATION

Validate using nearby dimension clues:
- Row count
- Column count
- Product matches table size

## 9.4 ALIGNMENT VALIDATION

Confirm:
- 2-byte alignment
- 4-byte alignment
- Consistent table spacing

---

# 10. INTEGRITY VERIFICATION PROCEDURE

## 10.1 CRC DISCOVERY

Search for:
- CRC tables
- Polynomial patterns
- Validation routines

## 10.2 CHECKSUM VALIDATION

Test hypotheses across:
- Boot region
- Application region
- Calibration region

Correct integrity model shall:
- Validate consistently
- Match logical boundaries
- Operate under one stable byte order

---

# 11. PROTECTED REGION DETECTION

Evaluate regions for:
- Compression
- Encryption
- Obfuscation

Indicators:
- High entropy
- Invalid instruction density
- Broken pointer locality
- Abnormal structure repetition

---

# 12. CONFIDENCE SCORING SYSTEM

Each detected structure shall receive scoring based on:

- Pointer validity
- Axis monotonicity
- Smoothness
- Alignment correctness
- XREF support
- Statistical consistency
- Checksum compatibility

## Confidence Levels

### 90–100
CONFIRMED

### 75–89
HIGHLY PROBABLE

### 50–74
PROBABLE

### <50
WEAK CANDIDATE

---

# 13. AUTOMATION REQUIREMENTS

Automation scripts shall include:
- Signature scanning
- Candidate ranking
- Axis correlation analytics
- Statistical sampling
- Confidence interval checks
- False-positive suppression
- Unit-tested validation routines

---

# 14. EXPORT REQUIREMENTS

Final export shall contain:
- Memory region map
- Function inventory
- String database
- Pointer graph
- Calibration candidates
- Axis definitions
- Integrity model
- Protected-region flags
- Confidence scores

Preferred export formats:
- JSON
- CSV
- XML
- SQLite database

---

# 15. QUALITY ASSURANCE

Before final approval verify:
- No offset drift
- Consistent endianness
- Checksum repeatability
- Map smoothness
- Pointer locality
- Calibration continuity
- Reproducibility across repeated runs

---

# 16. FINAL ACCEPTANCE CRITERIA

Analysis is accepted only if:
- Firmware layout is internally consistent
- Calibration structures are statistically defensible
- Integrity behavior is reproducible
- Candidate maps exhibit realistic interpolation behavior
- Protected regions are properly isolated
- Structured export is complete and reproducible

---

# 17. CORE OPERATING PRINCIPLE

> Prove layout first.
> Prove structure second.
> Prove calibration meaning last.
