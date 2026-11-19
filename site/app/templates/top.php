<body>
<div class="ldr" id="ldr" aria-hidden="true">
  <div class="ldr-in"><svg class="ldr-mark" viewBox="0 0 76 72"><path class="ldr-arch" d="M0 72 V24 A24 24 0 0 1 48 24 V72 H33 V26 A9 9 0 0 0 15 26 V72 Z"/><circle class="ldr-dot" cx="67" cy="63" r="9"/></svg>
    <div class="ldr-word"><b>ПЛАТФОРМА</b><small>НЕДВИЖИМОСТИ</small></div></div>
  <span class="ldr-city">Екатеринбург</span><span class="ldr-pc" id="ldrPc">0 %</span><div class="ldr-bar"><i id="ldrBar"></i></div>
</div>
<script>
(() => {
  if (/[?&]shot(&|$)/.test(location.search)) { document.getElementById('ldr').classList.add('gone'); document.documentElement.classList.add('shot'); html_ready(); return; }
  function html_ready() { document.documentElement.classList.add('ready'); }
  const L = document.getElementById('ldr'), bar = document.getElementById('ldrBar'), pc = document.getElementById('ldrPc'), html = document.documentElement;
  let seen = false; try { seen = sessionStorage.getItem('pn_ldr') === '1'; sessionStorage.setItem('pn_ldr', '1'); } catch (e) {}
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches, MIN = seen || reduce ? 500 : 1700, MAX = 4000, t0 = performance.now();
  if (seen) L.classList.add('quick');
  let p = 0, loaded = false, done = false;
  const set = v => { p = v; bar.style.width = v + '%'; pc.textContent = Math.round(v) + ' %'; };
  const tick = setInterval(() => { const el = performance.now() - t0; const target = loaded ? 100 : Math.min(92, 92 * (1 - Math.exp(-el / 900))); set(p + (target - p) * .25);
    if ((loaded && el > MIN && p > 99) || el > MAX) finish(); }, 40);
  function finish() { if (done) return; done = true; clearInterval(tick); set(100);
    setTimeout(() => { html.classList.add('ready'); L.classList.add('out'); setTimeout(() => L.classList.add('gone'), 900); }, 120); }
  addEventListener('load', () => { loaded = true; });
})();
</script>
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="heart" viewBox="0 0 24 24"><path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z" style="fill:var(--if,none);stroke:currentColor" stroke-width="1.8"/></symbol>
  <symbol id="cmp" viewBox="0 0 24 24"><g style="fill:none;stroke:currentColor" stroke-width="1.7"><rect x="3" y="5" width="7.5" height="14" rx="2"/><rect x="13.5" y="5" width="7.5" height="14" rx="2"/><path d="M6 15h1.5M17 15h1.5" stroke-linecap="round"/></g></symbol>
  <symbol id="check" viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></symbol>
  <symbol id="pin" viewBox="0 0 24 24"><path d="M12 21s-6-5.6-6-11a6 6 0 0 1 12 0c0 5.4-6 11-6 11z" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="10" r="2" fill="currentColor"/></symbol>
  <symbol id="i-search" viewBox="0 0 24 24"><circle cx="11" cy="11" r="6.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M16 16l4 4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></symbol>
  <symbol id="user" viewBox="0 0 24 24"><circle cx="12" cy="8.5" r="3.8" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M4.5 20c1.2-3.6 4-5.3 7.5-5.3s6.3 1.7 7.5 5.3" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></symbol>
  <symbol id="i-calc" viewBox="0 0 24 24"><rect x="5" y="3" width="14" height="18" rx="3" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M8.5 8h7M8.5 12.5h1M12 12.5h1M8.5 16.5h1M12 16.5h1" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></symbol>
  <symbol id="msg" viewBox="0 0 24 24"><path d="M4 5.5h16v11H9l-5 4z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></symbol>
  <symbol id="phone" viewBox="0 0 24 24"><path d="M6.6 3.5h2.6l1.4 4.2-2 1.3a11 11 0 0 0 6.4 6.4l1.3-2 4.2 1.4v2.6a2 2 0 0 1-2.2 2A16.6 16.6 0 0 1 4.6 5.7a2 2 0 0 1 2-2.2z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></symbol>
  <symbol id="share" viewBox="0 0 24 24"><path d="M12 15V4M7.5 8.5 12 4l4.5 4.5M5 13v6h14v-6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></symbol>
  <symbol id="t-search" viewBox="0 0 24 24"><circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M15.5 15.5l4.5 4.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle class="td" style="fill:var(--td,currentColor)" cx="10.5" cy="10.5" r="2"/></symbol>
  <symbol id="t-map" viewBox="0 0 24 24"><path d="M12 21.5s-6.5-6-6.5-11.5a6.5 6.5 0 0 1 13 0c0 5.5-6.5 11.5-6.5 11.5z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><circle class="td" style="fill:var(--td,currentColor)" cx="12" cy="10" r="2.4"/></symbol>
  <symbol id="t-pct" viewBox="0 0 24 24"><path d="M18 5L6 19" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="7" cy="7" r="2.6" fill="none" stroke="currentColor" stroke-width="1.6"/><circle class="td" style="fill:var(--td,currentColor)" cx="17" cy="17" r="2.8"/></symbol>
  <symbol id="t-door" viewBox="0 0 24 24"><path d="M4.5 21V10a6 6 0 0 1 12 0v11" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><path d="M8.5 21v-9.5a2 2 0 0 1 4 0V21" fill="none" stroke="currentColor" stroke-width="1.6"/><circle class="td" style="fill:var(--td,currentColor)" cx="20" cy="19" r="2.2"/></symbol>
  <symbol id="t-chat" viewBox="0 0 24 24"><path d="M4 5.5h16v11H10l-5 4v-4H4z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><circle cx="8.5" cy="11" r="1.1" fill="currentColor"/><circle cx="12" cy="11" r="1.1" fill="currentColor"/><circle class="td" style="fill:var(--td,currentColor)" cx="15.5" cy="11" r="1.5"/></symbol>
  <symbol id="t-menu" viewBox="0 0 24 24"><path d="M4 8h16M4 15h10" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/><circle cx="18.5" cy="15" r="2" fill="#F5553C"/></symbol>
  <symbol id="mark" viewBox="0 0 76 72"><path d="M0 72 V24 A24 24 0 0 1 48 24 V72 H33 V26 A9 9 0 0 0 15 26 V72 Z"/><circle cx="67" cy="63" r="9" fill="#F5553C"/></symbol>
</svg>

<div class="prog" id="prog" aria-hidden="true"><i></i><b></b></div>
