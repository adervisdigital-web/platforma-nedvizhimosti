
const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
const fmtM = n => (n / 1e6).toLocaleString('ru-RU', {maximumFractionDigits: 2}) + ' млн ₽';
const ann = (P, r) => { const L = P * .8, m = r / 1200; return L * m / (1 - Math.pow(1 + m, -360)); };
const plural = (n, a, b, c) => { const m = n % 10, h = n % 100; return m === 1 && h !== 11 ? a : m >= 2 && m <= 4 && (h < 12 || h > 14) ? b : c; };
