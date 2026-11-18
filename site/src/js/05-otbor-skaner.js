// отбор: сканер
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const SF = $('#sfield'), SC = 16, SN = SC * 9;
SF.insertAdjacentHTML('beforeend', Array.from({length: SN}, (_, i) => `<i class="${i % SC >= 12 ? 'x12' : ''}"></i>`).join(''));
const sdots = $$('#sfield i');
let scanT = [], scanRun = 0;
function scanStop() { scanT.forEach(clearTimeout); scanT = []; scanRun++; }
function scanStart() {
  if (window.__noScan) return;
  scanStop(); const run = scanRun, cols = () => innerWidth <= 1000 ? 12 : SC;
  const vis = () => sdots.filter((d, i) => i % SC < cols());
  const lis = $$('#clist li'), DUR = 1500, GAP = 450;
  sdots.forEach(d => d.classList.remove('off', 'pass', 'hit')); lis.forEach(l => l.classList.remove('act', 'pass'));
  let alive = vis(); const total = alive.length;
  $('#sIn').textContent = total; $('#sOut').textContent = total; $('#sOutL').textContent = 'проходят проверку';
  const finalN = 6, keep = new Set(alive.slice().sort(() => Math.random() - .5).slice(0, finalN));
  if (reduce) { alive.forEach(d => d.classList.add(keep.has(d) ? 'pass' : 'off')); lis.forEach(l => l.classList.add('pass')); $('#sOut').textContent = finalN; $('#sOutL').textContent = 'прошли все проверки'; return; }
  const beam = $('#beam'), W = SF.clientWidth;
  lis.forEach((li, s) => {
    scanT.push(setTimeout(() => {
      if (run !== scanRun) return;
      lis.forEach((l, k) => { l.classList.toggle('act', k === s); if (k < s) l.classList.add('pass'); });
      beam.classList.remove('go'); void beam.offsetWidth; beam.style.setProperty('--w', W + 'px'); beam.style.setProperty('--dur', DUR + 'ms'); beam.classList.add('go');
      li.style.setProperty('--dur', DUR + 'ms');
      const left = alive.filter(d => !keep.has(d)), drop = s === lis.length - 1 ? left : left.sort(() => Math.random() - .5).slice(0, Math.round(left.length * .45));
      drop.forEach(d => { const x = (d.offsetLeft + 5) / W; scanT.push(setTimeout(() => { if (run !== scanRun) return; d.classList.add('hit'); setTimeout(() => { d.classList.remove('hit'); d.classList.add('off'); }, 140); $('#sOut').textContent = +$('#sOut').textContent - 1; }, x * DUR)); });
      alive = alive.filter(d => !drop.includes(d));
    }, s * (DUR + GAP)));
  });
  scanT.push(setTimeout(() => { if (run !== scanRun) return; lis.forEach(l => { l.classList.remove('act'); l.classList.add('pass'); }); keep.forEach(d => d.classList.add('pass')); $('#sOut').textContent = finalN; $('#sOutL').textContent = 'прошли все проверки'; }, lis.length * (DUR + GAP)));
  scanT.push(setTimeout(() => { if (run === scanRun) scanStart(); }, lis.length * (DUR + GAP) + 4500));
}
new IntersectionObserver(es => { es[0].isIntersecting ? scanStart() : scanStop(); }, {threshold: .35}).observe($('#scan'));

