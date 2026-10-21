@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\setup_codex_mcp.ps1"
if errorlevel 1 (
  echo.
  echo Setup did not complete. Read the error above and try again.
)
echo.
pause
