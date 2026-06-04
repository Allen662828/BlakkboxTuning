@echo off
setlocal EnableExtensions EnableDelayedExpansion
title BlakkboxTuning Builder Workflow

REM ================================================================
REM BlakkboxTuning Builder Workflow
REM ---------------------------------------------------------------
REM Purpose:
REM   Bootstrap a local analysis project for DENSO BIN comparison,
REM   structural review, and checksum validation.
REM
REM Scope:
REM   - OEM vs MOD binary comparison
REM   - Modified-region mapping
REM   - Cluster statistics
REM   - Checksum review workflow
REM   - Report generation
REM
REM Non-scope:
REM   - No tuning logic
REM   - No performance calibration generation
REM   - No fuel/boost/torque/rail modification
REM ================================================================

set "ROOT=%~dp0"
if "%ROOT:~-1%"=="\" set "ROOT=%ROOT:~0,-1%"
set "PROJECT=%ROOT%\BlakkboxTuning_4N15_Workflow"
set "SCRIPTS=%PROJECT%\scripts"
set "INPUTS=%PROJECT%\inputs"
set "REPORTS=%PROJECT%\reports"
set "LOGS=%PROJECT%\logs"
set "DOCS=%PROJECT%\docs"

echo [1/5] Creating project scaffold...
if not exist "%PROJECT%" mkdir "%PROJECT%"
if not exist "%SCRIPTS%" mkdir "%SCRIPTS%"
if not exist "%INPUTS%" mkdir "%INPUTS%"
if not exist "%REPORTS%" mkdir "%REPORTS%"
if not exist "%LOGS%" mkdir "%LOGS%"
if not exist "%DOCS%" mkdir "%DOCS%"

echo [2/5] Writing placeholder instructions...
> "%DOCS%\README.txt" (
  echo BlakkboxTuning 4N15 Workflow
  echo.
  echo Place OEM BIN in inputs\OEM.bin
  echo Place MOD BIN in inputs\MOD.bin
  echo Run: builder_workflow.bat inputs\OEM.bin inputs\MOD.bin
  echo.
  echo Outputs:
  echo - reports\bin_review.md
  echo - reports\bin_review.json
  echo - reports\modified_regions.csv
)

echo [3/5] Checking Python runtime...
where python >nul 2>nul
if errorlevel 1 (
  echo Python not found on PATH.
  echo Install Python 3.10+ and rerun this workflow.
  goto :end
)

echo [4/5] Running binary review script if available...
if exist "%SCRIPTS%\bin_review.py" (
  if "%~1"=="" (
    echo Usage: builder_workflow.bat ^<OEM_BIN^> ^<MOD_BIN^>
  ) else (
    if "%~2"=="" (
      echo Usage: builder_workflow.bat ^<OEM_BIN^> ^<MOD_BIN^>
    ) else (
      python "%SCRIPTS%\bin_review.py" "%~1" "%~2" --outdir "%REPORTS%"
    )
  )
) else (
  echo Missing scripts\bin_review.py
)

echo [5/5] Done.

:end
echo.
echo Project scaffold: %PROJECT%
endlocal
