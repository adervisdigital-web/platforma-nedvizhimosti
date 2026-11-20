// «Квартира. Дом. Ремонт.»: на сенсорных экранах фото ремонта само переключается «до → после»; «Один менеджер на всё» открывает заявку с пакетом «квартира + ремонт».
(() => {
  const pba = document.querySelector('[data-pba]');
  if (pba && matchMedia('(hover: none)').matches && !matchMedia('(prefers-reduced-motion: reduce)').matches && 'IntersectionObserver' in window) {
    let t = null;
    new IntersectionObserver(([e]) => {
      clearInterval(t);
      if (e.isIntersecting) { pba.classList.add('is-after'); t = setInterval(() => pba.classList.toggle('is-after'), 2800); }
    }, {threshold: .5}).observe(pba);
  }
})();
