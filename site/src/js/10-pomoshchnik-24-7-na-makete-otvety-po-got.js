// помощник 24/7 (на макете — ответы по готовым темам; на сайте — ИИ + своя CRM заказчика)
const FAQ = PN.faq();
const QUICK = PN.quick();
const log = $('#chatLog');
function say(t, me) { const p = document.createElement('p'); if (me) { p.className = 'me'; p.textContent = t; } else p.innerHTML = t; log.appendChild(p); log.scrollTop = log.scrollHeight; return p; }
function ask(q) {
  say(q, 1); const t = say('печатает…'); t.className = 'typing';
  const hit = FAQ.find(([re]) => re.test(q));
  setTimeout(() => { t.className = ''; t.innerHTML = hit ? hit[1] : 'Передам вопрос менеджеру — он свяжется с вами. Оставьте телефон в <a href="#lead" data-lead="quiz" data-title="Перезвоним" data-want="Вопрос из чата">форме</a> или позвоните: <a href="tel:+79655002918">+7 965 500-29-18</a>.'; log.scrollTop = log.scrollHeight; }, reduce ? 0 : 700);
}
$('#chatQ').innerHTML = QUICK.map(q => `<button type="button">${q}</button>`).join('');
$$('#chatQ button').forEach(b => b.addEventListener('click', () => ask(b.textContent)));
$('#chatForm').addEventListener('submit', e => { e.preventDefault(); const v = $('#chatIn').value.trim(); if (v) { ask(v); $('#chatIn').value = ''; } });
let greeted = false;
function openChat(o) {
  $('#chat').hidden = !o; $('#chatFab').hidden = o; $('#chatFab').setAttribute('aria-expanded', o);
  if (o && !greeted) { say('Здравствуйте! Я помощник Платформы и отвечаю круглосуточно. Спросите про квартиры, ипотеку, ремонт или дома.'); greeted = true; }
  if (o && matchMedia('(hover:hover)').matches) $('#chatIn').focus();
  const mob = innerWidth <= 800; document.documentElement.classList.toggle('chat-lock', o && mob); if (o && mob) fitChat();
}
function fitChat() { const v = window.visualViewport, c = $('#chat'); if (!v || innerWidth > 800 || c.hidden) { c.style.height = c.style.top = ''; return; }
  c.style.top = v.offsetTop + 'px'; c.style.height = v.height + 'px'; const lg = $('#chatLog'); lg.scrollTop = lg.scrollHeight; }
if (window.visualViewport) { visualViewport.addEventListener('resize', fitChat); visualViewport.addEventListener('scroll', fitChat); }
$('#chatFab').addEventListener('click', () => openChat(true));
$('#chatX').addEventListener('click', () => openChat(false));
$$('[data-chat]').forEach(a => a.addEventListener('click', e => { e.preventDefault(); openChat(true); }));
document.addEventListener('keydown', e => { if (e.key === 'Escape' && !$('#chat').hidden) openChat(false); });

