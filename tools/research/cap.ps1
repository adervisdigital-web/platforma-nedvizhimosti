param([string]$url, [string]$prefix, [int]$shots = 4, [int]$wait = 9, [string]$key = '{PGDN}')
# Исследование референсов: открывает URL в Chrome пользователя (где выполнен вход в Behance),
# снимает экран, листает и снимает ещё. Только просмотр страниц, ничего не публикует.
Add-Type -AssemblyName System.Windows.Forms, System.Drawing
Start-Process "C:\Users\MSI\AppData\Local\Google\Chrome\Application\chrome.exe" $url
Start-Sleep -Seconds $wait
$ws = New-Object -ComObject WScript.Shell
$null = $ws.AppActivate('Chrome')
Start-Sleep -Milliseconds 700
$b = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
for ($i = 0; $i -lt $shots; $i++) {
  $bmp = New-Object System.Drawing.Bitmap $b.Width, $b.Height
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $g.CopyFromScreen($b.Location, [System.Drawing.Point]::Empty, $b.Size)
  $bmp.Save("$prefix`_$i.png", [System.Drawing.Imaging.ImageFormat]::Png)
  $g.Dispose(); $bmp.Dispose()
  [System.Windows.Forms.SendKeys]::SendWait($key)
  Start-Sleep -Milliseconds 1700
}
"done"
