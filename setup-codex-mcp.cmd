@echo off
setlocal
title LS OpenAPI MCP Setup
chcp 65001 >nul
if not exist "%LOCALAPPDATA%\LSOpenAPI" mkdir "%LOCALAPPDATA%\LSOpenAPI" >nul 2>&1
> "%LOCALAPPDATA%\LSOpenAPI\setup.log" echo LS OpenAPI MCP setup launcher started.
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -STA -File "%~dp0scripts\setup_codex_mcp_gui.ps1" 2>> "%LOCALAPPDATA%\LSOpenAPI\setup.log"
if errorlevel 1 (
  echo.
  echo The setup wizard closed with an error. Details are saved in:
  echo %LOCALAPPDATA%\LSOpenAPI\setup.log
  echo.
  type "%LOCALAPPDATA%\LSOpenAPI\setup.log"
)
echo.
pause
