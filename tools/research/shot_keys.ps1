param([string]$keys = '', [string]$out, [int]$wait = 1)
# Отправляет клавиши в активный Chrome (необязательно) и снимает экран.
Add-Type -AssemblyName System.Windows.Forms, System.Drawing
$ws = New-Object -ComObject WScript.Shell; $null = $ws.AppActivate('Chrome'); Start-Sleep -Milliseconds 400
if ($keys) { [System.Windows.Forms.SendKeys]::SendWait($keys) }
Start-Sleep -Seconds $wait
$b = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$bmp = New-Object System.Drawing.Bitmap $b.Width, $b.Height
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.CopyFromScreen($b.Location, [System.Drawing.Point]::Empty, $b.Size)
$bmp.Save($out, [System.Drawing.Imaging.ImageFormat]::Png); $g.Dispose(); $bmp.Dispose()
"done"
