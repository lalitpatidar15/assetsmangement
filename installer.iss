[Setup]
AppName=Asset Integrity Agent
AppVersion=1.0
DefaultDirName={pf}\AssetAgent
DisableProgramGroupPage=yes
UninstallDisplayIcon={app}\agent.exe
UninstallPassword=STRONG_PASSWORD_123
PrivilegesRequired=admin

[Files]
Source: "dist\agent.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\service.exe"; DestDir: "{app}"

[Run]
Filename: "{app}\service.exe"; Parameters: "install"; Flags: runhidden
Filename: "{app}\service.exe"; Parameters: "start"; Flags: runhidden

[UninstallRun]
Filename: "{app}\service.exe"; Parameters: "stop"; Flags: runhidden
Filename: "{app}\service.exe"; Parameters: "remove"; Flags: runhidden
