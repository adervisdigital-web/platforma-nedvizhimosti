param([int]$x, [int]$y, [string]$text, [string]$prefix, [int]$shots = 3, [int]$wait = 8, [switch]$noenter)
# Клик в поле на открытой странице Chrome, вставка текста через буфер, Enter, снимки экрана с прокруткой.
Add-Type -AssemblyName System.Windows.Forms, System.Drawing
Add-Type @"
using System; using System.Runtime.InteropServices;
public class M2 { [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
[DllImport("user32.dll")] public static extern void mouse_event(int f, int dx, int dy, int d, int e);
[StructLayout(LayoutKind.Sequential)] public struct KI { public ushort vk; public ushort scan; public uint flags; public uint time; public IntPtr extra; }
[StructLayout(LayoutKind.Explicit, Size=40)] public struct INP { [FieldOffset(0)] public uint type; [FieldOffset(8)] public KI ki; }
[DllImport("user32.dll")] public static extern uint SendInput(uint n, INP[] i, int size);
public static void Type(string s) { foreach (char c in s) { var a = new INP[2];
 a[0].type = 1; a[0].ki.scan = c; a[0].ki.flags = 4; a[1].type = 1; a[1].ki.scan = c; a[1].ki.flags = 6;
 SendInput(2, a, System.Runtime.InteropServices.Marshal.SizeOf(typeof(INP))); System.Threading.Thread.Sleep(15); } } }
"@
$ws = New-Object -ComObject WScript.Shell; $null = $ws.AppActivate('Chrome'); Start-Sleep -Milliseconds 500
[M2]::SetCursorPos($x, $y); Start-Sleep -Milliseconds 200
[M2]::mouse_event(2, 0, 0, 0, 0); [M2]::mouse_event(4, 0, 0, 0, 0); Start-Sleep -Milliseconds 300
if ($text) {
  [System.Windows.Forms.SendKeys]::SendWait('{END}'); Start-Sleep -Milliseconds 100
  [System.Windows.Forms.SendKeys]::SendWait('{BS 80}'); Start-Sleep -Milliseconds 200; [M2]::Type($text); Start-Sleep -Milliseconds 300
}
if (-not $noenter) { [System.Windows.Forms.SendKeys]::SendWait('{ENTER}') }
Start-Sleep -Seconds $wait
[M2]::SetCursorPos(1400, 900)
$b = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
for ($i = 0; $i -lt $shots; $i++) {
  $bmp = New-Object System.Drawing.Bitmap $b.Width, $b.Height
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $g.CopyFromScreen($b.Location, [System.Drawing.Point]::Empty, $b.Size)
  $bmp.Save("$prefix`_$i.png", [System.Drawing.Imaging.ImageFormat]::Png)
  $g.Dispose(); $bmp.Dispose()
  [System.Windows.Forms.SendKeys]::SendWait('{PGDN}'); Start-Sleep -Milliseconds 1500
}
"done"
