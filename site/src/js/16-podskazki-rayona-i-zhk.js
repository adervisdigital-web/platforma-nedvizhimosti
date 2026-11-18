// подсказки района и ЖК
$('#adList').innerHTML = [...new Set(ITEMS.flatMap(it => [it.d, it.zk]))].map(v => `<option value="${v}">`).join('');

