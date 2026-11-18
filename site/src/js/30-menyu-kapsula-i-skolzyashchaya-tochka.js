// меню: капсула и скользящая точка
const hdrEl = $('header'), nav = $('nav.main'), nd = $('nav.main .nd');
function ndTo(a) { if (!a) { nav.style.setProperty('--no', 0); return; } nav.style.setProperty('--nx', (a.offsetLeft + a.offsetWidth / 2 - 3) + 'px'); nav.style.setProperty('--no', 1); }
const ndActive = () => ndTo($('nav.main a.on'));
$$('nav.main a').forEach(a => a.addEventListener('mouseenter', () => ndTo(a)));
nav.addEventListener('mouseleave', ndActive);
new MutationObserver(ndActive).observe(nav, {subtree: true, attributes: true, attributeFilter: ['class']});
setTimeout(ndActive, 300); addEventListener('resize', ndActive);
function hdrUpd() { hdrEl.classList.toggle('ontop', scrollY < $('.hero').offsetHeight - 90); }
addEventListener('scroll', hdrUpd, {passive: true}); hdrUpd();

