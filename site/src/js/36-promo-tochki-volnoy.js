// промо: точки волной
$$('.pt .dotgrid').forEach(g => { const C = 7, R = 5; g.innerHTML = Array.from({length: C * R}, (_, i) => { const x = i % C, y = Math.floor(i / C); return `<i style="--d:${(C - 1 - x) + (R - 1 - y)}"${(x + y) % 9 === 4 ? ' class="hot"' : ''}></i>`; }).join(''); });
