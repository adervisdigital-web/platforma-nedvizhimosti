// заявка: точки у курсора
(() => { const lead = $('#lead'), lit = $('.lead .dotgrid.lit'); if (!lit || !matchMedia('(hover:hover)').matches) return;
  lead.addEventListener('mousemove', e => { const r = lit.getBoundingClientRect(); lit.style.setProperty('--mx', e.clientX - r.left + 'px'); lit.style.setProperty('--my', e.clientY - r.top + 'px'); });
  lead.addEventListener('mouseleave', () => { lit.style.setProperty('--mx', '-999px'); }); })();

