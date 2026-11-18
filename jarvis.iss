; ═══════════════════════════════════════════════════════
;  MINI-JARVIS — Instalador Inno Setup
;  Para compilar: abra este arquivo no Inno Setup e clique
;  em "Compile" (ou rode o ISCC.exe por linha de comando).
; ═══════════════════════════════════════════════════════

[Setup]
AppName=MINI-JARVIS
AppVersion=3.1
AppPublisher=Projeto Escolar
DefaultDirName={autopf}\MINI-JARVIS
DefaultGroupName=MINI-JARVIS
OutputBaseFilename=Instalador-MINI-JARVIS
SetupIconFile=logo.ico
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64compatible arm64

[Files]
Source: "jarvis.py";    DestDir: "{app}"; Flags: ignoreversion
Source: "jarvis_gui.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "executar.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md";    DestDir: "{app}"; Flags: ignoreversion
Source: "logo.ico";     DestDir: "{app}"; Flags: ignoreversion
Source: "logo.png";     DestDir: "{app}"; Flags: ignoreversion
Source: "plugins\*";    DestDir: "{app}\plugins"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\MINI-JARVIS"; Filename: "{app}\executar.bat"; IconFilename: "{app}\logo.ico"
Name: "{autodesktop}\MINI-JARVIS"; Filename: "{app}\executar.bat"; IconFilename: "{app}\logo.ico"

[Run]
Filename: "{app}\executar.bat"; Description: "Abrir o MINI-JARVIS agora"; Flags: postinstall skipifsilent

[Code]
// Avisa se o Python não estiver instalado
function InitializeSetup(): Boolean;
var
  PythonOk: Boolean;
  Codigo: Integer;
begin
  PythonOk := Exec('cmd.exe', '/c python --version', '', SW_HIDE, ewWaitUntilTerminated, Codigo) and (Codigo = 0);
  if not PythonOk then
    MsgBox('Atenção: Python não foi encontrado!' + #13#10 +
           'Instale em python.org antes de usar o MINI-JARVIS.', mbInformation, MB_OK);
  Result := True;
end;

// Depois de instalar, garante a biblioteca da interface
procedure CurStepChanged(CurStep: TSetupStep);
var
  Codigo: Integer;
begin
  if CurStep = ssPostInstall then
    Exec('cmd.exe', '/c python -m pip install customtkinter --quiet',
         '', SW_HIDE, ewWaitUntilTerminated, Codigo);
end;
