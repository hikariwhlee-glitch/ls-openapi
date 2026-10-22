@echo off
setlocal
title LS OpenAPI MCP Setup
chcp 65001 >nul
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -STA -File "%~dp0scripts\setup_codex_mcp_gui.ps1"
if errorlevel 1 (
  echo.
  echo Setup did not complete. Read the error above and try again.
)
echo.
pause
