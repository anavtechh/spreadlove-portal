$WshShell = New-Object -ComObject WScript.Shell

# 1. Startup Shortcut
$StartupPath = [System.Environment]::GetFolderPath('Startup')
$StartupShortcut = $WshShell.CreateShortcut("$StartupPath\SpreadLovePortal.lnk")
$StartupShortcut.TargetPath = "wscript.exe"
$StartupShortcut.Arguments = '"F:\Spread love\linkedin_automation\run_silent.vbs"'
$StartupShortcut.WorkingDirectory = "F:\Spread love\linkedin_automation"
$StartupShortcut.Description = "Spread Love Foundation LinkedIn Portal Background Service"
$StartupShortcut.Save()
Write-Host "Created Startup Shortcut: $StartupPath\SpreadLovePortal.lnk"

# 2. Desktop Shortcut
$DesktopPath = [System.Environment]::GetFolderPath('Desktop')
$DesktopShortcut = $WshShell.CreateShortcut("$DesktopPath\Spread Love LinkedIn Portal.lnk")
$DesktopShortcut.TargetPath = "http://127.0.0.1:5050"
$DesktopShortcut.Description = "Spread Love Foundation LinkedIn Automation Hub"
$DesktopShortcut.Save()
Write-Host "Created Desktop Shortcut: $DesktopPath\Spread Love LinkedIn Portal.lnk"
