# Скриншот HTML через headless Chrome. usage: bash tools/shot.sh <file-url> <out.png> <W,H>
C="/c/Users/MSI/AppData/Local/Google/Chrome/Application/chrome.exe"
UD="${TEMP:-/tmp}/pn_chrome_profile"
rm -f "${2:?}"
for i in 1 2 3; do "$C" --headless=new --disable-gpu --user-data-dir="$UD" --hide-scrollbars --allow-file-access-from-files --virtual-time-budget=8000 --window-size=$3 --screenshot="$2" "$1" >/dev/null 2>&1; [ -f "$2" ] && break; sleep 2; done
