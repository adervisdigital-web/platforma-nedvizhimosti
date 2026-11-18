// отзывы: стрелки
$$('.arr button').forEach(b => b.addEventListener('click', () => { const rv = $('.rv'); rv.scrollBy({left: +b.dataset.d * ($('.rc').offsetWidth + 14), behavior: reduce ? 'auto' : 'smooth'}); }));

