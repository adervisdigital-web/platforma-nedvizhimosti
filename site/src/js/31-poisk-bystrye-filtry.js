// поиск: быстрые фильтры
const QF = {ready: it => !it.due, fin: it => it.fin !== 'Без отделки', fam: it => it.t === 'new', deal: it => it.disc || it.special};
const qfOn = () => $$('.qf [aria-pressed=true]').map(b => b.dataset.qf);
const _match = match;
match = (it, f) => _match(it, f) && qfOn().every(k => QF[k](it));
$$('.qf button').forEach(b => b.addEventListener('click', () => { b.setAttribute('aria-pressed', b.getAttribute('aria-pressed') !== 'true'); liveCount(); }));

