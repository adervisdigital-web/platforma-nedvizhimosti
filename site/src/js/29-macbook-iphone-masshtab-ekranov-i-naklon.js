// MacBook + iPhone: масштаб экранов и наклон за курсором
const devs = $('#devs');
function fitDevs() { const m = $('.mbp .vp'), p = $('.iph .vp'); if (!m) return; devs.style.setProperty('--ks', m.clientWidth / 1440); devs.style.setProperty('--kp', p.clientWidth / 390); }
addEventListener('resize', fitDevs); fitDevs(); new ResizeObserver(fitDevs).observe(devs);
if (!reduce && matchMedia('(hover:hover)').matches) {
  devs.addEventListener('mousemove', e => {
    const r = devs.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
    devs.classList.add('move');
    devs.style.setProperty('--ry', (x * 14).toFixed(2) + 'deg'); devs.style.setProperty('--rx', (-y * 10).toFixed(2) + 'deg');
    devs.style.setProperty('--px', (x * 22).toFixed(1) + 'px'); devs.style.setProperty('--py', (y * 16).toFixed(1) + 'px');
  });
  devs.addEventListener('mouseleave', () => { devs.classList.remove('move'); ['--rx', '--ry'].forEach(v => devs.style.setProperty(v, '0deg')); ['--px', '--py'].forEach(v => devs.style.setProperty(v, '0px')); });
}

