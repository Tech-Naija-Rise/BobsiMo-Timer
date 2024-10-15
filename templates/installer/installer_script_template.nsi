!include MUI2.nsh
!define VERSION "1.2.3"
!define APP_NAME_ONLY "BobsiMo Timer"
!define APP_NAME "BobsiMo Timer ${VERSION}"

Name "${APP_NAME}"
#Icon .\BMT_logo.ico

OutFile "BobsiMo Timer - ${VERSION}.exe"
InstallDir "$PROGRAMFILES\BobsiMo Timer\${VERSION}"

!define MUI_ICON .\BMT_logo.ico
!define MUI_UNICON .\BMT_logo.ico

!define MUI_WELCOMEFINISHPAGE_BITMAP .\BMT_logo.bmp
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP .\BMT_logo.bmp

!define MUI_WELCOMEPAGE_TITLE "Welcome to ${APP_NAME_ONLY} Setup"
!define MUI_WELCOMEPAGE_TEXT "This setup will guide you through the installation of BobsiMo Timer"
	!insertmacro MUI_PAGE_WELCOME



	!insertmacro MUI_PAGE_INSTFILES



!define MUI_FINISHPAGE_TITLE "Thank You for Installing ${APP_NAME_ONLY}"
!define MUI_FINISHPAGE_TEXT "${APP_NAME} has now been installed on your computer$\n$\nClick on the finish button to continue"
!define MUI_FINISHPAGE_RUN "$INSTDIR\${APP_NAME}.exe"
!define MUI_FINISHPAGE_RUN_TEXT "Run ${APP_NAME_ONLY}"
	!insertmacro MUI_PAGE_FINISH


    !insertmacro MUI_UNPAGE_WELCOME
    !insertmacro MUI_UNPAGE_CONFIRM
    !insertmacro MUI_UNPAGE_FINISH


Function shortcut
    CreateShortcut "$DESKTOP\${APP_NAME_ONLY}.lnk" "$INSTDIR\${APP_NAME}.exe" ".\BMT_logo.ico"
     SetShellVarContext all
    CreateShortcut "$SMSTARTUP\${APP_NAME_ONLY}.lnk" "$INSTDIR\${APP_NAME}.exe" ".\BMT_logo.ico"

    CreateShortcut "$STARTMENU\Programs\${APP_NAME_ONLY}.lnk" "$INSTDIR\${APP_NAME}.exe" ".\BMT_logo.ico"
    #make a key for windows list of programs
FunctionEnd




Section "Timer App"
    # Dump the exe file
    SetOutPath "$INSTDIR"
    File /r ".\BobsiMo Timer ${VERSION}\*.*"    
    
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\BobsiMo" "Display Name" "${APP_NAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\BobsiMo" "UninstallString" '"$INSTDIR\Uninstall_BMT.exe"'

    ;Create uninstaller
    WriteUninstaller "$INSTDIR\Uninstall_BMT.exe"

    # Call to create the shortcut
    Call shortcut
SectionEnd




Section "Uninstall"
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
    RMDir /r "$INSTDIR\_internal"
    Delete "$INSTDIR\${APP_NAME}.exe"
    Delete "$INSTDIR\Uninstall_BMT.exe"
    RMDir "$INSTDIR"
SectionEnd