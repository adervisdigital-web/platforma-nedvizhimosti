// поиск: статус, сканер, перекат счётчика
(() => {
  const n = $('#goN'), btn = $('.go3'), line = $('.sbox3 .sline'); let last = n.textContent, t;
  const tm = new Date(); tm.setMinutes(tm.getMinutes() - 7);
  const hhmm = `${String(tm.getHours()).padStart(2, '0')}:${String(tm.getMinutes()).padStart(2, '0')}`;
  function upd() {
    const v = +n.textContent || 0;
    $('#goL').textContent = plural(v, 'квартира', 'квартиры', 'квартир');
    $('#sStat').innerHTML = `<span class="lg">обновлено в ${hhmm} · </span>подходит <b>${v}</b> из 144<span class="lg"> проверенных</span>`;
    if (n.textContent !== last) { last = n.textContent;
      [n, btn, line].forEach(el => el.classList.remove('roll', 'sweep', 'scan')); void n.offsetWidth;
      n.classList.add('roll'); btn.classList.add('sweep'); line.classList.add('scan'); }
  }
  new MutationObserver(upd).observe(n, {childList: true, characterData: true, subtree: true});
  upd();
})();

