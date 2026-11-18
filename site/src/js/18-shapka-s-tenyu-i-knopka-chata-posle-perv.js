// шапка с тенью и кнопка чата — после первого экрана
const hdr = $('header'), fab = $('#chatFab');
function onScroll() { hdr.classList.toggle('sc', scrollY > 10); fab.classList.toggle('show', scrollY > $('.hero').offsetHeight * .6); fab.classList.toggle('mini', scrollY > $('.hero').offsetHeight * 1.4); }
addEventListener('scroll', onScroll, {passive: true}); onScroll();

