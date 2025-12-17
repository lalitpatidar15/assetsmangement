@echo off
setlocal

if not exist "dist\service.exe" (
  echo dist\service.exe not found. Run scripts\build_windows.bat first.
  exit /b 1
)

rem Install and start the Windows service (requires Administrator)
"%~dp0..\dist\service.exe" install || exit /b 1
"%~dp0..\dist\service.exe" start || exit /b 1

echo Service installed and started.
endlocal
exit /b 0
