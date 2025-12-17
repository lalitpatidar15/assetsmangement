# Asset Integrity Agent (Windows)

Minimal Windows agent to detect HDD/SSD model, serial, size, generate a fingerprint, run as a Windows Service, and package with Inno Setup.

## 1. Requirements (Windows)
- Windows 10/11 (64-bit)
- Python 3.10+ (64-bit) on the build machine

Install dependencies (on Windows):
```bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller
```

## 2. Agent
- File: `agent.py`
- Outputs JSON with disk model, serial, size (GB), interface, media_type, and a fingerprint.

Run (Windows):
```bat
python agent.py
```

## 3. Build EXEs (PyInstaller)
Option A: Run helper script
```bat
scripts\build_windows.bat
```

Option B: Manual
```bat
pyinstaller --onefile --noconsole agent.py
pyinstaller --onefile service.py
```
Outputs are in `dist\agent.exe` and `dist\service.exe`.

## 4. Install Windows Service (Admin)
```bat
scripts\install_service.bat
```
Uninstall:
```bat
scripts\uninstall_service.bat
```
Service name: `AssetIntegrityAgent`

## 5. Installer (Inno Setup)
- Script: `installer.iss`
- Build with Inno Setup Compiler on Windows.
- Uninstall is password-protected via `UninstallPassword` in the script.

Typical files packaged:
- `dist\agent.exe`
- `dist\service.exe`

The installer will:
- Copy EXEs to `{pf}\AssetAgent`
- Install and start the service on finish
- Stop and remove the service on uninstall

## Notes
- `wmi` and `pywin32` are Windows-only; they are conditionally installed by `requirements.txt` on Windows.
- Build and service installation must be performed on a Windows machine.
