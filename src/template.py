"""Full page template for the SSR worker.

The markup, CSS and interactive JS below mirror index.html so the server
rendered page is pixel-identical to the original PWA. Only the values the
original computes client-side (prayer rows, dates, countdown, zone info) are
injected by entry.py.

Placeholders use @@NAME@@ markers rather than str.format/string.Template so the
embedded JavaScript can keep using template literals without escaping.
"""

PAGE = """<!DOCTYPE html>
<html lang="ms">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<title>@@TITLE@@</title>
<meta name="theme-color" content="#111820">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Waktu Solat">
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
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="@@OG_IMAGE_ALT@@">

<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="@@TITLE@@">
<meta name="twitter:description" content="@@DESCRIPTION@@">
<meta name="twitter:image" content="@@OG_IMAGE@@">
<meta name="twitter:image:alt" content="@@OG_IMAGE_ALT@@">

<!-- PWA -->
<link rel="manifest" href="/manifest.webmanifest">
<link rel="icon" href="/icons/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/icons/icon.svg">

<!-- JSON-LD -->
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

  .status-card{background:linear-gradient(135deg,rgba(42,122,114,.14),rgba(17,24,32,.96));border:1px solid rgba(61,169,159,.24);border-radius:var(--r);padding:14px 16px;margin-bottom:12px;}
  .status-top{display:flex;align-items:center;justify-content:space-between;gap:12px;}
  .status-copy{min-width:0;}
  .status-label{display:block;font-size:10px;letter-spacing:.22em;color:var(--teal-light);text-transform:uppercase;font-weight:600;margin-bottom:0;}
  .status-title{display:none;}
  .status-text{display:none;}
  .status-actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:0;}
  .status-btn{appearance:none;border:none;border-radius:999px;padding:10px 14px;font:inherit;font-size:12px;font-weight:600;cursor:pointer;transition:transform .15s ease,opacity .15s ease,border-color .2s ease;}
  .status-btn.primary{background:var(--gold);color:var(--deep);}
  .status-btn.secondary{background:rgba(255,255,255,.02);color:var(--text);border:1px solid var(--border);}
  .status-btn:disabled{cursor:not-allowed;opacity:.55;transform:none;}
  .status-help{margin-top:10px;padding-top:10px;border-top:1px solid rgba(255,255,255,.06);}
  .status-help-btn{appearance:none;background:none;border:none;color:var(--text-dim);font:inherit;font-size:11px;letter-spacing:.12em;text-transform:uppercase;cursor:pointer;padding:0;}
  .status-help-btn:hover{color:var(--gold-light);}
  .status-list{display:none;margin-top:10px;}
  .status-list.open{display:block;}
  .status-list ol{padding-left:18px;}
  .status-list li{font-size:12px;color:var(--text-dim);line-height:1.7;margin-bottom:6px;}
  .status-list li:last-child{margin-bottom:0;}
  .status-card.hidden{display:none;}
  .zone-wrap{background:var(--panel);border:1px solid var(--border);border-radius:var(--r);padding:14px;margin-bottom:12px;}
  .zone-label{font-size:10px;letter-spacing:.25em;color:var(--gold);text-transform:uppercase;display:block;margin-bottom:8px;font-weight:600;}
  select{width:100%;background:var(--card);border:1px solid var(--border);border-radius:8px;color:var(--text);font-family:inherit;font-size:15px;padding:9px 34px 9px 12px;appearance:none;cursor:pointer;outline:none;transition:border-color .2s;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23c9a84c' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 10px center;}
  select:focus{border-color:var(--gold);}
  #zoneSelect{margin-top:8px;}
  select option{background:var(--deep);}

  .info-note{background:rgba(42,122,114,.1);border:1px solid rgba(42,122,114,.25);border-radius:8px;padding:8px 12px;margin-bottom:12px;font-size:11.5px;color:var(--text-dim);line-height:1.6;font-style:italic;}
  .info-note b{color:var(--gold);font-style:normal;}

  /* ── Announcements (content/announcements) ── */
  .notice{background:rgba(201,168,76,.08);border:1px solid rgba(201,168,76,.28);border-radius:10px;padding:11px 13px;margin-bottom:12px;font-size:12.5px;color:var(--text-dim);line-height:1.6;display:flex;gap:9px;align-items:flex-start;}
  .notice-tag{font-size:8.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--gold);border:1px solid rgba(201,168,76,.3);border-radius:999px;padding:3px 7px;white-space:nowrap;font-weight:600;flex-shrink:0;margin-top:1px;}
  .notice a{color:var(--gold-light);text-decoration:none;}
  .notice a:hover{text-decoration:underline;}

  .date-strip{display:flex;align-items:center;justify-content:space-between;background:var(--gold-dim);border:1px solid var(--border);border-radius:8px;padding:9px 14px;margin-bottom:12px;}
  .date-hijri{font-family:var(--arabic);font-size:14px;color:var(--gold-light);}
  .date-miladi{font-size:13px;color:var(--text-dim);font-style:italic;}
  .date-day{font-size:10px;letter-spacing:.2em;color:var(--text-muted);text-transform:uppercase;font-weight:600;}

  .countdown-card{background:linear-gradient(135deg,var(--teal) 0%,#1d5550 100%);border-radius:var(--r);padding:15px 18px;margin-bottom:12px;display:flex;align-items:center;justify-content:space-between;box-shadow:0 4px 24px rgba(0,0,0,.4);overflow:hidden;position:relative;}
  .countdown-card::after{content:'';position:absolute;right:-20px;top:-20px;width:100px;height:100px;border-radius:50%;background:rgba(255,255,255,.04);}
  .countdown-label{font-size:10px;letter-spacing:.2em;color:rgba(255,255,255,.6);text-transform:uppercase;display:block;margin-bottom:3px;font-weight:600;}
  .countdown-name{font-size:20px;font-weight:600;color:#fff;}
  .countdown-timer{font-size:clamp(20px,5.5vw,26px);color:#fff;letter-spacing:.05em;font-weight:600;}
  .countdown-sub{font-size:11px;color:rgba(255,255,255,.5);text-align:right;margin-top:2px;}

  .legend{display:flex;gap:14px;justify-content:center;margin:8px 0 4px;}
  .legend-item{display:flex;align-items:center;gap:5px;font-size:11px;color:var(--text-dim);}
  .legend-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0;}
  .legend-dot.w{background:var(--gold);}
  .legend-dot.e{background:var(--teal-light);}

  .col-headers{display:grid;grid-template-columns:28px 1fr 78px 78px;gap:0 6px;padding:0 14px 5px;align-items:end;}
  .col-hdr{font-size:8.5px;letter-spacing:.15em;text-transform:uppercase;text-align:right;font-weight:600;}
  .col-hdr.lbl{text-align:left;padding-left:4px;color:var(--text-muted);}
  .col-hdr.cw{color:var(--gold);}
  .col-hdr.ce{color:var(--teal-light);}

  .prayers-grid{display:flex;flex-direction:column;gap:6px;}
  .prayer-row{display:grid;grid-template-columns:28px 1fr 78px 78px;gap:0 6px;align-items:center;background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:10px 14px;position:relative;overflow:hidden;transition:border-color .3s,background .3s;}
  .prayer-row.active{border-color:var(--gold);background:var(--gold-dim);box-shadow:var(--active-glow);}
  .prayer-row.active::before{content:'';position:absolute;left:0;top:0;bottom:0;width:3px;background:linear-gradient(to bottom,var(--gold-light),var(--gold));border-radius:2px 0 0 2px;}
  .prayer-row.dim-row{opacity:.62;}
  .prayer-icon{font-size:17px;text-align:center;}
  .prayer-info{padding-left:2px;}
  .prayer-name-ms{font-size:16px;font-weight:600;color:var(--text);display:block;}
  .prayer-name-ar{font-family:var(--arabic);font-size:11px;color:var(--text-muted);}
  .t-cell{text-align:right;}
  .t-val{font-size:clamp(12px,3.3vw,15px);font-weight:600;letter-spacing:.04em;display:block;}
  .t-val.w{color:var(--gold-light);}
  .t-val.e{color:var(--teal-light);}
  .t-diff{font-size:9px;color:rgba(61,169,159,.65);display:block;margin-top:1px;font-weight:600;}
  .prayer-row.active .prayer-name-ms{color:var(--gold-light);}
  .prayer-row.active .t-val.w{color:#fff;}
  .active-badge{position:absolute;top:5px;right:8px;font-size:7.5px;letter-spacing:.15em;color:var(--gold);text-transform:uppercase;background:var(--gold-dim);border:1px solid rgba(201,168,76,.3);border-radius:20px;padding:2px 6px;font-weight:600;}

  footer{text-align:center;padding:22px 0 0;font-size:11px;color:var(--text-muted);font-style:italic;border-top:1px solid var(--border);margin-top:18px;line-height:1.7;}
  footer span{color:var(--text-dim);}
  .ornament{text-align:center;color:var(--gold);opacity:.4;font-size:18px;margin:6px 0;letter-spacing:.4em;}

  @keyframes fadeUp{from{opacity:0;transform:translateY(12px);}to{opacity:1;transform:translateY(0);}}
  .prayer-row{animation:fadeUp .4s ease both;}
  .prayer-row:nth-child(1){animation-delay:.04s;}.prayer-row:nth-child(2){animation-delay:.08s;}
  .prayer-row:nth-child(3){animation-delay:.12s;}.prayer-row:nth-child(4){animation-delay:.16s;}
  .prayer-row:nth-child(5){animation-delay:.20s;}.prayer-row:nth-child(6){animation-delay:.24s;}
  .prayer-row:nth-child(7){animation-delay:.28s;}

  /* ── Top menu: Artikel | Panduan ── */
  .mainmenu{display:flex;gap:8px;justify-content:center;align-items:center;margin:0 0 14px;font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;font-weight:600;}
  .mainmenu a{color:var(--gold);text-decoration:none;opacity:.7;border:1px solid transparent;border-radius:999px;padding:7px 15px;transition:opacity .2s,border-color .2s,background .2s;}
  .mainmenu a:hover{opacity:1;}
  .mainmenu a.active{opacity:1;border-color:var(--border);background:var(--gold-dim);}

  .offline-chip{display:none;margin:0 auto 12px;width:max-content;max-width:100%;font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:var(--gold-light);border:1px solid rgba(201,168,76,.24);background:rgba(201,168,76,.08);border-radius:999px;padding:7px 10px;font-weight:600;}
  .offline-chip.show{display:block;}

  @media (max-width:560px){
    .status-top{align-items:flex-start;}
  }
</style>
</head>
<body>
<div class="geo"></div>
<div id="app">
  <header>
    <span class="arabic-title">وقت الصلاة</span>
    <div class="latin-title">Waktu Solat Malaysia</div>
    <div class="hline"></div>
  </header>

  <nav class="mainmenu" aria-label="Menu utama">
    <a href="/artikel/">Artikel</a>
    <a href="/panduan/">Panduan</a>
  </nav>

  <div class="status-card" id="installCard">
    <div class="status-top">
      <div class="status-copy">
        <span class="status-label">Pasang Pada Telefon</span>
        <div class="status-title" id="installTitle">Aplikasi ini boleh dipasang untuk penggunaan luar talian</div>
        <p class="status-text" id="installText">Selepas lawatan pertama, fail aplikasi akan disimpan pada peranti. Pilih zon anda, kemudian pasang ke skrin utama untuk akses seperti aplikasi biasa.</p>
      </div>
      <div class="status-actions">
        <button class="status-btn primary" id="installBtn" type="button" hidden>Browser Install</button>
      </div>
    </div>
    <div class="status-help">
      <button class="status-help-btn" id="howToInstallBtn" type="button">Cara Pasang</button>
      <div class="status-list" id="installHelp">
        <ol id="installSteps"></ol>
      </div>
    </div>
  </div>

  <div class="offline-chip" id="offlineChip">Mod luar talian aktif</div>
@@ANNOUNCEMENT@@

  <div class="zone-wrap">
    <span class="zone-label">Pilih Negeri &amp; Zon</span>
    <select id="stateSelect" onchange="changeState(this.value)">
@@STATE_OPTIONS@@    </select>
    <select id="zoneSelect" onchange="changeZone(this.value)">
@@ZONE_OPTIONS@@    </select>
  </div>

  <div class="info-note" id="zoneInfo">@@ZONE_INFO@@</div>

  <div class="date-strip">
    <div>
      <div class="date-hijri" id="hijriDate">@@HIJRI@@</div>
      <div class="date-day" id="dayName">@@DAY_NAME@@</div>
    </div>
    <div class="date-miladi" id="miladiDate">@@MILADI@@</div>
  </div>

  <div class="countdown-card">
    <div>
      <span class="countdown-label">Waktu Solat Seterusnya</span>
      <div class="countdown-name" id="nextPrayerName">@@NEXT_NAME@@</div>
    </div>
    <div>
      <div class="countdown-timer" id="countdownTimer">@@COUNTDOWN@@</div>
      <div class="countdown-sub" id="nextPrayerTime">@@NEXT_TIME@@</div>
    </div>
  </div>

  <div class="legend">
    <div class="legend-item"><div class="legend-dot w"></div><span>Hujung Barat (JAKIM Rasmi)</span></div>
    <div class="legend-item"><div class="legend-dot e"></div><span>Hujung Timur</span></div>
  </div>
  <div class="ornament">✦ ✦ ✦</div>

  <div class="col-headers">
    <div></div>
    <div class="col-hdr lbl">Waktu</div>
    <div class="col-hdr cw">◀ Barat</div>
    <div class="col-hdr ce">Timur ▶</div>
  </div>

  <div class="prayers-grid" id="prayersGrid">
@@PRAYER_ROWS@@  </div>

  <footer>
    <p>Kaedah <span>JAKIM</span> · Anugraha "Mekanika Benda Langit" · MKI Ke-116 (2019)</p>
    <p>Subuh 18°+2′ · Zohor +2′ · Asar +3′ · Maghrib +1′ · Isyak +2′</p>
    <p style="margin-top:8px;opacity:.8;">Oleh <a href="https://kamal.koditi.my/" target="_blank" style="color:var(--gold);text-decoration:none;">kamal.koditi.my</a> · Maklum balas: <a href="https://x.com/k4ml" target="_blank" style="color:var(--gold);text-decoration:none;">@k4ml</a></p>
    <p style="margin-top:10px;"><a href="/panduan/" style="color:var(--gold);text-decoration:none;">Peringatan &amp; Kaedah Pengiraan</a></p>
  </footer>
</div>

<script>
// ═══ Zone navigation ═══
const ZONES_DATA = @@ZONES_DATA@@;
const APP_STORAGE_KEY = 'waktu-solat:selected-zone';

function saveSelection(state, zone) {
  try {
    localStorage.setItem(APP_STORAGE_KEY, JSON.stringify({ state: state, zone: zone }));
  } catch (e) {}
}

function changeState(state) {
  const zones = ZONES_DATA[state];
  const select = document.getElementById('zoneSelect');
  select.innerHTML = zones.map(function (z) { return '<option value="' + z[1] + '">' + z[0] + '</option>'; }).join('');
  changeZone(zones[0][1]);
}

function changeZone(slug) {
  window.location.href = '/zon/' + slug + '/';
}

// Record the zone this page was rendered for, using the same key and shape as
// the original PWA so the selection carries over between the two.
saveSelection(@@CURRENT_STATE@@, @@CURRENT_ZONE@@);

// ═══ Countdown ═══
const NEXT_AT_MS = @@NEXT_AT_MS@@;

function pad2(n) { return String(n).padStart(2, '0'); }

function tickCountdown() {
  const el = document.getElementById('countdownTimer');
  if (!el || !NEXT_AT_MS) return;
  let diff = Math.floor((NEXT_AT_MS - Date.now()) / 1000);
  if (diff < 0) diff += 86400;
  if (diff < 0) { el.textContent = '--:--:--'; return; }
  el.textContent = pad2(Math.floor(diff / 3600)) + ':' + pad2(Math.floor((diff % 3600) / 60)) + ':' + pad2(diff % 60);
}

tickCountdown();
setInterval(tickCountdown, 1000);

// Reload just after midnight so the date and times stay current.
setInterval(function () {
  const n = new Date();
  if (n.getHours() === 0 && n.getMinutes() === 0 && n.getSeconds() < 5) window.location.reload();
}, 5000);

// ═══ Install / offline UI ═══
let installPromptEvent = null;
let isStandalone = false;

function isIos() { return /iphone|ipad|ipod/i.test(navigator.userAgent); }
function isAndroid() { return /android/i.test(navigator.userAgent); }

function detectStandalone() {
  return window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true;
}

function installStepsForDevice() {
  if (isIos()) {
    return [
      'Buka menu Share dalam Safari.',
      'Pilih "Add to Home Screen".',
      'Simpan ikon pada skrin utama untuk buka app tanpa bar alamat.'
    ];
  }
  if (isAndroid()) {
    return [
      'Buka menu pelayar anda.',
      'Pilih "Install app" atau "Add to Home screen".',
      'Sahkan pemasangan supaya waktu solat boleh dibuka seperti app biasa.'
    ];
  }
  return [
    'Buka menu pelayar anda.',
    'Cari pilihan "Install app" atau "Add to Home screen".',
    'Selepas dipasang, buka dari ikon skrin utama untuk pengalaman aplikasi penuh.'
  ];
}

function renderInstallHelp() {
  const steps = installStepsForDevice();
  document.getElementById('installSteps').innerHTML = steps.map(function (step) { return '<li>' + step + '</li>'; }).join('');
}

function updateOfflineChip() {
  document.getElementById('offlineChip').classList.toggle('show', !navigator.onLine);
}

function updateInstallUi() {
  isStandalone = detectStandalone();
  const card = document.getElementById('installCard');
  const installBtn = document.getElementById('installBtn');
  const help = document.getElementById('installHelp');
  const helpBtn = document.getElementById('howToInstallBtn');
  if (isStandalone || !navigator.onLine) {
    card.classList.add('hidden');
    installBtn.hidden = true;
    return;
  }
  card.classList.remove('hidden');
  helpBtn.hidden = false;
  if (installPromptEvent) {
    installBtn.hidden = false;
    installBtn.disabled = false;
    return;
  }
  installBtn.hidden = true;
  if (!navigator.onLine) help.classList.remove('open');
}

function toggleInstallHelp() {
  document.getElementById('installHelp').classList.toggle('open');
}

async function triggerInstall() {
  if (!installPromptEvent) return;
  installPromptEvent.prompt();
  try { await installPromptEvent.userChoice; } catch (e) {}
  installPromptEvent = null;
  updateInstallUi();
}

function registerInstallUi() {
  renderInstallHelp();
  document.getElementById('installBtn').addEventListener('click', triggerInstall);
  document.getElementById('howToInstallBtn').addEventListener('click', toggleInstallHelp);
  window.addEventListener('beforeinstallprompt', function (e) {
    e.preventDefault();
    installPromptEvent = e;
    updateInstallUi();
  });
  window.addEventListener('appinstalled', function () {
    installPromptEvent = null;
    updateInstallUi();
  });
  window.addEventListener('online', function () {
    updateOfflineChip();
    updateInstallUi();
  });
  window.addEventListener('offline', function () {
    updateOfflineChip();
    updateInstallUi();
  });
  updateOfflineChip();
  updateInstallUi();
}

registerInstallUi();

// ═══ Service worker ═══
if ('serviceWorker' in navigator) {
  window.addEventListener('load', function () {
    navigator.serviceWorker.register('/sw.js').catch(function () {});
  });
}
</script>

</body>
</html>
"""


# Social card (og:image / twitter:image). The raster is committed to
# public/og-image.png and served as a static asset; the absolute URL is built by
# the worker from SITE_ORIGIN.
OG_IMAGE_PATH = "/og-image.png"
OG_IMAGE_ALT = (
    "Waktu Solat Malaysia — logo bulan sabit dan siluet masjid, dengan jadual "
    "waktu solat JAKIM bagi 59 zon."
)


def render(**values) -> str:
    """Substitute @@NAME@@ markers in PAGE. Fails loudly on unused or missing markers."""
    html = PAGE
    for key, value in values.items():
        html = html.replace(f"@@{key.upper()}@@", str(value))
    if "@@" in html:
        leftover = sorted({part.split("@@", 1)[0] for part in html.split("@@")[1::2]})
        raise ValueError(f"unsubstituted template markers: {leftover}")
    return html
