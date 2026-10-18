; Audacity 4.0.1 Hebrew language pack installer
; Builds: AudacityHe-4.0.1-Installer.exe
; Installs the compiled Qt catalogue (audacity_he.qm) into Audacity's locale
; directory so Preferences > General > Language > Hebrew can load it.

Unicode true
Name "Audacity Hebrew Language Pack 4.0.1"
OutFile "..\deliverable\AudacityHe-4.0.1-Installer.exe"
InstallDir "$PROGRAMFILES64\Audacity"
InstallDirRegKey HKLM "Software\Audacity" "InstallPath"
RequestExecutionLevel admin
SetCompressor /SOLID lzma

Page directory
Page components
Page instfiles
UninstPage uninstConfirm
UninstPage instfiles

Section "Hebrew catalogue (required)" SEC_MAIN
  SetOutPath "$INSTDIR\share\audacity4\locale"
  File "audacity_he.qm"
  ; remember install dir for uninstaller
  WriteRegStr HKLM "Software\AudacityHebrew" "InstallDir" "$INSTDIR"
  ; uninstaller
  WriteUninstaller "$INSTDIR\AudacityHe-Uninstall.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AudacityHebrew" \
      "DisplayName" "Audacity Hebrew Language Pack 4.0.1"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AudacityHebrew" \
      "Publisher" "Audacity Hebrew translation project"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AudacityHebrew" \
      "UninstallString" "$INSTDIR\AudacityHe-Uninstall.exe"
  CreateShortCut "$SMPROGRAMS\Audacity Hebrew Language Pack.lnk" "$INSTDIR\AudacityHe-Uninstall.exe"
SectionEnd

Section "Readme" SEC_README
  SetOutPath "$INSTDIR"
  File "README-he.txt"
SectionEnd

Section "Uninstall"
  Delete "$INSTDIR\share\audacity4\locale\audacity_he.qm"
  Delete "$INSTDIR\README-he.txt"
  Delete "$INSTDIR\AudacityHe-Uninstall.exe"
  Delete "$SMPROGRAMS\Audacity Hebrew Language Pack.lnk"
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AudacityHebrew"
  DeleteRegKey HKLM "Software\AudacityHebrew"
SectionEnd
