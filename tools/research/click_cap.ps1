param([string]$url, [int]$scrolls = 0, [int]$x, [int]$y, [string]$prefix, [int]$shots = 8, [int]$wait = 9)
# Открывает страницу поиска, листает $scrolls раз, кликает по превью проекта (x,y в пикселях экрана),
# затем снимает проект, пролистывая PageDown. Только просмотр.
Add-Type -AssemblyName System.Windows.Forms, System.Drawing
Add-Type @"
using System; using System.Runtime.InteropServices;
public class M { [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
[DllImport("user32.dll")] public static extern void mouse_event(int f, int dx, int dy, int d, int e); }
"@
Start-Process "C:\Users\MSI\AppData\Local\Google\Chrome\Application\chrome.exe" $url
Start-Sleep -Seconds $wait
$ws = New-Object -ComObject WScript.Shell; $null = $ws.AppActivate('Chrome'); Start-Sleep -Milliseconds 600
for ($i = 0; $i -lt $scrolls; $i++) { [System.Windows.Forms.SendKeys]::SendWait('{PGDN}'); Start-Sleep -Milliseconds 1500 }
[M]::SetCursorPos($x, $y); Start-Sleep -Milliseconds 300
[M]::mouse_event(2, 0, 0, 0, 0); [M]::mouse_event(4, 0, 0, 0, 0)
Start-Sleep -Seconds 7
[M]::SetCursorPos(2540, 700)
$b = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
for ($i = 0; $i -lt $shots; $i++) {
  $bmp = New-Object System.Drawing.Bitmap $b.Width, $b.Height
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $g.CopyFromScreen($b.Location, [System.Drawing.Point]::Empty, $b.Size)
  $bmp.Save("$prefix`_$i.png", [System.Drawing.Imaging.ImageFormat]::Png)
  $g.Dispose(); $bmp.Dispose()
  [System.Windows.Forms.SendKeys]::SendWait('{PGDN}'); Start-Sleep -Milliseconds 1600
}
[System.Windows.Forms.SendKeys]::SendWait('{ESC}')
"done"
