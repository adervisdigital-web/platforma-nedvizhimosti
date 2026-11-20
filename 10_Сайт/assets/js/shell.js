// Каркас подстраниц — как на главной, но без её сценариев: шапка (тень, точка под разделом, связь и «перезвоним»),
// полоса прокрутки, «Ставим точку.» в подвале, мобильное меню и капсула снизу, помощник в чате, счётчики «Избранное» и «Сравнить».
// Данные — из data.js (#pn-data: faq, quick, settings, demo, api). Повторяет модули src/js 10, 12, 18, 20, 22, 30, 43, 46.
(() => {
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const html = document.documentElement;

  // ---- уведомление
  // window.toast без проверки «уже есть»: элемент с id="toast" сам попадает в window.toast, и тогда функции бы не было
  const toast = t => { const el = $('#toast'); if (!el) return; el.textContent = t; el.classList.add('on'); clearTimeout(toast.h); toast.h = setTimeout(() => el.classList.remove('on'), 3200); };
  window.toast = toast;

  // ---- шапка: тень, полоса прокрутки, кнопка чата, точка в подвале
  const hdr = $('header'), fab = $('#chatFab'), prog = $('#prog');
  const onScroll = () => {
    const y = scrollY, h = html.scrollHeight - innerHeight, k = h > 0 ? Math.min(1, y / h) : 0;
    // на подстраницах шапка — всегда плавающая капсула (класс sc в шаблоне), без прыжка контента
    if (prog) { prog.style.setProperty('--s', k); prog.classList.toggle('end', k > .995); }
    if (fab) { fab.classList.add('show'); fab.classList.toggle('mini', y > 600); }
  };
  // первый экран с фото: шапка — тёмное стекло, пока фото под ней (как на главной)
  const sxh = $('.sx-hero');
  const heroUpd = () => { if (sxh && hdr) hdr.classList.toggle('ontop', scrollY < sxh.offsetHeight - 90); };
  addEventListener('scroll', heroUpd, {passive: true}); heroUpd();
  addEventListener('scroll', onScroll, {passive: true}); addEventListener('resize', onScroll); onScroll();
  const fbig = $('.fbig');
  if (fbig) new IntersectionObserver((es, o) => { if (es[0].isIntersecting) { fbig.classList.add('in'); o.disconnect(); } }, {threshold: .6}).observe(fbig);

  // ---- точка под текущим разделом меню, скользит за курсором
  const nav = $('nav.main');
  if (nav) {
    const ndTo = a => { if (!a) { nav.style.setProperty('--no', 0); return; } nav.style.setProperty('--nx', (a.offsetLeft + a.offsetWidth / 2 - 3) + 'px'); nav.style.setProperty('--no', 1); };
    const ndActive = () => ndTo($('nav.main a.on'));
    $$('a', nav).forEach(a => a.addEventListener('mouseenter', () => ndTo(a)));
    nav.addEventListener('mouseleave', ndActive);
    setTimeout(ndActive, 200); addEventListener('resize', ndActive);
    document.fonts && document.fonts.ready.then(ndActive);
  }

  // ---- связь: часы Екатеринбурга, меню телефона, «перезвоним за 30 секунд»
  const ph = $('#hbPh'), pop = $('#hbPop'), cb = $('#hbCb'), inp = $('#hbTel');
  const ekb = () => { const d = new Date(), u = d.getTime() + d.getTimezoneOffset() * 6e4; return new Date(u + 5 * 36e5); };
  if (ph && pop) {
    const clock = () => { const t = ekb(), h = t.getHours(), open = h >= 9 && h < 21;
      $('#hbClk').textContent = String(h).padStart(2, '0') + ':' + String(t.getMinutes()).padStart(2, '0');
      $('#hbStatus').textContent = open ? 'на связи' : 'перезвоним с 9:00'; $('#hbDot').classList.toggle('off', !open);
      if (!cb.classList.contains('sent')) $('#hbCbNote').textContent = open ? 'Оставьте номер — менеджер наберёт сам' : 'Сейчас офис закрыт — позвоним в 9:00'; };
    clock(); setInterval(clock, 15000);
    const open = o => { pop.hidden = !o; ph.setAttribute('aria-expanded', o); if (o) setTimeout(() => inp.focus(), 50); };
    ph.addEventListener('click', e => { e.stopPropagation(); open(pop.hidden); });
    pop.addEventListener('click', e => e.stopPropagation());
    document.addEventListener('click', () => open(false));
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && !pop.hidden) { open(false); ph.focus(); } });
    $$('[data-chat]', pop).forEach(b => b.addEventListener('click', () => open(false)));
    inp.addEventListener('input', () => { cb.classList.remove('bad'); let d = inp.value.replace(/\D/g, ''); if (!d) { inp.value = ''; return; }
      if (/^\s*\+\s*[0-689]/.test(inp.value)) return;
      if (d[0] === '8') d = '7' + d.slice(1); if (d[0] !== '7') d = '7' + d; const p = d.slice(1, 11);
      inp.value = '+7' + (p.length ? ' (' + p.slice(0, 3) : '') + (p.length > 3 ? ') ' + p.slice(3, 6) : '') + (p.length > 6 ? '-' + p.slice(6, 8) : '') + (p.length > 8 ? '-' + p.slice(8, 10) : ''); });
    $('#hbCc').addEventListener('change', () => $('#hbCcL').classList.remove('bad'));
    cb.addEventListener('submit', e => { e.preventDefault();
      if (!/^\+7/.test(inp.value) || inp.value.replace(/\D/g, '').length !== 11) { cb.classList.add('bad'); inp.focus(); return; }
      if (!$('#hbCc').checked) { $('#hbCcL').classList.add('bad'); $('#hbCc').focus(); return; }
      PN.send({kind: 'callback', phone: inp.value}, () => {
        const h = ekb().getHours(), openNow = h >= 9 && h < 21; cb.classList.add('sent');
        $('#hbCbNote').textContent = openNow ? `Звоним на ${inp.value} — держите телефон рядом` : `Позвоним на ${inp.value} завтра в 9:00`;
        cb.querySelector('b').textContent = openNow ? 'Уже набираем' : 'Заявка принята';
        toast(openNow ? 'Перезвоним в течение 30 секунд' : 'Перезвоним завтра в 9:00'); }); });
  }

  // ---- «Избранное» и «Сравнить»: те же списки, что на главной (localStorage pn_fav / pn_cmp, номера квартир — id в базе, как в PN.items());
  // кнопки на карточках каталога — [data-fav] / [data-cmp]; список открывается на главной
  const read = k => { try { return JSON.parse(localStorage.getItem(k) || '[]').map(Number); } catch (e) { return []; } };
  const write = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} };
  const count = k => read(k).length;
  const counts = () => [['#favCnt', 'pn_fav'], ['#cmpCnt', 'pn_cmp']].forEach(([c, k]) => { const n = count(k), el = $(c); if (el) { el.textContent = n; el.classList.toggle('on', n > 0); } });
  const marks = () => { const f = read('pn_fav'), c = read('pn_cmp');
    $$('[data-fav]').forEach(b => b.setAttribute('aria-pressed', f.includes(+b.dataset.fav)));
    $$('[data-cmp]').forEach(b => b.setAttribute('aria-pressed', c.includes(+b.dataset.cmp))); };
  counts(); marks();
  addEventListener('storage', e => { if (e.key === 'pn_fav' || e.key === 'pn_cmp') { counts(); marks(); } });   // изменили в другой вкладке
  document.addEventListener('pn:cards', marks);                                                                     // каталог догрузил карточки
  document.addEventListener('click', e => {
    const b = e.target.closest('[data-fav], [data-cmp]'); if (!b) return;
    e.preventDefault(); e.stopPropagation();
    const op = b.dataset.fav !== undefined ? 'fav' : 'cmp', k = 'pn_' + op, id = +(b.dataset.fav ?? b.dataset.cmp), v = read(k);
    if (id < 0) return;
    if (!v.includes(id) && op === 'cmp' && v.length >= 4) { toast('Сравнить можно до 4 квартир — уберите одну из сравнения'); return; }
    const on = !v.includes(id); write(k, on ? v.concat(id) : v.filter(x => x !== id)); counts(); marks();
    if (on) toast(op === 'fav' ? 'Добавили в избранное — смотрите в шапке' : `В сравнении: ${count(k)}. Откройте «Сравнить» в шапке`);
  });
  [['#favCnt', 'pn_fav', '#favBtn', 'fav'], ['#cmpCnt', 'pn_cmp', '#cmpBtn', 'cmp']].forEach(([c, k, b, op]) => {
    const btn = $(b); btn && btn.addEventListener('click', () => {
      if (!count(k)) { toast(op === 'fav' ? 'Пока пусто — нажмите сердечко на карточке квартиры' : 'Добавьте квартиры к сравнению — кнопка на фото в карточке'); return; }
      location.href = './?open=' + op; });
  });

  // ---- заявка прямо на странице: кнопки [data-lead] (просмотр, смета, подбор) открывают окно, а не уводят на главную.
  // К заявке прикладывается контекст: объект (data-ref), пожелание (data-want), расчёт калькулятора (data-calc), фильтры каталога (data-filters).
  const ekbHour = () => ekb().getHours();
  const maskPhone = el => el.addEventListener('input', () => { let d = el.value.replace(/\D/g, ''); if (!d) { el.value = ''; return; }
    if (/^\s*\+\s*[0-689]/.test(el.value)) return;
    if (d[0] === '8') d = '7' + d.slice(1); if (d[0] !== '7') d = '7' + d; const p = d.slice(1, 11);
    el.value = '+7' + (p.length ? ' (' + p.slice(0, 3) : '') + (p.length > 3 ? ') ' + p.slice(3, 6) : '') + (p.length > 6 ? '-' + p.slice(6, 8) : '') + (p.length > 8 ? '-' + p.slice(8, 10) : ''); });
  const OUT = {down: 'взнос', term: 'срок', pay: 'платёж', loan: 'кредит', area: 'площадь', sum: 'итого', ppm: 'за м²', rest: 'остаток'};
  const calcText = btn => {
    const c = btn.closest('[data-mort], [data-ren], [data-inst]') || $('[data-mort], [data-ren], [data-inst]'); if (!c) return '';
    const parts = $$('[aria-checked="true"], [aria-pressed="true"][data-k]', c).map(b => b.dataset.k ? 'детей: ' + b.textContent.trim() : b.textContent.trim().replace(/\s+/g, ' '));
    const price = $('[data-i="price"]', c); if (price && price.value) parts.push('цена ' + price.value);
    $$('[data-o]', c).forEach(o => { if (OUT[o.dataset.o] && o.textContent.trim()) parts.push(OUT[o.dataset.o] + ' ' + o.textContent.trim()); });
    return parts.join(', ');
  };
  const filterText = () => { const f = $('[data-ct-form]'); if (!f) return ''; const p = [];
    for (const el of f.elements) { if (!el.name) continue;
      if (el.type === 'checkbox') { if (el.checked) p.push(el.parentElement.textContent.trim()); }
      else if (el.value.trim()) p.push((el.closest('label') ? el.closest('label').firstElementChild.textContent.trim() + ' ' : '') + (el.tagName === 'SELECT' ? el.selectedOptions[0].textContent : el.value.trim())); }
    return p.join(', '); };
  let lq = null;
  const lqBuild = () => {
    lq = document.createElement('dialog'); lq.className = 'lq'; lq.setAttribute('aria-labelledby', 'lqT');
    lq.innerHTML = `<form class="lq-f" novalidate>
      <button type="button" class="lq-x" aria-label="Закрыть">×</button>
      <p class="lq-r">[<i></i>Заявка ]</p><h2 id="lqT"></h2><p class="lq-what" id="lqW"></p>
      <div class="lq-when" hidden><span>Когда удобно посмотреть</span><div role="radiogroup" aria-label="Когда удобно посмотреть">${['Сегодня', 'Завтра', 'В выходные', 'Обсудим по телефону'].map((t, i) => `<button type="button" role="radio" aria-checked="${i === 3}">${t}</button>`).join('')}</div></div>
      <label class="lq-l"><span>Как к вам обращаться</span><input name="name" autocomplete="given-name" maxlength="80" placeholder="Имя"></label>
      <label class="lq-l"><span>Телефон</span><input name="phone" type="tel" autocomplete="tel" placeholder="+7 (___) ___-__-__" required></label>
      <label class="cns lq-c"><input type="checkbox" name="cc"> <span>Согласен на <a href="privacy/" target="_blank">обработку персональных данных</a></span></label>
      <button type="submit" class="pg-btn red lq-s">Отправить заявку</button>
      <p class="lq-n" id="lqN"></p>
      <div class="lq-ok" hidden><b>Заявка принята<i></i></b><p id="lqOk"></p><button type="button" class="pg-btn lq-done">Хорошо</button></div>
    </form>`;
    document.body.append(lq);
    const f = $('form', lq), ph = f.elements.phone;
    maskPhone(ph);
    $('.lq-x', lq).addEventListener('click', () => lq.close());
    $('.lq-done', lq).addEventListener('click', () => lq.close());
    lq.addEventListener('click', e => { if (e.target === lq) lq.close(); });
    $$('.lq-when [role=radio]', lq).forEach(b => b.addEventListener('click', () => $$('.lq-when [role=radio]', lq).forEach(x => x.setAttribute('aria-checked', x === b))));
    f.elements.cc.addEventListener('change', () => f.querySelector('.lq-c').classList.remove('bad'));
    ph.addEventListener('input', () => ph.closest('.lq-l').classList.remove('bad'));
    f.addEventListener('submit', e => { e.preventDefault();
      if (!/^\+7/.test(ph.value) || ph.value.replace(/\D/g, '').length !== 11) { ph.closest('.lq-l').classList.add('bad'); $('#lqN').textContent = 'Проверьте номер: нужен российский номер, 10 цифр после +7'; ph.focus(); return; }
      if (!f.elements.cc.checked) { f.querySelector('.lq-c').classList.add('bad'); $('#lqN').textContent = 'Отметьте согласие на обработку персональных данных'; f.elements.cc.focus(); return; }
      const d = lq._ctx, sb = $('.lq-s', lq); sb.disabled = true; $('#lqN').textContent = 'Отправляем…';
      const slot = d.kind === 'viewing' ? ($('.lq-when [aria-checked="true"]', lq) || {}).textContent || '' : '';
      PN.send({kind: d.kind, phone: ph.value, name: f.elements.name.value.trim(), want: d.want, object_ref: d.ref, slot}, r => {
        const open = ekbHour() >= 9 && ekbHour() < 21;
        $('#lqOk').textContent = (r && r.demo) ? 'Это демо-версия сайта: заявка никуда не отправлена.' : (open ? 'Менеджер перезвонит на ' + ph.value + ' в рабочее время, обычно в течение получаса.' : 'Сейчас офис закрыт — перезвоним на ' + ph.value + ' завтра с 9:00.');
        $('.lq-ok', lq).hidden = false; f.classList.add('is-sent'); $('#lqN').textContent = ''; sb.disabled = false; $('.lq-done', lq).focus();
      }, r => { sb.disabled = false; $('#lqN').textContent = (r && r.message) || 'Заявка не отправилась — позвоните нам: +7 965 500-29-18'; });
    });
  };
  document.addEventListener('click', e => {
    const b = e.target.closest('[data-lead]'); if (!b || !window.PN || !PN.send || typeof HTMLDialogElement !== 'function') return;
    e.preventDefault();
    if (!lq) lqBuild();
    const f = $('form', lq); f.classList.remove('is-sent'); $('.lq-ok', lq).hidden = true; $('#lqN').textContent = '';
    let want = b.dataset.want || '';
    if (b.hasAttribute('data-calc')) { const c = calcText(b); if (c) want += ' — расчёт: ' + c; }
    if (b.hasAttribute('data-filters')) { const c = filterText(); if (c) want += ' — фильтры: ' + c; }
    lq._ctx = {kind: b.dataset.lead === 'viewing' ? 'viewing' : 'quiz', want: want.slice(0, 200), ref: b.dataset.ref || location.pathname};
    $('#lqT').textContent = b.dataset.title || 'Заявка';
    $('#lqW').textContent = (b.dataset.want || '').replace(/^[^:]+:\s*/, '') || '';
    $('#lqW').hidden = !$('#lqW').textContent;
    $('.lq-when', lq).hidden = lq._ctx.kind !== 'viewing';
    lq.showModal(); setTimeout(() => (f.elements.phone.value ? f.elements.name : f.elements.phone).focus(), 30);
  });

  // ---- мобильное меню и капсула снизу
  const tb = $('#tabbar'), mn = $('#mnav'), mb = $('#mnBtn');
  if (tb) { let lastY = scrollY;
    addEventListener('scroll', () => { const y = scrollY, d = y - lastY; if (Math.abs(d) > 6) { tb.classList.toggle('hide', d > 0 && y > 300); lastY = y; } }, {passive: true}); }
  if (mn && mb) {
    const openMn = o => { mn.hidden = !o; mb.setAttribute('aria-expanded', o); html.classList.toggle('mn-lock', o);
      if (o) { const st = $('#hbStatus'); $('#mnSt').textContent = st ? st.textContent : 'на связи'; $('#mnX').focus(); } else mb.focus(); };
    mb.addEventListener('click', () => openMn(true)); $('#mnX').addEventListener('click', () => openMn(false));
    $$('.mn-l a, .mn-c [data-chat], .mn-cab', mn).forEach(a => a.addEventListener('click', () => openMn(false)));
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && !mn.hidden) openMn(false); });
  }

  // ---- помощник 24/7 (ответы по готовым темам, как на главной)
  const chat = $('#chat'), log = $('#chatLog');
  if (chat && log && window.PN) {
    const FAQ = PN.faq(), QUICK = PN.quick(); let greeted = false;
    const say = (t, me) => { const p = document.createElement('p'); if (me) { p.className = 'me'; p.textContent = t; } else p.innerHTML = t; log.appendChild(p); log.scrollTop = log.scrollHeight; return p; };
    const ask = q => { say(q, 1); const t = say('печатает…'); t.className = 'typing';
      const hit = FAQ.find(([re]) => re.test(q));
      setTimeout(() => { t.className = ''; t.innerHTML = hit ? hit[1] : 'Передам вопрос менеджеру — он свяжется с вами. Оставьте телефон в <a href="./#lead">форме</a> или позвоните: <a href="tel:+79655002918">+7 965 500-29-18</a>.'; log.scrollTop = log.scrollHeight; }, matchMedia('(prefers-reduced-motion: reduce)').matches ? 0 : 700); };
    $('#chatQ').innerHTML = QUICK.map(q => `<button type="button">${q}</button>`).join('');
    $$('#chatQ button').forEach(b => b.addEventListener('click', () => ask(b.textContent)));
    $('#chatForm').addEventListener('submit', e => { e.preventDefault(); const v = $('#chatIn').value.trim(); if (v) { ask(v); $('#chatIn').value = ''; } });
    const fitChat = () => { const v = window.visualViewport; if (!v || innerWidth > 800 || chat.hidden) { chat.style.height = chat.style.top = ''; return; }
      chat.style.top = v.offsetTop + 'px'; chat.style.height = v.height + 'px'; log.scrollTop = log.scrollHeight; };
    if (window.visualViewport) { visualViewport.addEventListener('resize', fitChat); visualViewport.addEventListener('scroll', fitChat); }
    window.openChat = o => {
      chat.hidden = !o; fab && (fab.hidden = o, fab.setAttribute('aria-expanded', o));
      if (o && !greeted) { say('Здравствуйте! Я помощник Платформы и отвечаю круглосуточно. Спросите про квартиры, ипотеку, ремонт или дома.'); greeted = true; }
      if (o && matchMedia('(hover:hover)').matches) $('#chatIn').focus();
      const mob = innerWidth <= 800; html.classList.toggle('chat-lock', o && mob); if (o && mob) fitChat();
    };
    fab && fab.addEventListener('click', () => openChat(true));
    $('#chatX').addEventListener('click', () => openChat(false));
    $$('[data-chat]').forEach(a => a.addEventListener('click', e => { e.preventDefault(); openChat(true); }));
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && !chat.hidden) openChat(false); });
    // мессенджеры: ников пока нет — ведём в чат
    $$('[data-soon]').forEach(a => a.addEventListener('click', e => { e.preventDefault(); openChat(true); toast(a.dataset.find ? `В ${a.dataset.soon} найдите «${a.dataset.find}» — или пишите здесь, ответим сразу` : `${a.dataset.soon} подключим к запуску — пока пишите здесь, ответим сразу`); }));
  }
})();
