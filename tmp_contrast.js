var els = document.querySelectorAll('p,span,a,button,label,h1,h2,h3,h4,h5,h6');
var r = [];
for (var i = 0; i < els.length; i++) {
  var el = els[i];
  if (!el.textContent.trim()) continue;
  var s = getComputedStyle(el);
  var c = s.color;
  var bg = s.backgroundColor;
  if (c && bg && bg !== 'rgba(0, 0, 0, 0)') {
    r.push({text: el.textContent.trim().slice(0, 30), color: c, bg: bg, fontSize: s.fontSize});
  }
  if (r.length >= 10) break;
}
JSON.stringify(r);
