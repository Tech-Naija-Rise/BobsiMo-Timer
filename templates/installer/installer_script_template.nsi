!include MUI2.nsh
!define VERSION "1.2.3"
!define APP_NAME_ONLY "BobsiMo Timer"
!define APP_NAME "BobsiMo Timer ${VERSION}"

Name "${APP_NAME}"
InstallDir "$PROGRAMFILES\BobsiMo Timer"  # No version in the folder path

# Set the installer output file
OutFile "BobsiMo Timer - ${VERSION}.exe"

# Icon and Uninstaller Icon
!define MUI_ICON ".\BMT_logo.ico"
!define MUI_UNICON ".\BMT_logo.ico"

# Welcome and Header Images
!define MUI_WELCOMEFINISHPAGE_BITMAP ".\BMT_logo.bmp"
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP ".\BMT_logo.bmp"

# Welcome Page Customization
!define MUI_WELCOMEPAGE_TITLE "Welcome to ${APP_NAME_ONLY} Setup"
!define MUI_WELCOMEPAGE_TEXT "This setup will guide you through the installation of BobsiMo Timer"
!insertmacro MUI_PAGE_WELCOME

# Installation Progress Page
!insertmacro MUI_PAGE_INSTFILES

# Finish Page Customization
!define MUI_FINISHPAGE_TITLE "Thank You for Installing ${APP_NAME_ONLY}"
!define MUI_FINISHPAGE_TEXT "${APP_NAME} has now been installed on your computer$\n$\nClick on the finish button to continue"
!define MUI_FINISHPAGE_RUN "$INSTDIR\${APP_NAME_ONLY}.exe"
!define MUI_FINISHPAGE_RUN_TEXT "Run ${APP_NAME_ONLY}"
!insertmacro MUI_PAGE_FINISH

# Uninstaller Pages
!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_FINISH

# Function to create shortcuts
Function CreateShortcuts
    CreateShortcut "$DESKTOP\${APP_NAME_ONLY}.lnk" "$INSTDIR\${APP_NAME_ONLY}.exe" "$INSTDIR\BMT_logo.ico"
    CreateShortcut "$SMPROGRAMS\${APP_NAME_ONLY}\${APP_NAME_ONLY}.lnk" "$INSTDIR\${APP_NAME_ONLY}.exe" "$INSTDIR\BMT_logo.ico"
FunctionEnd

# Section for installing the app
Section "Timer App"
    SetOutPath "$INSTDIR"
    File /r ".\BobsiMo Timer\*.*"  # Assuming the app files are in the folder 'BobsiMo Timer'
    
    # Write registry keys for uninstall info
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\BobsiMo" "Display Name" "${APP_NAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\BobsiMo" "UninstallString" '"$INSTDIR\Uninstall_BMT.exe"'

    # Create uninstaller
    WriteUninstaller "$INSTDIR\Uninstall_BMT.exe"

    # Create desktop and start menu shortcuts
    Call CreateShortcuts
SectionEnd

# Uninstall Section
Section "Uninstall"
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\BobsiMo"
    RMDir /r "$INSTDIR"
    Delete "$INSTDIR\Uninstall_BMT.exe"
SectionEnd
