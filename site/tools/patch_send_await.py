"""Финальная проверка, замечание 4: «принято» — только после ответа сервера; маска не делает из иностранного номера +7.
Run из корня репо: py -3 -X utf8 site/tools/patch_send_await.py"""
import os
S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def rep(rel, old, new):
    p = os.path.join(S, rel); s = open(p, encoding='utf8').read()
    if new in s: return print('уже есть:', rel)
    assert s.count(old) == 1, (rel, old[:80], s.count(old))
    open(p, 'w', encoding='utf8', newline='\n').write(s.replace(old, new)); print('правка:', rel)


FOREIGN = "if (/^\\s*\\+\\s*[0-689]/.test({v}.value)) return;   // номер не российский — не переделываем в +7, проверка его отклонит"
# --- форма заявки
J11 = 'src/js/11-telefon-maska-i-proverka.js'
rep(J11, "  if (!d) { lp.value = ''; return; }", "  if (!d) { lp.value = ''; return; }\n  " + FOREIGN.format(v='lp'))
rep(J11, "  if (lp.value.replace(/\\D/g, '').length !== 11) { lp.closest('.f').classList.add('bad'); lp.focus(); return; }",
    "  if (!/^\\+7/.test(lp.value) || lp.value.replace(/\\D/g, '').length !== 11) { lp.closest('.f').classList.add('bad'); lp.focus(); return; }")
rep(J11, "  e.currentTarget.classList.add('sent');\n  PN.send({kind: 'quiz',",
    "  const form = e.currentTarget, btn = $('#qSend'); btn.disabled = true;\n  PN.send({kind: 'quiz',")
rep(J11, "name: $('#ln').value, phone: lp.value});",
    "name: $('#ln').value, phone: lp.value},\n    () => { btn.disabled = false; form.classList.add('sent'); }, () => { btn.disabled = false; });")
# --- «перезвоните»
J43 = 'src/js/43-panel-svyazi-v-menyu.js'
rep(J43, "let d = inp.value.replace(/\\D/g, ''); if (!d) { inp.value = ''; return; }",
    "let d = inp.value.replace(/\\D/g, ''); if (!d) { inp.value = ''; return; }\n    " + FOREIGN.format(v='inp'))
rep(J43, "    if (inp.value.replace(/\\D/g, '').length !== 11) { cb.classList.add('bad'); inp.focus(); return; }",
    "    if (!/^\\+7/.test(inp.value) || inp.value.replace(/\\D/g, '').length !== 11) { cb.classList.add('bad'); inp.focus(); return; }")
rep(J43, "    PN.send({kind: 'callback', phone: inp.value});\n", "    PN.send({kind: 'callback', phone: inp.value}, () => {\n")
rep(J43, "    toast(openNow ? 'Перезвоним в течение 30 секунд' : 'Перезвоним завтра в 9:00'); });\n",
    "    toast(openNow ? 'Перезвоним в течение 30 секунд' : 'Перезвоним завтра в 9:00'); }); });\n")
# --- запись на просмотр
J23 = 'src/js/23-zapis-na-prosmotr-v-demo-dom.js'
rep(J23, "      if (ip.value.replace(/\\D/g, '').length !== 11) { $('#bkF').classList.add('bad'); ip.focus(); return; }",
    "      if (!/^\\+7/.test(ip.value) || ip.value.replace(/\\D/g, '').length !== 11) { $('#bkF').classList.add('bad'); ip.focus(); return; }")
rep(J23, "phone: ip.value}); }\n      const d = days[day],", "phone: ip.value}, () => {\n      const d = days[day],")
rep(J23, "    });\n  };\n  $('#dlgT').textContent = kind;", "      }); }\n    });\n  };\n  $('#dlgT').textContent = kind;")
# --- слой данных: PN.send(поля, приУспехе, приОтказе); на витрине — сразу успех (синхронно, как в прототипе)
p = os.path.join(S, 'public/assets/js/data.js'); s = open(p, encoding='utf8').read()
a = s.find('  PN.send = fields => {'); b = s.find('  };\n', a) + len('  };\n')
assert a > 0 and b > a
s = s[:a] + """  PN.send = (fields, onOk = () => {}, onFail = () => {}) => {
    if (D.demo) { onOk({ok: true, demo: true}); say('Это демо-версия сайта: заявка никуда не отправлена'); return; }
    const hp = (document.getElementById('pnHp') || {}).value || '';
    fetch(PN.api + 'lead', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({...fields, consent: 1, hp, t0: T0})})
      .then(r => r.json())
      .catch(() => ({ok: false, message: 'Нет связи с сервером — позвоните нам: ' + ((D.settings || {}).phone || '')}))
      .then(r => { if (r.ok) onOk(r); else { window.toast && toast(r.message || 'Заявка не отправлена — позвоните нам'); onFail(r); } });
  };
""" + s[b:]
open(p, 'w', encoding='utf8', newline='\n').write(s); print('правка: data.js')
