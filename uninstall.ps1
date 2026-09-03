$ErrorActionPreference = 'SilentlyContinue'
$ShortcutPath = Join-Path ([Environment]::GetFolderPath('Startup')) 'TubeGrab.lnk'
Remove-Item -LiteralPath $ShortcutPath -Force
# Also clean up the scheduled-task version used by early builds, if it exists.
Stop-ScheduledTask -TaskName 'FrogGrab YouTube Helper'
Unregister-ScheduledTask -TaskName 'FrogGrab YouTube Helper' -Confirm:$false
Get-CimInstance Win32_Process -Filter "Name = 'pythonw.exe'" | Where-Object {
    $_.CommandLine -like '*ytdownloader*downloader.py*'
} | Invoke-CimMethod -MethodName Terminate | Out-Null
Remove-Item -LiteralPath (Join-Path ([Environment]::GetFolderPath('Startup')) 'FrogGrab.lnk') -Force
Remove-Item -LiteralPath (Join-Path ([Environment]::GetFolderPath('Startup')) 'Grabber.lnk') -Force
Write-Host 'TubeGrab backend removed. Remove the extension from edge://extensions to finish.'
