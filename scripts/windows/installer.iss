[Setup]
AppName=Blender Hub
AppVersion={#Version}
AppPublisher=vdfuste

; DefaultDirName={autopf}\Blender Hub
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
DefaultDirName={commonpf64}\Blender Hub

DefaultGroupName=Blender Hub
AllowNoIcons=yes
OutputDir=.
OutputBaseFilename=BlenderHub-{#Version}-Windows-Installer
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "..\..\output\dist\blenderhub\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs 

[Run]
Filename: "{app}\BlenderHub.exe"; Description: "{cm:LaunchProgram,Blender Hub}"; Flags: nowait postinstall skipifsilent
