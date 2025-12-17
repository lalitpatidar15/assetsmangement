[Setup]
AppName=Asset Integrity Agent
AppVersion=1.0
DefaultDirName={pf}\AssetAgent
DisableProgramGroupPage=yes
UninstallDisplayIcon={app}\agent.exe
PrivilegesRequired=admin
OutputDir=dist-installer
OutputBaseFilename=AssetIntegrityAgentSetup

[Files]
Source: "dist\agent.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\service.exe"; DestDir: "{app}"
Source: "scripts\repair.ps1"; DestDir: "{app}"

[Run]
Filename: "{app}\service.exe"; Parameters: "install"; Flags: runhidden
Filename: "{app}\service.exe"; Parameters: "start"; Flags: runhidden
; Set service recovery to auto-restart on failure
Filename: "sc.exe"; Parameters: "failure AssetIntegrityAgent reset= 0 actions= restart/60000/restart/60000/restart/60000"; Flags: runhidden
; Create hourly SYSTEM task to repair service if removed
Filename: "schtasks.exe"; Parameters: "/Create /TN ""AssetAgentRepair"" /SC MINUTE /MO 5 /RU ""SYSTEM"" /RL HIGHEST /TR ""powershell.exe -NoProfile -ExecutionPolicy Bypass -File """"{app}\repair.ps1"""""" /F"; Flags: runhidden

[UninstallRun]
Filename: "{app}\service.exe"; Parameters: "stop"; Flags: runhidden
Filename: "{app}\service.exe"; Parameters: "remove"; Flags: runhidden
; Remove scheduled task on uninstall
Filename: "schtasks.exe"; Parameters: "/Delete /TN ""AssetAgentRepair"" /F"; Flags: runhidden
