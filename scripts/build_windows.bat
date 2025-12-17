@echo off
setlocal

where python >nul 2>nul || (
  echo Python not found. Please install Python 3.10+ (64-bit).
  exit /b 1
)

python -m pip install --upgrade pip || exit /b 1
python -m pip install -r requirements.txt || exit /b 1
python -m pip install pyinstaller || exit /b 1

pyinstaller --onefile --noconsole agent.py || exit /b 1
pyinstaller --onefile service.py || exit /b 1

echo.
echo Build complete. Binaries are in the dist\ folder.
endlocal
exit /b 0
