param([string[]]$keys = @('now', 'leg', 'base', 'line', 'frame'), [int]$steps = 5)
# Для каждого знака: загрузить mk_<key>.jpg, «Поиск», затем снимки HOME и PGDN×steps с паузой (ленивая подгрузка картинок).
$R = Split-Path -Parent $MyInvocation.MyCommand.Path
$T = "$env:TEMP\pn_be"
foreach ($k in $keys) {
  & "$R\shot_keys.ps1" -keys "{HOME}" -out "$T\tmp.png" -wait 1 | Out-Null
  & "$R\type_search.ps1" -x 221 -y 406 -text "" -prefix "$T\x" -shots 0 -wait 3 -noenter | Out-Null
  & "$R\type_search.ps1" -x 1609 -y 1251 -text "$T\mk_$k.jpg" -prefix "$T\x" -shots 0 -wait 4 | Out-Null
  & "$R\type_search.ps1" -x 132 -y 507 -text "" -prefix "$T\x" -shots 0 -wait 18 -noenter | Out-Null
  & "$R\shot_keys.ps1" -keys "{HOME}" -out "$T\s_${k}_0.png" -wait 4 | Out-Null
  for ($i = 1; $i -le $steps; $i++) { & "$R\shot_keys.ps1" -keys "{PGDN}" -out "$T\s_${k}_$i.png" -wait 5 | Out-Null }
  "$k done"
}
