#!/usr/bin/env python3
"""Bundle assets into a single self-contained HTML for mobile use."""
import base64
import pathlib

HERE = pathlib.Path(__file__).parent
ASSETS = HERE / "assets"
OUT = HERE / "index.html"

BRANDS = [
    ("Samsung",    "samsung.png",          "image/png"),
    ("LG",         "lg-logo.png",          "image/png"),
    ("Panasonic",  "Panasonic-logo.jpg",   "image/jpeg"),
    ("Mitsubishi", "mitsubishi-logo.jpg",  "image/jpeg"),
    ("Haier",      "haier.jpeg",           "image/jpeg"),
    ("Daikin",     "daikin.jpg",           "image/jpeg"),
    ("Godrej",     "godrej.jpeg",          "image/jpeg"),
    ("Lloyd",      "llyod.jpeg",           "image/jpeg"),
    ("Blue Star",  "bluestar.png",         "image/png"),
]

def data_uri(filename: str, mime: str) -> str:
    data = (ASSETS / filename).read_bytes()
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:{mime};base64,{b64}"

entries = []
for name, fname, mime in BRANDS:
    entries.append(f'    {{ name: {name!r}, src: "{data_uri(fname, mime)}" }}')
brands_js = ",\n".join(entries)

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover, user-scalable=no" />
<meta name="apple-mobile-web-app-capable" content="yes" />
<meta name="mobile-web-app-capable" content="yes" />
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
<meta name="theme-color" content="#0b1220" />
<title>Brand Pop Quiz</title>
<style>
  :root {
    --bg-1: #0b1220;
    --bg-2: #131b2e;
    --card: #ffffff;
    --ink: #e8ecf4;
    --ink-dim: #9aa3b2;
    --ink-faint: #5b6477;
    --accent: #c9a96a;
    --rule: rgba(255,255,255,0.08);
    --btn-bg: rgba(255,255,255,0.06);
    --btn-bg-active: rgba(201,169,106,0.18);
    --btn-border: rgba(255,255,255,0.12);
    --card-shadow:
      0 1px 0 rgba(255,255,255,0.04) inset,
      0 30px 80px -20px rgba(0,0,0,0.55),
      0 8px 24px -8px rgba(0,0,0,0.4);
  }

  * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }

  html, body {
    margin: 0;
    padding: 0;
    height: 100%;
    color: var(--ink);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
    user-select: none;
    -webkit-user-select: none;
    overflow: hidden;
    overscroll-behavior: none;
    touch-action: manipulation;
  }

  body {
    min-height: 100vh;
    min-height: 100dvh;
    background:
      radial-gradient(900px 700px at 20% 0%, rgba(201, 169, 106, 0.08), transparent 60%),
      radial-gradient(800px 600px at 80% 100%, rgba(80, 120, 200, 0.08), transparent 60%),
      linear-gradient(160deg, var(--bg-1) 0%, var(--bg-2) 100%);
    display: flex;
    flex-direction: column;
    padding: env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left);
  }

  body::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    background-image:
      linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
    background-size: 40px 40px;
    mask-image: radial-gradient(ellipse at center, black 30%, transparent 75%);
    -webkit-mask-image: radial-gradient(ellipse at center, black 30%, transparent 75%);
  }

  /* ---------- Header ---------- */
  header {
    flex: 0 0 auto;
    padding: 16px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--rule);
  }
  .brand {
    display: flex;
    align-items: center;
    gap: 10px;
    letter-spacing: 0.14em;
    font-size: 11px;
    text-transform: uppercase;
    color: var(--ink-dim);
    font-weight: 500;
  }
  .brand .dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: var(--accent);
    box-shadow: 0 0 12px var(--accent);
  }
  .counter {
    font-variant-numeric: tabular-nums;
    font-size: 12px;
    letter-spacing: 0.08em;
    color: var(--ink-dim);
  }
  .counter strong {
    color: var(--ink);
    font-weight: 600;
  }

  /* ---------- Stage ---------- */
  main {
    flex: 1 1 auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 18px 18px 8px;
    position: relative;
    min-height: 0;
  }

  .card {
    position: relative;
    background: var(--card);
    border-radius: 20px;
    width: 100%;
    max-width: 520px;
    flex: 1 1 auto;
    min-height: 0;
    max-height: 60vh;
    box-shadow: var(--card-shadow);
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 28px;
    cursor: pointer;
  }
  .card:active { transform: scale(0.995); }

  .card::after {
    content: "";
    position: absolute;
    inset: 0;
    pointer-events: none;
    background: radial-gradient(circle at 30% 0%, rgba(255,255,255,0.55), transparent 50%);
    mix-blend-mode: overlay;
    opacity: 0.6;
  }

  .logo-wrap {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: opacity 220ms ease, transform 220ms ease;
  }
  .logo-wrap.out { opacity: 0; transform: scale(0.98); }
  .logo-wrap img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
    -webkit-user-drag: none;
    pointer-events: none;
  }

  /* ---------- Answer reveal ---------- */
  .answer {
    margin-top: 18px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    opacity: 0;
    transform: translateY(8px);
    transition: opacity 240ms ease, transform 240ms ease;
  }
  .answer.show { opacity: 1; transform: translateY(0); }
  .answer .name {
    font-size: 22px;
    font-weight: 600;
    letter-spacing: 0.04em;
    color: var(--ink);
  }
  .answer .accent {
    width: 18px;
    height: 2px;
    background: var(--accent);
    border-radius: 2px;
  }

  /* ---------- Progress dots ---------- */
  .progress {
    margin-top: 14px;
    display: flex;
    gap: 7px;
    flex-wrap: wrap;
    justify-content: center;
  }
  .progress span {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: rgba(255,255,255,0.12);
    transition: background 200ms ease, transform 200ms ease;
  }
  .progress span.done    { background: var(--accent); }
  .progress span.current { background: var(--ink); transform: scale(1.4); }

  /* ---------- Action bar (mobile-first) ---------- */
  .actions {
    flex: 0 0 auto;
    padding: 14px 16px calc(14px + env(safe-area-inset-bottom));
    display: grid;
    grid-template-columns: 1fr 1.4fr 1fr;
    gap: 10px;
    border-top: 1px solid var(--rule);
  }
  .btn {
    appearance: none;
    -webkit-appearance: none;
    background: var(--btn-bg);
    border: 1px solid var(--btn-border);
    color: var(--ink);
    font-family: inherit;
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 0.05em;
    padding: 14px 10px;
    border-radius: 12px;
    cursor: pointer;
    transition: background 140ms ease, transform 80ms ease, border-color 140ms ease;
    text-transform: uppercase;
  }
  .btn:active { transform: scale(0.97); background: var(--btn-bg-active); }
  .btn.primary {
    background: var(--accent);
    color: #1f1606;
    border-color: transparent;
  }
  .btn.primary:active { background: #b8965a; }
  .btn.ghost {
    color: var(--ink-dim);
  }

  /* ---------- Finished state ---------- */
  .done {
    text-align: center;
    padding: 16px;
  }
  .done .tick {
    width: 52px;
    height: 52px;
    border-radius: 50%;
    border: 2px solid var(--accent);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    color: var(--accent);
    font-size: 26px;
    margin-bottom: 16px;
  }
  .done h1 {
    margin: 0 0 8px;
    font-size: 24px;
    font-weight: 600;
    letter-spacing: -0.01em;
    color: #1f2433;
  }
  .done p {
    margin: 0;
    color: #5b6477;
    font-size: 14px;
  }

  /* Larger phones / tablets */
  @media (min-width: 600px) {
    header { padding: 22px 28px; }
    .brand { font-size: 12px; }
    .counter { font-size: 13px; }
    .card { padding: 40px; max-height: 56vh; }
    .answer .name { font-size: 26px; }
    .actions { padding: 18px 22px calc(18px + env(safe-area-inset-bottom)); }
    .btn { font-size: 15px; padding: 16px 12px; }
  }

  /* Landscape on phones — keep card visible */
  @media (orientation: landscape) and (max-height: 500px) {
    main { padding: 10px; }
    .card { max-height: 65vh; padding: 18px; }
    .answer { margin-top: 10px; height: 30px; }
    .answer .name { font-size: 18px; }
    .progress { margin-top: 8px; }
    .actions { padding: 8px 12px calc(8px + env(safe-area-inset-bottom)); }
    .btn { padding: 10px; font-size: 13px; }
  }
</style>
</head>

<body>
  <header>
    <div class="brand">
      <span class="dot"></span>
      <span>Brand Pop Quiz</span>
    </div>
    <div class="counter"><strong id="cur">1</strong> &nbsp;/&nbsp; <span id="total">9</span></div>
  </header>

  <main>
    <div class="card" id="card">
      <div class="logo-wrap" id="logoWrap"></div>
    </div>

    <div class="answer" id="answer">
      <span class="accent"></span>
      <span class="name" id="name"></span>
      <span class="accent"></span>
    </div>

    <div class="progress" id="progress"></div>
  </main>

  <div class="actions">
    <button class="btn ghost" id="btnReveal">Reveal</button>
    <button class="btn primary" id="btnNext">Next</button>
    <button class="btn ghost" id="btnRestart">Restart</button>
  </div>

<script>
  const brands = [
__BRANDS__
  ];

  const cardEl     = document.getElementById('card');
  const logoWrap   = document.getElementById('logoWrap');
  const answerEl   = document.getElementById('answer');
  const nameEl     = document.getElementById('name');
  const curEl      = document.getElementById('cur');
  const totalEl    = document.getElementById('total');
  const progressEl = document.getElementById('progress');
  const btnNext    = document.getElementById('btnNext');
  const btnReveal  = document.getElementById('btnReveal');
  const btnRestart = document.getElementById('btnRestart');

  let order = [];
  let index = 0;
  let finished = false;

  function shuffle(arr) {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  function buildProgressDots() {
    progressEl.innerHTML = '';
    for (let i = 0; i < order.length; i++) {
      progressEl.appendChild(document.createElement('span'));
    }
    updateProgress();
  }

  function updateProgress() {
    const dots = progressEl.children;
    for (let i = 0; i < dots.length; i++) {
      dots[i].classList.remove('done', 'current');
      if (i < index) dots[i].classList.add('done');
      else if (i === index) dots[i].classList.add('current');
    }
  }

  function showCard() {
    if (finished) return;
    const b = order[index];
    logoWrap.classList.add('out');
    answerEl.classList.remove('show');

    setTimeout(function () {
      const img = document.createElement('img');
      img.alt = '';
      img.src = b.src;
      logoWrap.innerHTML = '';
      logoWrap.appendChild(img);
      nameEl.textContent = b.name;
      curEl.textContent = index + 1;
      updateProgress();
      requestAnimationFrame(function () { logoWrap.classList.remove('out'); });
    }, 200);
  }

  function next() {
    if (finished) { restart(); return; }
    if (index < order.length - 1) {
      index++;
      showCard();
    } else {
      finish();
    }
  }

  function reveal() {
    if (!finished) answerEl.classList.add('show');
  }

  function finish() {
    finished = true;
    logoWrap.classList.add('out');
    answerEl.classList.remove('show');
    setTimeout(function () {
      logoWrap.innerHTML =
        '<div class="done">' +
          '<div class="tick">&#10003;</div>' +
          '<h1>All nine, named.</h1>' +
          '<p>Tap Next to play again.</p>' +
        '</div>';
      Array.prototype.forEach.call(progressEl.children, function (d) {
        d.classList.remove('current');
        d.classList.add('done');
      });
      curEl.textContent = order.length;
      requestAnimationFrame(function () { logoWrap.classList.remove('out'); });
    }, 200);
  }

  function restart() {
    finished = false;
    order = shuffle(brands);
    index = 0;
    totalEl.textContent = order.length;
    buildProgressDots();
    showCard();
  }

  // Tap card to advance
  cardEl.addEventListener('click', next);

  // Buttons
  btnNext.addEventListener('click', next);
  btnReveal.addEventListener('click', reveal);
  btnRestart.addEventListener('click', restart);

  // Keyboard (when used on desktop too)
  document.addEventListener('keydown', function (e) {
    if (e.code === 'Space')               { e.preventDefault(); next(); }
    else if (e.key === 'a' || e.key === 'A') { reveal(); }
    else if (e.key === 'r' || e.key === 'R') { restart(); }
  });

  restart();
</script>
</body>
</html>
"""

OUT.write_text(HTML.replace("__BRANDS__", brands_js), encoding="utf-8")
print(f"Wrote {OUT} ({OUT.stat().st_size / 1024:.1f} KB)")
