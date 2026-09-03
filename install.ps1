$ErrorActionPreference = 'Stop'
$ProjectDir = $PSScriptRoot
$Python = (Get-Command python).Source
$PythonW = Join-Path (Split-Path $Python) 'pythonw.exe'
if (-not (Test-Path -LiteralPath $PythonW)) { $PythonW = $Python }

& $Python -m pip install -r (Join-Path $ProjectDir 'requirements.txt')

$TokenBytes = New-Object byte[] 32
$TokenGenerator = [Security.Cryptography.RandomNumberGenerator]::Create()
$TokenGenerator.GetBytes($TokenBytes)
$TokenGenerator.Dispose()
$Token = [Convert]::ToBase64String($TokenBytes)
$Config = @{ token = $Token; port = 17843 } | ConvertTo-Json
Set-Content -LiteralPath (Join-Path $ProjectDir 'tubegrab.json') -Value $Config -Encoding UTF8
Set-Content -LiteralPath (Join-Path $ProjectDir 'extension\config.js') -Value "globalThis.TUBEGRAB_CONFIG = { port: 17843, token: '$Token' };" -Encoding UTF8

$StartupDir = [Environment]::GetFolderPath('Startup')
$ShortcutPath = Join-Path $StartupDir 'TubeGrab.lnk'
$Shell = New-Object -ComObject WScript.Shell
$Shortcut = $Shell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $PythonW
$Shortcut.Arguments = ('"{0}"' -f (Join-Path $ProjectDir 'downloader.py'))
$Shortcut.WorkingDirectory = $ProjectDir
$Shortcut.WindowStyle = 7
$Shortcut.Description = 'TubeGrab YouTube downloader'
$Shortcut.Save()

Start-Process -FilePath $PythonW -ArgumentList ('"{0}"' -f (Join-Path $ProjectDir 'downloader.py')) -WorkingDirectory $ProjectDir -WindowStyle Hidden

Write-Host ''
Write-Host 'TubeGrab installed. In Edge open edge://extensions, enable Developer mode,'
Write-Host "click Load unpacked, and select: $ProjectDir\extension"
