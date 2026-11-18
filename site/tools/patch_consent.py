"""Разовая правка задачи 12: галочка согласия (152-ФЗ) в формах заявки, обратного звонка и записи на просмотр + отправка через PN.send.
Run из корня репо: py -3 -X utf8 site/tools/patch_consent.py"""
import os
S = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
R = os.path.dirname(S)


def rep(rel, old, new, root=S):
    p = os.path.join(root, rel); s = open(p, encoding='utf8').read()
    if new in s: return print('уже есть:', rel)
    assert s.count(old) == 1, (rel, old[:70], s.count(old))
    open(p, 'w', encoding='utf8', newline='\n').write(s.replace(old, new)); print('правка:', rel)


CNS = '<label class="cns" id="{id}L"><input type="checkbox" id="{id}"> <span>Согласен на <a href="privacy/" target="_blank">обработку персональных данных</a></span></label>'
rep('app/templates/sections/lead.php', '<small>Нажимая «Получить подборку», вы соглашаетесь на обработку персональных данных.</small>', CNS.format(id='lc'))
ARROW = '<button type="submit" aria-label="Заказать звонок"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h9M8.5 4.5L12 8l-3.5 3.5"/></svg></button></div>'
rep('app/templates/header.php', ARROW + '</form>', ARROW + CNS.format(id='hbCc') + '</form>')
rep('src/js/23-zapis-na-prosmotr-v-demo-dom.js', '      <button class="btn red" type="button" id="bkGo"', '      ' + CNS.format(id='bkC') + '\n      <button class="btn red" type="button" id="bkGo"')

PH = "if (lp.value.replace(/\\D/g, '').length !== 11) { lp.closest('.f').classList.add('bad'); lp.focus(); return; }"
rep('src/js/11-telefon-maska-i-proverka.js', "  " + PH + "\n  e.currentTarget.classList.add('sent');",
    "  " + PH + "\n  if (!$('#lc').checked) { $('#lcL').classList.add('bad'); $('#lc').focus(); return; }\n  e.currentTarget.classList.add('sent');\n"
    "  PN.send({kind: 'quiz', want: ($('#leadForm .ch [aria-pressed=true]') || {}).textContent || '', budget: $('#qbv').textContent,\n"
    "    area: $$('#qr [aria-pressed=true]').map(b => b.textContent).join(', '), name: $('#ln').value, phone: lp.value});")
CB = "    if (inp.value.replace(/\\D/g, '').length !== 11) { cb.classList.add('bad'); inp.focus(); return; }"
rep('src/js/43-panel-svyazi-v-menyu.js', CB,
    CB + "\n    if (!$('#hbCc').checked) { $('#hbCcL').classList.add('bad'); $('#hbCc').focus(); return; }\n    PN.send({kind: 'callback', phone: inp.value});")
BK = "      if (ip.value.replace(/\\D/g, '').length !== 11) { $('#bkF').classList.add('bad'); ip.focus(); return; }"
rep('src/js/23-zapis-na-prosmotr-v-demo-dom.js', BK,
    BK + "\n      if (!$('#bkC').checked) { $('#bkCL').classList.add('bad'); $('#bkC').focus(); return; }\n"
    "      { const d0 = days[day], p2 = n => String(n).padStart(2, '0');\n"
    "        PN.send({kind: 'viewing', want: kind, object_ref: subj, slot: `${d0.getFullYear()}-${p2(d0.getMonth() + 1)}-${p2(d0.getDate())} ${slot}`, phone: ip.value}); }")

p = os.path.join(S, 'public/assets/js/data.js'); s = open(p, encoding='utf8').read()
if 'PN.send' not in s:
    a = s.find('  // Витрина на GitHub Pages'); b = s.find('})();', a)
    s = s[:a] + """  // Отправка заявки: на витрине (demo) — никуда, честно говорим об этом; на сервере — POST api/lead.
  const T0 = Math.floor(Date.now() / 1000);
  const say = m => setTimeout(() => window.toast && toast(m), 1600);
  PN.send = fields => {
    if (D.demo) { say('Это демо-версия сайта: заявка никуда не отправлена'); return Promise.resolve({ok: true, demo: true}); }
    const hp = (document.getElementById('pnHp') || {}).value || '';
    return fetch(PN.api + 'lead', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({...fields, consent: 1, hp, t0: T0})})
      .then(r => r.json())
      .catch(() => ({ok: false, message: 'Нет связи с сервером — позвоните нам: ' + ((D.settings || {}).phone || '')}))
      .then(r => { if (!r.ok) say(r.message || 'Заявка не отправлена — позвоните нам'); return r; });
  };
""" + s[b:]
    open(p, 'w', encoding='utf8', newline='\n').write(s); print('правка: data.js')
rep('app/templates/layout.php', '<script id="pn-data" type="application/json">',
    '<input id="pnHp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px">\n<script id="pn-data" type="application/json">')
p = os.path.join(S, 'public/assets/css/site.css'); s = open(p, encoding='utf8').read()
if '.cns{' not in s:
    open(p, 'a', encoding='utf8', newline='\n').write("""
/* согласие на обработку персональных данных (152-ФЗ) */
.cns{display:flex;align-items:flex-start;gap:8px;font-size:13px;line-height:1.35;color:inherit;opacity:.8;margin:10px 0;cursor:pointer;text-align:left}
.cns input{width:18px;height:18px;min-height:0;margin:0;flex:none;accent-color:var(--red-ui)}
.cns a{color:inherit;text-decoration:underline;text-underline-offset:2px}
.cns.bad{opacity:1;color:var(--red-ui)}
"""); print('правка: site.css')
rep('tools/test_site.py', "if($('#qSend')){$('#leadForm').requestSubmit();", "if($('#qSend')){if($('#lc'))$('#lc').checked=true;$('#leadForm').requestSubmit();", root=R)
rep('tools/test_site.py', "$('#bkP').dispatchEvent(new Event('input'));$('#bkGo').click();",
    "$('#bkP').dispatchEvent(new Event('input'));if($('#bkC'))$('#bkC').checked=true;$('#bkGo').click();", root=R)
