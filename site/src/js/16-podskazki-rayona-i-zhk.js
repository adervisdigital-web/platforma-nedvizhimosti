// подсказки района и ЖК
$('#adList').innerHTML = [...new Set(ALL.flatMap(it => [it.d, it.zk]))].map(v => `<option value="${v}">`).join('');

