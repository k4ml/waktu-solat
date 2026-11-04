"""Pencari arah kiblat (Qibla direction finder) — served at /kiblat/.

The bearing itself is pure math (great-circle bearing to the Kaaba) and needs
no network, so it is computed in the browser and also mirrored here in Python
for the copy shown to crawlers and as a fallback default.

The page is deliberately self-contained: geolocation and the device compass are
browser APIs, so everything interactive lives in one inline script. Only the
values that are useful to crawlers (canonical URL, default coordinates) are
injected by the worker.

Placeholders use @@NAME@@ markers rather than str.format so the embedded
JavaScript can keep its braces.
"""

from math import atan2, cos, degrees, radians, sin
from html import escape
import json

# Kaaba, Masjid al-Haram, Makkah.
KAABA_LAT = 21.4225
KAABA_LNG = 39.8262

# Default to Kuala Lumpur so the page is useful before permission is granted.
DEFAULT_LAT = 3.1390
DEFAULT_LNG = 101.6869


def qibla_bearing(lat: float, lng: float) -> float:
    """Great-circle initial bearing (degrees clockwise from true north)."""
    kaaba_lat = radians(KAABA_LAT)
    kaaba_lng = radians(KAABA_LNG)
    lat = radians(lat)
    lng = radians(lng)
    d_lng = kaaba_lng - lng
    y = sin(d_lng) * cos(kaaba_lat)
    x = cos(lat) * sin(kaaba_lat) - sin(lat) * cos(kaaba_lat) * cos(d_lng)
    return (degrees(atan2(y, x)) + 360) % 360


# Malaysian cities the bearing differs noticeably between; used by the manual
# picker for desktop users who will not grant geolocation.
CITY_PRESETS = [
    ("Kuala Lumpur", 3.1390, 101.6869),
    ("Johor Bahru", 1.4927, 103.7414),
    ("George Town", 5.4141, 100.3288),
    ("Ipoh", 4.5975, 101.0901),
    ("Kuantan", 3.8077, 103.3260),
    ("Kota Kinabalu", 5.9804, 116.0735),
    ("Kuching", 1.5533, 110.3592),
    ("Kota Bharu", 6.1254, 102.2381),
]

_SITE_SUFFIX = " - Waktu Solat Malaysia"
_OG_IMAGE_PATH = "/social-card.png"

# The Kaaba glyph, reused by the compass needle and the intro note.
_KAABA_SVG = (
    '<path d="M12 2 3 7v10l9 5 9-5V7z"/>'
    '<path d="M12 2v20M3 7l9 5 9-5"/>'
)

PAGE = """<!DOCTYPE html>
<html lang="ms">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<title>@@TITLE@@</title>
<meta name="theme-color" content="#111820">

<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-4EM4VJY5X6"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-4EM4VJY5X6');
</script>
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Arah Kiblat">
<meta name="mobile-web-app-capable" content="yes">
<meta name="description" content="@@DESCRIPTION@@">
<link rel="canonical" href="@@CANONICAL@@">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:url" content="@@CANONICAL@@">
<meta property="og:title" content="@@TITLE@@">
<meta property="og:description" content="@@DESCRIPTION@@">
<meta property="og:locale" content="ms_MY">
<meta property="og:site_name" content="Waktu Solat Malaysia">
<meta property="og:image" content="@@OG_IMAGE@@">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="@@OG_IMAGE_WIDTH@@">
<meta property="og:image:height" content="@@OG_IMAGE_HEIGHT@@">
<meta property="og:image:alt" content="@@OG_IMAGE_ALT@@">

<!-- Twitter -->
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="@@TITLE@@">
<meta name="twitter:description" content="@@DESCRIPTION@@">
<meta name="twitter:image" content="@@OG_IMAGE@@">
<meta name="twitter:image:alt" content="@@OG_IMAGE_ALT@@">

<!-- PWA -->
<link rel="manifest" href="/manifest.webmanifest">
<link rel="icon" href="/icons/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/icons/icon.svg">

<script type="application/ld+json">@@JSON_LD@@</script>

<style>
  :root {
    --ink:#0d1117; --deep:#111820; --panel:#161e27; --card:#1c2733;
    --border:rgba(180,145,80,0.2); --gold:#c9a84c; --gold-light:#e8c97a;
    --gold-dim:rgba(201,168,76,0.12); --teal:#2a7a72; --teal-light:#3da99f;
    --text:#e8e0d0; --text-dim:rgba(232,224,208,0.55); --text-muted:rgba(232,224,208,0.3);
    --active-glow:0 0 30px rgba(201,168,76,0.25); --r:12px;
    --sans:'Segoe UI',system-ui,sans-serif;
    --arabic:'Noto Naskh Arabic','Amiri','Scheherazade New','Times New Roman',serif;
  }
  *,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
  body{background:var(--ink);color:var(--text);font-family:var(--sans);min-height:100vh;overflow-x:hidden;}
  body::before{content:'';position:fixed;inset:0;z-index:0;background:radial-gradient(ellipse 80% 50% at 50% -10%,rgba(42,122,114,.18) 0%,transparent 60%),radial-gradient(ellipse 60% 40% at 100% 100%,rgba(201,168,76,.08) 0%,transparent 55%);pointer-events:none;}
  .geo{position:fixed;inset:0;z-index:0;opacity:.04;pointer-events:none;background-image:repeating-linear-gradient(60deg,var(--gold) 0,var(--gold) 1px,transparent 0,transparent 50%),repeating-linear-gradient(-60deg,var(--gold) 0,var(--gold) 1px,transparent 0,transparent 50%),repeating-linear-gradient(0deg,var(--gold) 0,var(--gold) 1px,transparent 0,transparent 50%);background-size:60px 60px;}
  #app{position:relative;z-index:1;max-width:540px;margin:0 auto;padding:0 14px 60px;}

  header{text-align:center;padding:32px 0 18px;}
  .arabic-title{font-family:var(--arabic);font-size:clamp(26px,7vw,40px);color:var(--gold);line-height:1.3;display:block;margin-bottom:4px;}
  .latin-title{font-size:clamp(10px,3vw,13px);letter-spacing:.3em;color:var(--text-dim);text-transform:uppercase;font-weight:600;}
  .hline{width:80px;height:1px;background:linear-gradient(to right,transparent,var(--gold),transparent);margin:12px auto 0;}

  nav.mainmenu{display:flex;gap:8px;justify-content:center;align-items:center;margin:16px 0 16px;font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;font-weight:600;}
  nav.mainmenu a{color:var(--gold);text-decoration:none;opacity:.7;border:1px solid transparent;border-radius:999px;padding:7px 15px;transition:opacity .2s,border-color .2s,background .2s;}
  nav.mainmenu a:hover{opacity:1;}
  nav.mainmenu a.active{opacity:1;border-color:var(--border);background:var(--gold-dim);}

  .card{background:var(--panel);border:1px solid var(--border);border-radius:var(--r);padding:14px 16px;margin-bottom:12px;}
  .card-label{display:block;font-size:10px;letter-spacing:.25em;color:var(--gold);text-transform:uppercase;font-weight:600;margin-bottom:8px;}

  .intro-note{background:rgba(42,122,114,.1);border:1px solid rgba(42,122,114,.25);border-radius:8px;padding:10px 12px;margin-bottom:12px;font-size:12px;color:var(--text-dim);line-height:1.65;}
  .intro-note b{color:var(--gold);}

  .loc-readout{font-size:14px;color:var(--text);margin-bottom:10px;font-weight:600;letter-spacing:.02em;}
  .loc-readout span{color:var(--text-dim);font-weight:400;}
  .btn-row{display:flex;gap:8px;flex-wrap:wrap;}
  .btn{appearance:none;border:none;border-radius:999px;padding:10px 16px;font:inherit;font-size:12.5px;font-weight:600;cursor:pointer;transition:transform .15s ease,opacity .15s ease,border-color .2s ease;}
  .btn:active{transform:scale(.97);}
  .btn.primary{background:var(--gold);color:var(--deep);}
  .btn.secondary{background:rgba(255,255,255,.02);color:var(--text);border:1px solid var(--border);}
  .btn.wide{width:100%;margin-top:12px;}
  .btn:disabled{cursor:not-allowed;opacity:.55;}

  select,input[type=number]{background:var(--card);border:1px solid var(--border);border-radius:8px;color:var(--text);font-family:inherit;font-size:14px;padding:9px 12px;outline:none;transition:border-color .2s;width:100%;}
  select{cursor:pointer;appearance:none;padding-right:32px;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23c9a84c' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 10px center;}
  select:focus,input[type=number]:focus{border-color:var(--gold);}
  select option{background:var(--deep);}

  details.manual{margin-top:12px;border-top:1px solid rgba(255,255,255,.06);padding-top:12px;}
  details.manual summary{cursor:pointer;font-size:11.5px;letter-spacing:.06em;color:var(--text-dim);font-weight:600;list-style:none;}
  details.manual summary::-webkit-details-marker{display:none;}
  details.manual summary::before{content:'▸ ';color:var(--gold);}
  details.manual[open] summary::before{content:'▾ ';}
  .manual-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:10px 0;}
  .manual-grid label{display:block;font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--text-muted);font-weight:600;}
  .manual-grid input{margin-top:4px;}
  .loc-status{font-size:12px;color:var(--text-dim);margin-top:8px;min-height:1px;line-height:1.5;}
  .loc-status.error{color:#e8896a;}

  .compass-card{background:linear-gradient(135deg,rgba(42,122,114,.12),rgba(17,24,32,.96));border:1px solid rgba(61,169,159,.24);border-radius:var(--r);padding:18px 16px;margin-bottom:12px;text-align:center;}
  .bearing-big{font-size:clamp(40px,13vw,60px);font-weight:700;color:var(--gold-light);line-height:1;letter-spacing:.02em;}
  .bearing-big .deg{font-size:.5em;vertical-align:top;opacity:.8;margin-left:2px;}
  .bearing-sub{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--text-dim);margin-top:4px;font-weight:600;}

  .compass{position:relative;width:min(280px,74vw);margin:18px auto 6px;aspect-ratio:1;}
  .compass svg{width:100%;height:100%;display:block;transform-origin:50% 50%;transition:transform .12s linear;will-change:transform;}
  .dial-ring{fill:rgba(13,17,23,.55);stroke:var(--border);stroke-width:1.5;}
  .dial-tick{stroke:var(--text-muted);stroke-width:1.5;}
  .dial-tick.major{stroke:var(--gold);stroke-width:2.5;}
  .dial-letter{fill:var(--gold-light);font-family:var(--sans);font-size:15px;font-weight:700;text-anchor:middle;dominant-baseline:middle;}
  .dial-letter.cardinal{fill:var(--gold);font-size:19px;}
  .dial-num{fill:var(--text-muted);font-family:var(--sans);font-size:8.5px;text-anchor:middle;dominant-baseline:middle;}
  .dial-hub{fill:var(--deep);stroke:var(--gold);stroke-width:2;}
  .qibla-arrow{fill:var(--teal-light);stroke:var(--gold);stroke-width:1.5;}
  .qibla-glyph{fill:none;stroke:var(--deep);stroke-width:1.6;stroke-linejoin:round;}
  .qibla-label{fill:var(--gold-light);font-family:var(--sans);font-size:10px;font-weight:700;letter-spacing:.12em;text-anchor:middle;}
  .device-marker{position:absolute;top:-2px;left:50%;transform:translateX(-50%);color:var(--gold);font-size:16px;text-shadow:0 0 8px rgba(201,168,76,.6);pointer-events:none;}

  .hint{font-size:13px;color:var(--text-dim);line-height:1.6;margin-top:14px;min-height:40px;}
  .hint b{color:var(--gold-light);}
  .sensor-status{font-size:11px;letter-spacing:.06em;color:var(--text-muted);margin-top:10px;line-height:1.5;}
  .calib{display:none;margin-top:10px;font-size:12px;color:var(--gold-light);background:var(--gold-dim);border:1px solid rgba(201,168,76,.3);border-radius:8px;padding:9px 12px;line-height:1.55;}
  .calib.show{display:block;}

  .readout-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:12px;}
  .readout{background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:10px 8px;text-align:center;}
  .readout-label{display:block;font-size:8.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--text-muted);font-weight:600;margin-bottom:5px;}
  .readout-value{font-size:16px;font-weight:600;color:var(--gold-light);}

  .notes{background:var(--panel);border:1px solid var(--border);border-radius:var(--r);padding:16px;margin-bottom:12px;}
  .notes h2{font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-bottom:10px;font-weight:600;}
  .notes ul{padding-left:18px;}
  .notes li{font-size:13px;color:var(--text-dim);line-height:1.7;margin-bottom:8px;}
  .notes li:last-child{margin-bottom:0;}
  .notes b{color:var(--text);}
  .notes a{color:var(--teal-light);text-decoration:none;}
  .notes a:hover{text-decoration:underline;}

  footer{text-align:center;padding:22px 0 0;font-size:11px;color:var(--text-muted);font-style:italic;border-top:1px solid var(--border);margin-top:18px;line-height:1.7;}
  footer a{color:var(--gold);text-decoration:none;}
  footer a:hover{text-decoration:underline;}

  @media (max-width:420px){
    .manual-grid{grid-template-columns:1fr;}
  }
</style>
</head>
<body>
<div class="geo"></div>
<div id="app">
  <header>
    <span class="arabic-title">اتجاه القبلة</span>
    <div class="latin-title">Pencari Arah Kiblat</div>
    <div class="hline"></div>
  </header>

  <nav class="mainmenu" aria-label="Menu utama">
    <a href="/artikel/">Artikel</a>
    <a href="/panduan/">Panduan</a>
    <a href="/kiblat/" class="active" aria-current="page">Kiblat</a>
  </nav>

  <div class="intro-note">
    Arah kiblat dikira terus pada peranti anda (tiada rangkaian diperlukan) menggunakan
    bearing bulatan besar dari lokasi anda ke Kaabah (21.4225°N, 39.8262°E).
    Dari Malaysia ia biasanya sekitar <b>292°–293° dari Utara sebenar</b>.
  </div>

  <div class="card">
    <span class="card-label">Lokasi Anda</span>
    <div class="loc-readout" id="locReadout">Belum ditetapkan</div>
    <div class="btn-row">
      <button class="btn primary" id="detectBtn" type="button">Kesan Lokasi</button>
      <select id="citySelect" aria-label="Pilih bandar">
        <option value="">Pilih bandar…</option>
@@CITY_OPTIONS@@      </select>
    </div>
    <details class="manual">
      <summary>Masukkan koordinat secara manual</summary>
      <div class="manual-grid">
        <label>Latitud<input id="latInput" type="number" step="0.0001" min="-90" max="90" inputmode="decimal" placeholder="3.1390"></label>
        <label>Longitud<input id="lngInput" type="number" step="0.0001" min="-180" max="180" inputmode="decimal" placeholder="101.6869"></label>
      </div>
      <button class="btn secondary" id="applyBtn" type="button">Guna koordinat ini</button>
    </details>
    <div class="loc-status" id="locStatus"></div>
  </div>

  <div class="compass-card">
    <div class="bearing-big"><span id="bearingValue">—</span><span class="deg">°</span></div>
    <div class="bearing-sub" id="bearingSub">dari Utara sebenar</div>

    <div class="compass" id="compass">
      <svg id="dial" viewBox="0 0 260 260" role="img" aria-label="Kompas arah kiblat">
        <circle class="dial-ring" cx="130" cy="130" r="126"></circle>
        <g id="dialTicks"></g>
        <g id="dialLetters"></g>
        <g id="qiblaGroup" transform="rotate(0 130 130)">
          <polygon class="qibla-arrow" points="130,16 143,58 117,58"></polygon>
          <g class="qibla-glyph" transform="translate(130 40) scale(0.62) translate(-12 -12)">@@KAABA_SVG@@</g>
          <text class="qibla-label" x="130" y="78">KIBLAT</text>
        </g>
        <circle class="dial-hub" cx="130" cy="130" r="7"></circle>
      </svg>
      <div class="device-marker" id="deviceMarker" title="Arah bahagian atas peranti">▲</div>
    </div>

    <div class="hint" id="hint">Tetapkan lokasi anda dahulu, kemudian hidupkan kompas dan putar peranti sehingga jarum KIBLAT bertemu penanda ▲ di atas.</div>

    <button class="btn primary wide" id="compassBtn" type="button">Hidupkan Kompas</button>
    <div class="sensor-status" id="sensorStatus">Kompas belum dihidupkan.</div>
    <div class="calib" id="calib">Ketepatan kompas rendah. Gerakkan peranti dalam corak <b>angka lapan (8)</b> untuk mengkalibrasi magnetometer.</div>
  </div>

  <div class="readout-grid">
    <div class="readout"><span class="readout-label">Kiblat</span><span class="readout-value" id="roBearing">—</span></div>
    <div class="readout"><span class="readout-label">Hala peranti</span><span class="readout-value" id="roHeading">—</span></div>
    <div class="readout"><span class="readout-label">Dari atas skrin</span><span class="readout-value" id="roRelative">—</span></div>
  </div>

  <div class="notes">
    <h2>Nota</h2>
    <ul>
      <li><b>Kompas:</b> pada iPhone, ketepatan lebih baik menggunakan <b>webkitCompassHeading</b>; pada Android kami utamakan peristiwa <b>deviceorientationabsolute</b> supaya bacaan relatif kepada Utara sebenar, bukan arah relatif peranti.</li>
      <li><b>Keizinan:</b> iOS 13+ memerlukan ketikan pengguna untuk kedua-dua lokasi dan orientasi. Itulah sebabnya butang “Kesan Lokasi” dan “Hidupkan Kompas” perlu ditekan.</li>
      <li><b>Magnetometer:</b> bacaan lemah dalam bangunan atau berhampiran logam. Kalibrasi dengan corak angka 8 apabila diminta.</li>
      <li><b>Tiada sensor?</b> Kebanyakan komputer meja tiada API orientasi. Gunakan bacaan darjah: putar sehingga <b>Utara</b> pada carta menghadap Utara sebenar — jarum kiblat kemudiannya menunjukkan arah sebenar.</li>
      <li><b>Deklinasi magnetik</b> di Malaysia adalah kecil (±0°–1°), jadi ia diabaikan di sini.</li>
      <li>Perubahan ini adalah panduan umum. Sahkan dengan <a href="https://www.e-solat.gov.my" target="_blank" rel="noopener">e-Solat JAKIM</a> atau masjid berdekatan.</li>
    </ul>
  </div>

  <footer>
    <p>Arah Kiblat · <a href="/">Waktu Solat Malaysia</a> · <a href="/panduan/">Peringatan &amp; Kaedah Pengiraan</a> · <a href="/panduan/nota-pembangunan-kiblat/">Nota Pembangunan</a></p>
    <p style="margin-top:8px;">Oleh <a href="https://kamal.koditi.my/" target="_blank" rel="noopener">kamal.koditi.my</a> · Maklum balas: <a href="https://x.com/k4ml" target="_blank" rel="noopener">@k4ml</a></p>
  </footer>
</div>

<script>
(function () {
  'use strict';

  // ═══ Constants ═══
  var KAABA_LAT = @@KAABA_LAT@@;
  var KAABA_LNG = @@KAABA_LNG@@;
  var DEFAULT_LOC = { lat: @@DEFAULT_LAT@@, lng: @@DEFAULT_LNG@@, label: 'Kuala Lumpur' };
  var STORE_KEY = 'kiblat:location';
  var SVG_NS = 'http://www.w3.org/2000/svg';
  var CENTER = 130;

  var CARDS = [
    { a: 0, t: 'N', cardinal: true },
    { a: 90, t: 'E', cardinal: true },
    { a: 180, t: 'S', cardinal: true },
    { a: 270, t: 'W', cardinal: true }
  ];

  // ═══ Pure math: great-circle bearing to the Kaaba ═══
  function qiblaBearing(lat, lng) {
    var kaabaLat = KAABA_LAT * Math.PI / 180;
    var kaabaLng = KAABA_LNG * Math.PI / 180;
    lat *= Math.PI / 180;
    lng *= Math.PI / 180;
    var dLng = kaabaLng - lng;
    var y = Math.sin(dLng) * Math.cos(kaabaLat);
    var x = Math.cos(lat) * Math.sin(kaabaLat) - Math.sin(lat) * Math.cos(kaabaLat) * Math.cos(dLng);
    return (Math.atan2(y, x) * 180 / Math.PI + 360) % 360;
  }

  // ═══ State ═══
  var loc = null;          // {lat, lng, label}
  var bearing = null;      // degrees from true north
  var heading = 0;         // device heading, 0 = pointing north, clockwise
  var hasHeading = false;
  var orientationStarted = false;
  var gotOrientationEvent = false;

  // ═══ Elements ═══
  var $ = function (id) { return document.getElementById(id); };
  var dial = $('dial');
  var qiblaGroup = $('qiblaGroup');

  // ═══ Dial (compass rose) construction ═══
  function polar(angleDeg, radius) {
    var rad = (angleDeg - 90) * Math.PI / 180;
    return { x: CENTER + radius * Math.cos(rad), y: CENTER + radius * Math.sin(rad) };
  }

  function buildRose() {
    var ticks = $('dialTicks');
    var letters = $('dialLetters');
    var i;

    for (i = 0; i < 360; i += 5) {
      var major = (i % 45) === 0;
      var outer = polar(i, 124);
      var inner = polar(i, major ? 112 : 118);
      var line = document.createElementNS(SVG_NS, 'line');
      line.setAttribute('x1', outer.x.toFixed(2));
      line.setAttribute('y1', outer.y.toFixed(2));
      line.setAttribute('x2', inner.x.toFixed(2));
      line.setAttribute('y2', inner.y.toFixed(2));
      line.setAttribute('class', 'dial-tick' + (major ? ' major' : ''));
      ticks.appendChild(line);
    }

    // Degree numbers every 30°, sitting just inside the ticks.
    for (i = 0; i < 360; i += 30) {
      if (i % 90 === 0) continue;
      var p = polar(i, 102);
      var num = document.createElementNS(SVG_NS, 'text');
      num.setAttribute('x', p.x.toFixed(2));
      num.setAttribute('y', p.y.toFixed(2));
      num.setAttribute('class', 'dial-num');
      num.textContent = String(i);
      letters.appendChild(num);
    }

    CARDS.forEach(function (c) {
      var p = polar(c.a, 92);
      var t = document.createElementNS(SVG_NS, 'text');
      t.setAttribute('x', p.x.toFixed(2));
      t.setAttribute('y', p.y.toFixed(2));
      t.setAttribute('class', 'dial-letter' + (c.cardinal ? ' cardinal' : ''));
      t.textContent = c.t;
      letters.appendChild(t);
    });
  }

  // ═══ Rendering ═══
  function render() {
    if (!bearing && bearing !== 0) {
      $('bearingValue').textContent = '—';
      $('roBearing').textContent = '—';
    } else {
      $('bearingValue').textContent = bearing.toFixed(1);
      $('roBearing').textContent = bearing.toFixed(1) + '°';
      qiblaGroup.setAttribute('transform', 'rotate(' + bearing.toFixed(2) + ' 130 130)');
    }

    // Rotate the rose by -heading so its N points to true north.
    dial.style.transform = 'rotate(' + (hasHeading ? -heading : 0) + 'deg)';

    $('roHeading').textContent = hasHeading ? heading.toFixed(0) + '°' : '—';

    if (bearing !== null && hasHeading) {
      var rel = (bearing - heading + 360) % 360;
      $('roRelative').textContent = rel.toFixed(0) + '°';
      $('hint').innerHTML = 'Pusing badan anda sehingga jarum emas <b>KIBLAT</b> bertemu penanda <b>▲</b> di bahagian atas skrin.';
      $('bearingSub').textContent = 'dari Utara sebenar · ' + rel.toFixed(0) + '° dari hadapan';
    } else if (bearing !== null) {
      $('roRelative').textContent = bearing.toFixed(0) + '°';
      $('hint').innerHTML = 'Carta ini berorientasikan <b>Utara di atas</b>. Kiblat berada pada <b>' + bearing.toFixed(1) + '°</b> dari Utara — hadapkan peranti ke arah itu, atau hidupkan kompas untuk panduan langsung.';
      $('bearingSub').textContent = 'dari Utara sebenar';
    } else {
      $('roRelative').textContent = '—';
    }
  }

  function setLocation(lat, lng, label, persist) {
    if (typeof lat !== 'number' || typeof lng !== 'number' || isNaN(lat) || isNaN(lng)) return;
    loc = { lat: lat, lng: lng, label: label || 'Lokasi tersuai' };
    bearing = qiblaBearing(lat, lng);
    $('locReadout').innerHTML =
      escapeHtml(loc.label) + ' <span>· ' + lat.toFixed(4) + '°N, ' + lng.toFixed(4) + '°E</span>';
    $('latInput').value = lat.toFixed(4);
    $('lngInput').value = lng.toFixed(4);
    if (persist !== false) saveLocation(loc);
    render();
  }

  function setStatus(message, isError) {
    var el = $('locStatus');
    el.textContent = message || '';
    el.classList.toggle('error', !!isError);
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  // ═══ Location: cache in localStorage for offline reuse ═══
  function saveLocation(value) {
    try { localStorage.setItem(STORE_KEY, JSON.stringify(value)); } catch (e) {}
  }

  function loadLocation() {
    try {
      var raw = JSON.parse(localStorage.getItem(STORE_KEY) || 'null');
      if (raw && typeof raw.lat === 'number' && typeof raw.lng === 'number') return raw;
    } catch (e) {}
    return null;
  }

  function detectLocation() {
    if (!navigator.geolocation) {
      setStatus('Pelayar ini tiada API geolokasi. Masukkan koordinat secara manual.', true);
      return;
    }
    setStatus('Sedang mengesan lokasi…');
    $('detectBtn').disabled = true;
    navigator.geolocation.getCurrentPosition(function (pos) {
      $('detectBtn').disabled = false;
      var c = pos.coords;
      setLocation(c.latitude, c.longitude, 'Lokasi GPS');
      setStatus('Lokasi dikesan (ketepatan ±' + Math.round(c.accuracy) + ' m).');
    }, function (err) {
      $('detectBtn').disabled = false;
      var reasons = {
        1: 'Kebenaran ditolak. Benarkan akses lokasi atau masukkan koordinat manual.',
        2: 'Kedudukan tidak tersedia.',
        3: 'Masa tamat semasa mengesan lokasi.'
      };
      setStatus(reasons[err && err.code] || 'Gagal mengesan lokasi.', true);
    }, { enableHighAccuracy: true, timeout: 10000, maximumAge: 600000 });
  }

  // ═══ Device compass ═══
  function screenAngle() {
    if (window.screen && screen.orientation && typeof screen.orientation.angle === 'number') {
      return screen.orientation.angle;
    }
    if (typeof window.orientation === 'number') return (window.orientation + 360) % 360;
    return 0;
  }

  function onOrientation(e) {
    var h = null;
    if (typeof e.webkitCompassHeading === 'number' && !isNaN(e.webkitCompassHeading)) {
      // iOS Safari: already a clockwise heading from (magnetic) north.
      h = e.webkitCompassHeading;
      if (typeof e.webkitCompassAccuracy === 'number' && e.webkitCompassAccuracy >= 0) {
        $('calib').classList.toggle('show', e.webkitCompassAccuracy > 15);
      }
    } else if (typeof e.alpha === 'number' && e.alpha !== null) {
      // alpha is anticlockwise from north; compass heading is clockwise. Add the
      // screen rotation so "up" on the screen, not the device frame, is zero.
      h = ((360 - e.alpha) + screenAngle() + 360) % 360;
    }

    if (h === null) return;

    gotOrientationEvent = true;
    heading = (h % 360 + 360) % 360;
    hasHeading = true;
    render();
  }

  function setSensorStatus(message) {
    $('sensorStatus').textContent = message;
  }

  function startCompass() {
    if (orientationStarted) return;
    if (typeof window.DeviceOrientationEvent === 'undefined') {
      setSensorStatus('Peranti ini tidak menyokong API orientasi. Gunakan carta Utara di atas sebagai panduan.');
      return;
    }

    // iOS 13+ requires an explicit, gesture-triggered permission request.
    if (typeof window.DeviceOrientationEvent.requestPermission === 'function') {
      window.DeviceOrientationEvent.requestPermission().then(function (state) {
        if (state === 'granted') {
          attachOrientation();
          setSensorStatus('Kompas aktif. Putar peranti — helaian carta mengikut Utara.');
        } else {
          setSensorStatus('Kebenaran kompas ditolak. Gunakan carta Utara di atas sebagai panduan.');
        }
      }).catch(function () {
        setSensorStatus('Kebenaran kompas tidak dapat diminta. Gunakan carta Utara di atas.');
      });
      return;
    }

    attachOrientation();
    setSensorStatus('Kompas aktif. Putar peranti — helaian carta mengikut Utara.');
  }

  function attachOrientation() {
    orientationStarted = true;
    window.addEventListener('deviceorientationabsolute', onOrientation, true);
    window.addEventListener('deviceorientation', onOrientation, true);
    window.addEventListener('orientationchange', render, false);

    // If no event arrives, the device has no usable magnetometer.
    window.setTimeout(function () {
      if (!gotOrientationEvent) {
        setSensorStatus('Tiada data sensor diterima. Peranti mungkin tiada magnetometer — gunakan carta Utara di atas.');
      }
    }, 1500);
  }

  // ═══ Wiring ═══
  function init() {
    buildRose();

    $('detectBtn').addEventListener('click', detectLocation);
    $('compassBtn').addEventListener('click', startCompass);

    $('citySelect').addEventListener('change', function () {
      var opt = this.options[this.selectedIndex];
      if (!opt.value) return;
      setLocation(parseFloat(opt.dataset.lat), parseFloat(opt.dataset.lng), opt.textContent);
      setStatus('Lokasi ditetapkan ke ' + opt.textContent + '.');
      this.value = '';
    });

    $('applyBtn').addEventListener('click', function () {
      var lat = parseFloat($('latInput').value);
      var lng = parseFloat($('lngInput').value);
      if (isNaN(lat) || isNaN(lng) || lat < -90 || lat > 90 || lng < -180 || lng > 180) {
        setStatus('Koordinat tidak sah. Latitud -90…90, longitud -180…180.', true);
        return;
      }
      setLocation(lat, lng, 'Koordinat manual');
      setStatus('Koordinat manual digunakan.');
    });

    // Prefer a cached fix, else the Kuala Lumpur default.
    var cached = loadLocation();
    if (cached) {
      setLocation(cached.lat, cached.lng, cached.label);
      setStatus('Menggunakan lokasi terakhir yang disimpan.');
    } else {
      setLocation(DEFAULT_LOC.lat, DEFAULT_LOC.lng, DEFAULT_LOC.label, false);
      setStatus('Contoh lokasi: Kuala Lumpur. Tekan “Kesan Lokasi” untuk ketepatan sebenar.');
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
</script>

</body>
</html>
"""


def _render(**values) -> str:
    html = PAGE
    for key, value in values.items():
        html = html.replace(f"@@{key.upper()}@@", str(value))
    if "@@" in html:
        leftover = sorted({part.split("@@", 1)[0] for part in html.split("@@")[1::2]})
        raise ValueError(f"unsubstituted template markers: {leftover}")
    return html


def render_kiblat(site_origin: str = "") -> str:
    """Render the Qibla finder page."""
    canonical = f"{site_origin}/kiblat/"
    title = "Pencari Arah Kiblat (Qibla)" + _SITE_SUFFIX
    description = (
        "Cari arah kiblat dari lokasi anda menggunakan bearing bulatan besar ke "
        "Kaabah. Berfungsi luar talian dengan kompas peranti atau carta Utara."
    )

    city_options = "".join(
        f'        <option value="{escape(name)}" data-lat="{lat}" data-lng="{lng}">'
        f"{escape(name)}</option>\n"
        for name, lat, lng in CITY_PRESETS
    )

    json_ld = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "Pencari Arah Kiblat",
        "description": description,
        "url": canonical,
        "applicationCategory": "UtilitiesApplication",
        "inLanguage": "ms",
        "operatingSystem": "Any",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "MYR"},
    }

    return _render(
        title=escape(title),
        description=escape(description, quote=True),
        canonical=canonical,
        og_image=f"{site_origin}{_OG_IMAGE_PATH}",
        og_image_width=1024,
        og_image_height=1024,
        og_image_alt=escape(
            "Logo Waktu Solat Malaysia: bulan sabit keemasan, siluet masjid dan "
            "orbit biru di atas latar biru gelap.",
            quote=True,
        ),
        json_ld=json.dumps(json_ld, ensure_ascii=False),
        city_options=city_options,
        kaaba_svg=_KAABA_SVG,
        kaaba_lat=KAABA_LAT,
        kaaba_lng=KAABA_LNG,
        default_lat=DEFAULT_LAT,
        default_lng=DEFAULT_LNG,
    )
