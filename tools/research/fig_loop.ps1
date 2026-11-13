param([string[]]$keys = @('leg', 'base', 'line', 'frame'), [switch]$dialogOpen)
# Для каждого знака: загрузить mk_<key>.jpg в изобразительный поиск Роспатента (масштаб страницы 67 %), нажать «Поиск»,
# снять верх и низ выдачи (z_<key>_top.png, z_<key>_bot.png). Фильтр МКТУ уже выставлен на странице.
$R = "C:\Users\MSI\Desktop\ПЛАТФОРМА -приложение\tools\research"
$T = "$env:TEMP\pn_be"
$first = $true
foreach ($k in $keys) {
  & "$R\shot_keys.ps1" -keys "{HOME}" -out "$T\tmp.png" -wait 1 | Out-Null
  if (-not ($first -and $dialogOpen)) { & "$R\type_search.ps1" -x 221 -y 406 -text "" -prefix "$T\x" -shots 0 -wait 3 -noenter | Out-Null }
  $first = $false
  & "$R\type_search.ps1" -x 1609 -y 1251 -text "$T\mk_$k.jpg" -prefix "$T\x" -shots 0 -wait 4 | Out-Null
  & "$R\type_search.ps1" -x 132 -y 507 -text "" -prefix "$T\x" -shots 0 -wait 18 -noenter | Out-Null
  & "$R\shot_keys.ps1" -keys "{HOME}" -out "$T\z_${k}_top.png" -wait 3 | Out-Null
  & "$R\shot_keys.ps1" -keys "{END}" -out "$T\z_${k}_bot.png" -wait 4 | Out-Null
  "$k done"
}
