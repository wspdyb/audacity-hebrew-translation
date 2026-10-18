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

Var TARGET_LOCALE_DIR

Page directory "" "" dirLeave
Page components
Page instfiles
UninstPage uninstConfirm
UninstPage instfiles

Function .onInit
  ; Auto-detect if running or if installed in portable / standard path
  ; 1. Check if bin\Audacity4.exe or Audacity.exe exists in the registry path or default path
  IfFileExists "$INSTDIR\locale\*.*" found_good
  IfFileExists "$INSTDIR\share\audacity4\locale\*.*" found_good
  IfFileExists "$INSTDIR\share\locale\*.*" found_good

  ; Try finding from running process or common paths if default does not have Audacity executable
  IfFileExists "$INSTDIR\bin\Audacity4.exe" found_good
  IfFileExists "$INSTDIR\Audacity.exe" found_good

  ; Check Downloads folder where current user has the portable version
  IfFileExists "$PROFILE\Downloads\audacity-win-4.0.1-x86_64\Audacity-4.0.1.262721353[909d5f7]-x86_64\bin\Audacity4.exe" 0 not_downloads
    StrCpy $INSTDIR "$PROFILE\Downloads\audacity-win-4.0.1-x86_64\Audacity-4.0.1.262721353[909d5f7]-x86_64"
    Goto found_good
  not_downloads:

  found_good:
FunctionEnd

Function dirLeave
  ; Strip trailing slashes
  StrCpy $R0 "$INSTDIR" "" -1
  StrCmp $R0 "\" 0 no_slash
    StrCpy $INSTDIR "$INSTDIR" -1
  no_slash:

  ; Check where locale directory is
  ; Case 1: Directly inside $INSTDIR\locale (standard layout for Audacity 4 release packages)
  IfFileExists "$INSTDIR\locale\*.*" is_root_locale 0

  ; Case 2: Under share\audacity4\locale (standard Linux/FHS or some custom builds)
  IfFileExists "$INSTDIR\share\audacity4\locale\*.*" is_share_audacity4 0

  ; Case 3: Under share\locale
  IfFileExists "$INSTDIR\share\locale\*.*" is_share_locale 0

  ; Case 4: The user selected the "bin" folder by mistake
  IfFileExists "$INSTDIR\..\locale\*.*" is_bin_parent 0

  ; Case 5: The user has bin\Audacity4.exe in $INSTDIR, create $INSTDIR\locale
  IfFileExists "$INSTDIR\bin\Audacity4.exe" is_root_locale 0
  IfFileExists "$INSTDIR\Audacity.exe" is_root_locale 0

  ; Warning if no Audacity seems to be in the folder
  MessageBox MB_YESNO|MB_ICONEXCLAMATION "תיקיית Audacity או תיקיית שפות (locale) לא זוהתה בנתיב שנבחר.$\nהאם להמשיך ולהתקין בנתיב זה בכל זאת?" IDYES is_root_locale
  Abort

is_bin_parent:
  GetFullPathName $INSTDIR "$INSTDIR\.."
  StrCpy $TARGET_LOCALE_DIR "$INSTDIR\locale"
  Goto done

is_share_audacity4:
  StrCpy $TARGET_LOCALE_DIR "$INSTDIR\share\audacity4\locale"
  Goto done

is_share_locale:
  StrCpy $TARGET_LOCALE_DIR "$INSTDIR\share\locale"
  Goto done

is_root_locale:
  StrCpy $TARGET_LOCALE_DIR "$INSTDIR\locale"
  Goto done

done:
FunctionEnd

Section "Hebrew catalogue (required)" SEC_MAIN
  ; Fallback if TARGET_LOCALE_DIR is empty
  StrCmp $TARGET_LOCALE_DIR "" 0 has_locale_dir
    StrCpy $TARGET_LOCALE_DIR "$INSTDIR\locale"
  has_locale_dir:

  CreateDirectory "$TARGET_LOCALE_DIR"
  SetOutPath "$TARGET_LOCALE_DIR"
  File "audacity_he.qm"

  ; If share\audacity4\locale also exists, copy there as well for full compatibility
  IfFileExists "$INSTDIR\share\audacity4\locale\*.*" 0 no_dual_copy
    CreateDirectory "$INSTDIR\share\audacity4\locale"
    CopyFiles /SILENT "$TARGET_LOCALE_DIR\audacity_he.qm" "$INSTDIR\share\audacity4\locale\audacity_he.qm"
  no_dual_copy:

  ; Clean up old misplaced file if it exists from previous installations
  IfFileExists "$INSTDIR\Audacity\share\audacity4\locale\audacity_he.qm" 0 no_clean_sub
    Delete "$INSTDIR\Audacity\share\audacity4\locale\audacity_he.qm"
    RMDir "$INSTDIR\Audacity\share\audacity4\locale"
    RMDir "$INSTDIR\Audacity\share\audacity4"
    RMDir "$INSTDIR\Audacity\share"
    Delete "$INSTDIR\Audacity\README-he.txt"
    Delete "$INSTDIR\Audacity\AudacityHe-Uninstall.exe"
    RMDir "$INSTDIR\Audacity"
  no_clean_sub:

  ; remember install dir for uninstaller
  WriteRegStr HKLM "Software\AudacityHebrew" "InstallDir" "$INSTDIR"
  WriteRegStr HKLM "Software\AudacityHebrew" "LocaleDir" "$TARGET_LOCALE_DIR"

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
  ReadRegStr $0 HKLM "Software\AudacityHebrew" "LocaleDir"
  StrCmp $0 "" default_uninstall_locale
    Delete "$0\audacity_he.qm"
    Goto cont_uninstall

default_uninstall_locale:
  Delete "$INSTDIR\locale\audacity_he.qm"
  Delete "$INSTDIR\share\audacity4\locale\audacity_he.qm"

cont_uninstall:
  Delete "$INSTDIR\README-he.txt"
  Delete "$INSTDIR\AudacityHe-Uninstall.exe"
  Delete "$SMPROGRAMS\Audacity Hebrew Language Pack.lnk"
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\AudacityHebrew"
  DeleteRegKey HKLM "Software\AudacityHebrew"
SectionEnd
