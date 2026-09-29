import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Lmao 💗", page_icon="💗", layout="centered")

# ---------- Black & Pink theme for the Streamlit page ----------
# (For a permanent theme also create .streamlit/config.toml, see bottom of file)
st.markdown(
    """
    <style>
        .stApp { background-color: #000000; }
        header[data-testid="stHeader"] { background: transparent; }
        h1, p, span, label { color: #ffb6c1 !important; }
        .block-container { padding-top: 2rem; }
        footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "<h1 style='text-align:center;'>💗 Something for you 💗</h1>",
    unsafe_allow_html=True,
)

# ---------- The turtle heart, re-created in a canvas ----------
# Same math as the turtle code:
#   for scale in range(11, 17): for i in range(120): draw" at the heart curve
APP_HTML = """
<style>
  html, body { margin:0; background:#000; font-family: Arial, sans-serif; }
  #stage { position:relative; width:100%; height:640px; overflow:hidden; background:#000; }
  #row { display:flex; gap:16px; justify-content:center; align-items:center;
         padding-top:14px; position:relative; z-index:5; flex-wrap:wrap; }
  button {
    font-size:18px; font-weight:bold; padding:14px 26px; border-radius:50px;
    border:2px solid #ff6c9d; cursor:pointer; transition: transform .15s, box-shadow .15s;
    -webkit-tap-highlight-color: transparent; touch-action: manipulation;
  }
  #play { background:#ff6c9d; color:#000; box-shadow:0 0 18px #ff6c9d88; }
  #play:hover { transform:scale(1.06); box-shadow:0 0 28px #ff6c9d; }
  #nope { background:#000; color:#ffb6c1; }
  #nope.free { position:absolute; z-index:10; transition: left .12s ease-out, top .12s ease-out; }
  #placeholder { display:none; }
  canvas { position:absolute; left:0; top:70px; width:100%; height:calc(100% - 70px); }
  #msg { position:absolute; bottom:10px; width:100%; text-align:center; color:#ff6c9d;
         font-size:15px; min-height:20px; z-index:4; }
</style>

<div id="stage">
  <div id="row">
    <button id="play">▶ Play</button>
    <span id="placeholder"></span>
    <button id="nope">💔 I didn't like it</button>
  </div>
  <canvas id="c"></canvas>
  <div id="msg"></div>
</div>

<script>
const stage = document.getElementById('stage');
const canvas = document.getElementById('c');
const ctx = canvas.getContext('2d');
const playBtn = document.getElementById('play');
const nope = document.getElementById('nope');
const placeholder = document.getElementById('placeholder');
const msg = document.getElementById('msg');
let timer = null;

function fitCanvas() {
  const r = canvas.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  canvas.width = r.width * dpr;
  canvas.height = r.height * dpr;
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.fillStyle = '#000';
  ctx.fillRect(0, 0, r.width, r.height);
}
fitCanvas();
window.addEventListener('resize', fitCanvas);

/* ---------------- PLAY: draws the heart of "I love you" ---------------- */
function play() {
  if (timer) clearInterval(timer);
  fitCanvas();
  const r = canvas.getBoundingClientRect();
  const k = Math.min(r.width / 600, r.height / 560);      // responsive scaling
  const cx = r.width / 2, cy = r.height / 2 + 20 * k;

  ctx.fillStyle = '#ffb6c1';
  ctx.font = 'bold ' + Math.max(6, 8 * k) + 'px Arial';
  ctx.textAlign = 'center';

  let scale = 11, i = 0;
  timer = setInterval(() => {
    const angle = i * (Math.PI * 2) / 120;
    const x = 16 * Math.pow(Math.sin(angle), 3) * scale;
    const y = (13 * Math.cos(angle) - 5 * Math.cos(2 * angle)
              - 2 * Math.cos(3 * angle) - Math.cos(4 * angle)) * scale;
    ctx.fillText('I love you', cx + x * k, cy - y * k);   // canvas y is flipped
    i++;
    if (i >= 120) { i = 0; scale++; }
    if (scale > 16) { clearInterval(timer); msg.textContent = '💗 I love you 💗'; }
  }, 9);
  msg.textContent = '';
}
playBtn.addEventListener('click', play);

/* ------------- "I didn't like it": impossible to click ------------- */
const taunts = ["Nope 😏", "Too slow!", "Nice try 💗", "Can't catch me", "You know you loved it", "Missed!"];
let free = false;

function dodge() {
  const s = stage.getBoundingClientRect();
  if (!free) {                                  // detach from the row on first dodge
    const b = nope.getBoundingClientRect();
    placeholder.style.display = 'inline-block';
    placeholder.style.width = b.width + 'px';
    placeholder.style.height = b.height + 'px';
    nope.classList.add('free');
    nope.style.left = (b.left - s.left) + 'px';
    nope.style.top = (b.top - s.top) + 'px';
    free = true;
  }
  const b = nope.getBoundingClientRect();
  const maxX = s.width - b.width - 8;
  const maxY = s.height - b.height - 8;
  nope.style.left = Math.max(8, Math.random() * maxX) + 'px';
  nope.style.top = Math.max(8, Math.random() * maxY) + 'px';
  msg.textContent = taunts[Math.floor(Math.random() * taunts.length)];
}

// Laptop: jump away before the cursor even reaches it
nope.addEventListener('mouseenter', dodge);
document.addEventListener('mousemove', (e) => {
  const b = nope.getBoundingClientRect();
  const dx = e.clientX - (b.left + b.width / 2);
  const dy = e.clientY - (b.top + b.height / 2);
  if (Math.hypot(dx, dy) < 90) dodge();
});
// Phone: jump away the moment a finger touches it
['touchstart', 'pointerdown', 'mousedown', 'click'].forEach(ev =>
  nope.addEventListener(ev, (e) => { e.preventDefault(); e.stopPropagation(); dodge(); },
                        { passive: false })
);
</script>
"""

components.html(APP_HTML, height=660)

st.markdown(
    "<p style='text-align:center; opacity:.7;'>Press play 💗</p>",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Optional permanent theme: create  .streamlit/config.toml  with:
#
# [theme]
# base = "dark"
# backgroundColor = "#000000"
# secondaryBackgroundColor = "#1a0a10"
# primaryColor = "#ff6c9d"
# textColor = "#ffb6c1"
#
# Run with:  streamlit run love_app.py
# ---------------------------------------------------------------------------
