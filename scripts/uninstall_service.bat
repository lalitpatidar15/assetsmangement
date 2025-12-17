@echo off
setlocal

if exist "%~dp0..\dist\service.exe" (
  "%~dp0..\dist\service.exe" stop
  "%~dp0..\dist\service.exe" remove
) else (
  echo dist\service.exe not found. If the service exists, you can remove it via:
  echo   sc stop AssetIntegrityAgent ^&^& sc delete AssetIntegrityAgent
)

echo Uninstall attempted. Check Services for status.
endlocal
exit /b 0
