// карта на телефоне
$('#mapBtn').addEventListener('click', e => { const on = $('.res').classList.toggle('showmap'); e.currentTarget.setAttribute('aria-pressed', on); e.currentTarget.lastChild.textContent = on ? 'Списком' : 'На карте'; });


