@echo off
setlocal
title LS OpenAPI MCP Setup
chcp 65001 >nul
echo.
echo LS OpenAPI MCP command-line setup
echo API calls and orders are not executed during setup.
echo Your app key and secret will be entered in hidden prompts.
echo.
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\setup_codex_mcp.ps1"
set "SETUP_EXIT_CODE=%ERRORLEVEL%"
echo.
if "%SETUP_EXIT_CODE%"=="0" (
  echo Setup completed successfully.
) else (
  echo Setup failed with exit code %SETUP_EXIT_CODE%.
  echo See the error above. Detailed log, if available:
  echo %LOCALAPPDATA%\LSOpenAPI\setup.log
)
echo.
pause
exit /b %SETUP_EXIT_CODE%
