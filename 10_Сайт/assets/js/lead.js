// Окно заявки: кнопки [data-lead="quiz|viewing"] на любой странице открывают форму поверх страницы, а не уводят к форме внизу.
// data-title — заголовок, data-want — что нужно (уходит в заявку), data-ref — объект, data-calc — приложить расчёт калькулятора, data-filters — фильтры каталога.
(() => {
  const $ = (q, r = document) => r.querySelector(q), $$ = (q, r = document) => [...r.querySelectorAll(q)];
  // ---- заявка прямо на странице: кнопки [data-lead] (просмотр, смета, подбор) открывают окно, а не уводят на главную.
  // К заявке прикладывается контекст: объект (data-ref), пожелание (data-want), расчёт калькулятора (data-calc), фильтры каталога (data-filters).
  const ekbHour = () => (new Date().getUTCHours() + 5) % 24;   // Екатеринбург, UTC+5
  const maskPhone = el => el.addEventListener('input', () => { let d = el.value.replace(/\D/g, ''); if (!d) { el.value = ''; return; }
    if (/^\s*\+\s*[0-689]/.test(el.value)) return;
    if (d[0] === '8') d = '7' + d.slice(1); if (d[0] !== '7') d = '7' + d; const p = d.slice(1, 11);
    el.value = '+7' + (p.length ? ' (' + p.slice(0, 3) : '') + (p.length > 3 ? ') ' + p.slice(3, 6) : '') + (p.length > 6 ? '-' + p.slice(6, 8) : '') + (p.length > 8 ? '-' + p.slice(8, 10) : ''); });
  const OUT = {down: 'взнос', term: 'срок', pay: 'платёж', loan: 'кредит', area: 'площадь', sum: 'итого', ppm: 'за м²', rest: 'остаток'};
  const clean = t => String(t || '').replace(/\s+/g, ' ').trim();
  const calcText = btn => {
    const c = btn.closest('[data-mort], [data-ren], [data-inst]') || (btn.closest('.calc') ? null : $('[data-mort], [data-ren], [data-inst]'));
    if (c) {
      const parts = $$('[aria-checked="true"], [aria-pressed="true"][data-k]', c).map(b => b.dataset.k ? 'детей: ' + b.textContent.trim() : clean(b.textContent));
      const price = $('[data-i="price"]', c); if (price && price.value) parts.push('цена ' + price.value);
      $$('[data-o]', c).forEach(o => { if (OUT[o.dataset.o] && o.textContent.trim()) parts.push(OUT[o.dataset.o] + ' ' + o.textContent.trim()); });
      return parts.join(', ');
    }
    const m = btn.closest('.calc'); if (!m) return '';                                      // калькуляторы главной
    const parts = [];
    $$('.rng label', m).forEach(l => { const v = $('b', l); if (v && v.textContent.trim()) parts.push(clean(l.firstChild.textContent).toLowerCase() + ' ' + clean(v.textContent)); });
    $$('[aria-pressed="true"]', m).forEach(b => { if (!b.closest('.cprog')) parts.push((b.dataset.k ? 'детей: ' : '') + clean(b.childNodes[0] ? b.childNodes[0].textContent : b.textContent)); });
    const pay = $('.pay', m); if (pay && pay.textContent.trim() !== '—') parts.push('итог ' + clean(pay.textContent));
    return parts.join(', ').slice(0, 170);
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

})();
