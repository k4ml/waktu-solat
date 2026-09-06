"""Cloudflare Worker entry point for Waktu Solat Malaysia - SSR with offline PWA support."""

import json
from datetime import datetime
from urllib.parse import urlparse, parse_qs

from workers import Response, WorkerEntrypoint

from prayer import calc_times, fmt_min, diff_str, to_hijri, MYT
from zones import ZONES, get_zone_by_code, get_all_zones_flat

# Default zone (most populated area - KL)
DEFAULT_ZONE = "WLY01"

# Prayer metadata with Arabic names (matching original design)
PRAYERS = [
    {"key": "imsak", "name": "Imsak", "ar": "إمساك", "dim": True},
    {"key": "fajr", "name": "Subuh", "ar": "الفجر", "dim": False},
    {"key": "syuruk", "name": "Syuruk", "ar": "الشروق", "dim": True},
    {"key": "dhuhr", "name": "Zohor", "ar": "الظهر", "dim": False},
    {"key": "asr", "name": "Asar", "ar": "العصر", "dim": False},
    {"key": "maghrib", "name": "Maghrib", "ar": "المغرب", "dim": False},
    {"key": "isyak", "name": "Isyak", "ar": "العشاء", "dim": False},
]

# Active prayers (highlighted)
ACTIVE_KEYS = ["fajr", "dhuhr", "asr", "maghrib", "isyak"]


class Default(WorkerEntrypoint):
    """Main Worker entry point."""

    async def fetch(self, request):
        """Handle incoming requests."""
        url = urlparse(request.url)
        path = url.path

        # API endpoint for JSON data
        if path.startswith("/api/zone/"):
            zone_code = path.split("/")[-1].upper()
            return self.api_zone(zone_code)

        # Service worker
        if path == "/sw.js":
            return self.serve_sw_js()

        # Manifest
        if path == "/manifest.webmanifest":
            return self.serve_manifest()

        # Zone page: /zone/JHR02
        if path.startswith("/zone/"):
            zone_code = path.split("/")[-1].upper()
            return self.render_zone_page(zone_code)

        # Root - default zone
        if path == "/" or path == "":
            params = parse_qs(url.query)
            zone_param = params.get("zone", [None])[0]
            if zone_param:
                return self.render_zone_page(zone_param.upper())
            return self.render_zone_page(DEFAULT_ZONE)

        return Response("Not Found", status=404)

    def api_zone(self, zone_code: str):
        """Return prayer times as JSON API."""
        result = self.get_zone_times(zone_code)
        if result is None:
            return Response(
                json.dumps({"error": "Zone not found"}),
                status=404,
                headers={"Content-Type": "application/json"},
            )

        return Response(
            json.dumps(result),
            headers={
                "Content-Type": "application/json",
                "Cache-Control": "public, max-age=3600",
            },
        )

    def get_zone_times(self, zone_code: str):
        """Calculate prayer times for a zone."""
        found = get_zone_by_code(zone_code)
        if found is None:
            return None

        state, zone_name, data = found
        now = datetime.now(MYT)
        elev = data.get("elev", 10)

        west_times = calc_times(
            now, data["west"]["lat"], data["west"]["lng"], data["tz"], elev
        )
        east_times = calc_times(
            now, data["east"]["lat"], data["east"]["lng"], data["tz"], elev
        )

        return {
            "zone": zone_code,
            "state": state,
            "zone_name": zone_name,
            "date": now.strftime("%Y-%m-%d"),
            "hijri": to_hijri(now),
            "west": {
                "label": data["west"]["label"],
                "times": {k: fmt_min(v) for k, v in west_times.items()},
            },
            "east": {
                "label": data["east"]["label"],
                "times": {k: fmt_min(v) for k, v in east_times.items()},
            },
        }

    def get_next_prayer(self, zone_code: str, now: datetime):
        """Calculate the next prayer time.
        
        Returns (prayer_name, prayer_time_str, minutes_until).
        """
        found = get_zone_by_code(zone_code)
        if found is None:
            return None, None, None

        _, _, data = found
        elev = data.get("elev", 10)
        times = calc_times(now, data["west"]["lat"], data["west"]["lng"], data["tz"], elev)

        # Current minutes since midnight
        current_min = now.hour * 60 + now.minute

        # Find next prayer (skip imsak and syuruk for next prayer display)
        next_prayer_key = None
        next_prayer_min = None
        for p in PRAYERS:
            key = p["key"]
            if key in ("imsak", "syuruk"):
                continue
            t = times[key]
            if t is not None and t > current_min:
                next_prayer_key = key
                next_prayer_min = t
                break

        # If no more prayers today, show tomorrow's Fajr
        if next_prayer_key is None:
            next_prayer_key = "fajr"
            next_prayer_min = times["fajr"]
            if next_prayer_min is not None:
                # Add 24 hours (1440 min) for tomorrow
                next_prayer_min += 1440

        if next_prayer_key is None:
            return None, None, None

        # Get prayer name in Malay
        prayer_names = {
            "fajr": "Subuh",
            "dhuhr": "Zohor",
            "asr": "Asar",
            "maghrib": "Maghrib",
            "isyak": "Isyak",
        }
        name = prayer_names.get(next_prayer_key, next_prayer_key)

        # Calculate minutes until
        if next_prayer_min >= 1440:
            mins_until = next_prayer_min - 1440 - current_min + 1440
        else:
            mins_until = next_prayer_min - current_min

        # Format time
        display_min = next_prayer_min % 1440
        time_str = f"{display_min // 60:02d}:{display_min % 60:02d}"

        return name, time_str, mins_until

    def render_zone_page(self, zone_code: str):
        """Render full HTML page matching original design."""
        result = self.get_zone_times(zone_code)

        if result is None:
            return self.render_zone_selector("Zon tidak ditemui")

        zone_data = get_zone_by_code(zone_code)
        state, zone_name, _ = zone_data
        now = datetime.now(MYT)

        # Get next prayer
        next_name, next_time, mins_until = self.get_next_prayer(zone_code, now)
        if next_name is None:
            next_name = "—"
            next_time = "—"
            mins_until = 0

        # Build state options
        state_options = ""
        for s in ZONES.keys():
            selected = " selected" if s == state else ""
            state_options += f'        <option value="{s}"{selected}>{s}</option>\n'

        # Build zone options for this state
        zone_options = ""
        for zn, data in ZONES[state].items():
            code = data["zone"]
            selected = " selected" if zn == zone_name else ""
            zone_options += f'        <option value="{code}"{selected}>{zn}</option>\n'

        # Build prayer rows
        prayer_rows = ""
        for i, p in enumerate(PRAYERS):
            key = p["key"]
            w_time = result["west"]["times"][key]
            e_time = result["east"]["times"][key]
            d = diff_str(_to_minutes(w_time), _to_minutes(e_time))
            is_active = key in ACTIVE_KEYS
            active_class = " active" if is_active else ""
            dim_class = " dim-row" if p["dim"] else ""
            active_badge = '<span class="active-badge">Aktif</span>' if is_active else ""
            delay = i * 0.04

            prayer_rows += f"""      <div class="prayer-row{active_class}{dim_class}" style="animation-delay:{delay:.2f}s">
        <div class="prayer-icon">{self._prayer_icon(key)}</div>
        <div class="prayer-info">
          <span class="prayer-name-ms">{p["name"]}</span>
          <span class="prayer-name-ar">{p["ar"]}</span>
        </div>
        <div class="t-cell">
          <span class="t-val w">{w_time}</span>
          <span class="t-diff">{d}</span>
        </div>
        <div class="t-cell">
          <span class="t-val e">{e_time}</span>
        </div>
        {active_badge}
      </div>\n"""

        location = zone_name.split(" - ", 1)[1] if " - " in zone_name else zone_name
        title = f"Waktu Solat {location} - {result['date']}"
        description = (
            f"Waktu solat hari ini di {location}, {state}. "
            f"Subuh {result['west']['times']['fajr']}, "
            f"Zohor {result['west']['times']['dhuhr']}, "
            f"Asar {result['west']['times']['asr']}, "
            f"Maghrib {result['west']['times']['maghrib']}, "
            f"Isyak {result['west']['times']['isyak']}."
        )

        json_ld = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": title,
            "description": description,
            "datePublished": result["date"],
            "mainEntity": {
                "@type": "ItemList",
                "name": f"Waktu Solat {location}",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": i + 1,
                        "name": p["name"],
                        "description": f"{result['west']['times'][p['key']]} ({result['west']['label']})",
                    }
                    for i, p in enumerate(PRAYERS)
                ],
            },
        }

        html = f"""<!DOCTYPE html>
<html lang="ms">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<title>Waktu Solat Malaysia</title>
<meta name="theme-color" content="#111820">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Waktu Solat">
<meta name="mobile-web-app-capable" content="yes">
<meta name="description" content="{description}">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:locale" content="ms_MY">

<!-- Twitter -->
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">

<!-- PWA -->
<link rel="manifest" href="/manifest.webmanifest">
<link rel="icon" href="icons/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="icons/icon.svg">

<!-- JSON-LD -->
<script type="application/ld+json">{json.dumps(json_ld, ensure_ascii=False)}</script>

<style>
:root {{
    --ink:#0d1117; --deep:#111820; --panel:#161e27; --card:#1c2733;
    --border:rgba(180,145,80,0.2); --gold:#c9a84c; --gold-light:#e8c97a;
    --gold-dim:rgba(201,168,76,0.12); --teal:#2a7a72; --teal-light:#3da99f;
    --text:#e8e0d0; --text-dim:rgba(232,224,208,0.55); --text-muted:rgba(232,224,208,0.3);
    --active-glow:0 0 30px rgba(201,168,76,0.25); --r:12px;
    --sans:'Segoe UI',system-ui,sans-serif;
    --arabic:'Noto Naskh Arabic','Amiri','Scheherazade New','Times New Roman',serif;
}}
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0;}}
body{{background:var(--ink);color:var(--text);font-family:var(--sans);min-height:100vh;overflow-x:hidden;}}
body::before{{content:'';position:fixed;inset:0;z-index:0;background:radial-gradient(ellipse 80% 50% at 50% -10%,rgba(42,122,114,.18) 0%,transparent 60%),radial-gradient(ellipse 60% 40% at 100% 100%,rgba(201,168,76,.08) 0%,transparent 55%);pointer-events:none;}}
.geo{{position:fixed;inset:0;z-index:0;opacity:.04;pointer-events:none;background-image:repeating-linear-gradient(60deg,var(--gold) 0,var(--gold) 1px,transparent 0,transparent 50%),repeating-linear-gradient(-60deg,var(--gold) 0,var(--gold) 1px,transparent 0,transparent 50%),repeating-linear-gradient(0deg,var(--gold) 0,var(--gold) 1px,transparent 0,transparent 50%);background-size:60px 60px;}}
#app{{position:relative;z-index:1;max-width:540px;margin:0 auto;padding:0 14px 60px;}}

header{{text-align:center;padding:32px 0 18px;}}
.arabic-title{{font-family:var(--arabic);font-size:clamp(26px,7vw,40px);color:var(--gold);line-height:1.3;display:block;margin-bottom:4px;}}
.latin-title{{font-size:clamp(10px,3vw,13px);letter-spacing:.3em;color:var(--text-dim);text-transform:uppercase;font-weight:600;}}
.hline{{width:80px;height:1px;background:linear-gradient(to right,transparent,var(--gold),transparent);margin:12px auto 0;}}

.offline-chip{{display:none;margin:0 auto 12px;width:max-content;max-width:100%;font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:var(--gold-light);border:1px solid rgba(201,168,76,.24);background:rgba(201,168,76,.08);border-radius:999px;padding:7px 10px;font-weight:600;}}
.offline-chip.show{{display:block;}}

.zone-wrap{{background:var(--panel);border:1px solid var(--border);border-radius:var(--r);padding:14px;margin-bottom:12px;}}
.zone-label{{font-size:10px;letter-spacing:.25em;color:var(--gold);text-transform:uppercase;display:block;margin-bottom:8px;font-weight:600;}}
select{{width:100%;background:var(--card);border:1px solid var(--border);border-radius:8px;color:var(--text);font-family:inherit;font-size:15px;padding:9px 34px 9px 12px;appearance:none;cursor:pointer;outline:none;transition:border-color .2s;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23c9a84c' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 10px center;}}
select:focus{{border-color:var(--gold);}}
#zoneSelect{{margin-top:8px;}}
select option{{background:var(--deep);}}

.info-note{{background:rgba(42,122,114,.1);border:1px solid rgba(42,122,114,.25);border-radius:8px;padding:8px 12px;margin-bottom:12px;font-size:11.5px;color:var(--text-dim);line-height:1.6;font-style:italic;}}
.info-note b{{color:var(--gold);font-style:normal;}}

.date-strip{{display:flex;align-items:center;justify-content:space-between;background:var(--gold-dim);border:1px solid var(--border);border-radius:8px;padding:9px 14px;margin-bottom:12px;}}
.date-hijri{{font-family:var(--arabic);font-size:14px;color:var(--gold-light);}}
.date-miladi{{font-size:13px;color:var(--text-dim);font-style:italic;}}
.date-day{{font-size:10px;letter-spacing:.2em;color:var(--text-muted);text-transform:uppercase;font-weight:600;}}

.countdown-card{{background:linear-gradient(135deg,var(--teal) 0%,#1d5550 100%);border-radius:var(--r);padding:15px 18px;margin-bottom:12px;display:flex;align-items:center;justify-content:space-between;box-shadow:0 4px 24px rgba(0,0,0,.4);overflow:hidden;position:relative;}}
.countdown-card::after{{content:'';position:absolute;right:-20px;top:-20px;width:100px;height:100px;border-radius:50%;background:rgba(255,255,255,.04);}}
.countdown-label{{font-size:10px;letter-spacing:.2em;color:rgba(255,255,255,.6);text-transform:uppercase;display:block;margin-bottom:3px;font-weight:600;}}
.countdown-name{{font-size:20px;font-weight:600;color:#fff;}}
.countdown-timer{{font-size:clamp(20px,5.5vw,26px);color:#fff;letter-spacing:.05em;font-weight:600;}}
.countdown-sub{{font-size:11px;color:rgba(255,255,255,.5);text-align:right;margin-top:2px;}}

.legend{{display:flex;gap:14px;justify-content:center;margin:8px 0 4px;}}
.legend-item{{display:flex;align-items:center;gap:5px;font-size:11px;color:var(--text-dim);}}
.legend-dot{{width:8px;height:8px;border-radius:50%;flex-shrink:0;}}
.legend-dot.w{{background:var(--gold);}}
.legend-dot.e{{background:var(--teal-light);}}

.col-headers{{display:grid;grid-template-columns:28px 1fr 78px 78px;gap:0 6px;padding:0 14px 5px;align-items:end;}}
.col-hdr{{font-size:8.5px;letter-spacing:.15em;text-transform:uppercase;text-align:right;font-weight:600;}}
.col-hdr.lbl{{text-align:left;padding-left:4px;color:var(--text-muted);}}
.col-hdr.cw{{color:var(--gold);}}
.col-hdr.ce{{color:var(--teal-light);}}

.prayers-grid{{display:flex;flex-direction:column;gap:6px;}}
.prayer-row{{display:grid;grid-template-columns:28px 1fr 78px 78px;gap:0 6px;align-items:center;background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:10px 14px;position:relative;overflow:hidden;transition:border-color .3s,background .3s;}}
.prayer-row.active{{border-color:var(--gold);background:var(--gold-dim);box-shadow:var(--active-glow);}}
.prayer-row.active::before{{content:'';position:absolute;left:0;top:0;bottom:0;width:3px;background:linear-gradient(to bottom,var(--gold-light),var(--gold));border-radius:2px 0 0 2px;}}
.prayer-row.dim-row{{opacity:.62;}}
.prayer-icon{{font-size:17px;text-align:center;}}
.prayer-info{{padding-left:2px;}}
.prayer-name-ms{{font-size:16px;font-weight:600;color:var(--text);display:block;}}
.prayer-name-ar{{font-family:var(--arabic);font-size:11px;color:var(--text-muted);}}
.t-cell{{text-align:right;}}
.t-val{{font-size:clamp(12px,3.3vw,15px);font-weight:600;letter-spacing:.04em;display:block;}}
.t-val.w{{color:var(--gold-light);}}
.t-val.e{{color:var(--teal-light);}}
.t-diff{{font-size:9px;color:rgba(61,169,159,.65);display:block;margin-top:1px;font-weight:600;}}
.prayer-row.active .prayer-name-ms{{color:var(--gold-light);}}
.prayer-row.active .t-val.w{{color:#fff;}}
.active-badge{{position:absolute;top:5px;right:8px;font-size:7.5px;letter-spacing:.15em;color:var(--gold);text-transform:uppercase;background:var(--gold-dim);border:1px solid rgba(201,168,76,.3);border-radius:20px;padding:2px 6px;font-weight:600;}}

footer{{text-align:center;padding:22px 0 0;font-size:11px;color:var(--text-muted);font-style:italic;border-top:1px solid var(--border);margin-top:18px;line-height:1.7;}}
footer span{{color:var(--text-dim);}}
.ornament{{text-align:center;color:var(--gold);opacity:.4;font-size:18px;margin:6px 0;letter-spacing:.4em;}}

@keyframes fadeUp{{from{{opacity:0;transform:translateY(12px);}}to{{opacity:1;transform:translateY(0);}}}}
.prayer-row{{animation:fadeUp .4s ease both;}}
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

  <div class="offline-chip" id="offlineChip">Mod luar talian aktif</div>

  <div class="zone-wrap">
    <span class="zone-label">Pilih Negeri &amp; Zon</span>
    <select id="stateSelect" onchange="changeState(this.value)">
{state_options}    </select>
    <select id="zoneSelect" onchange="changeZone(this.value)">
{zone_options}    </select>
  </div>

  <div class="info-note" id="zoneInfo">
    <b>{result['zone']}</b> · {state} · {result['west']['label']} ({result['west']['label']}) — {result['east']['label']} ({result['east']['label']})
  </div>

  <div class="date-strip">
    <div>
      <div class="date-hijri" id="hijriDate">{result['hijri']}</div>
      <div class="date-day" id="dayName">{["Isnin","Selasa","Rabu","Khamis","Jumaat","Sabtu","Ahad"][now.weekday()]}</div>
    </div>
    <div class="date-miladi" id="miladiDate">{result['date']}</div>
  </div>

  <div class="countdown-card">
    <div>
      <span class="countdown-label">Waktu Solat Seterusnya</span>
      <div class="countdown-name" id="nextPrayerName">{next_name}</div>
    </div>
    <div>
      <div class="countdown-timer" id="countdownTimer">{f"{mins_until//60:02d}:{mins_until%60:02d}" if mins_until else "—"}</div>
      <div class="countdown-sub" id="nextPrayerTime">{next_time}</div>
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
{prayer_rows}  </div>

  <footer>
    <p>Kaedah <span>JAKIM</span> · Anugraha "Mekanika Benda Langit" · MKI Ke-116 (2019)</p>
    <p>Subuh 18°+2′ · Zohor +2′ · Asar +3′ · Maghrib +1′ · Isyak +2′</p>
    <p style="margin-top:8px;opacity:.8;">Oleh <a href="https://kamal.koditi.my/" target="_blank" style="color:var(--gold);text-decoration:none;">kamal.koditi.my</a></p>
  </footer>
</div>

<script>
// Zone navigation
const ZONES_DATA = {json.dumps({s: list(ZONES[s].keys()) for s in ZONES}, ensure_ascii=False)};

function changeState(state) {{
  const zones = ZONES_DATA[state];
  const select = document.getElementById('zoneSelect');
  select.innerHTML = zones.map(z => '<option value="' + z.split(' - ')[0] + '">' + z + '</option>').join('');
  changeZone(zones[0].split(' - ')[0]);
}}

function changeZone(code) {{
  window.location.href = '/zone/' + code;
}}

// Offline detection
function updateOnlineStatus() {{
  var chip = document.getElementById('offlineChip');
  if (chip) chip.classList.toggle('show', !navigator.onLine);
}}
window.addEventListener('online', updateOnlineStatus);
window.addEventListener('offline', updateOnlineStatus);
updateOnlineStatus();

// Register service worker
if ('serviceWorker' in navigator) {{
  navigator.serviceWorker.register('/sw.js');
}}
</script>
</body>
</html>"""

        return Response(
            html,
            headers={
                "Content-Type": "text/html; charset=utf-8",
                "Cache-Control": "public, max-age=300",
            },
        )

    def render_zone_selector(self, message: str = ""):
        """Render page showing all available zones."""
        zones = get_all_zones_flat()
        options = ""
        for z in zones:
            options += f'        <option value="{z["zone"]}">{z["state"]} - {z["zone_name"]}</option>\n'

        html = f"""<!DOCTYPE html>
<html lang="ms">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Waktu Solat Malaysia - Pilih Zon</title>
  <meta name="description" content="Waktu solat untuk semua zon di Malaysia.">
  <style>
    :root {{ --ink:#0d1117; --deep:#111820; --gold:#c9a84c; --text:#e8e0d0; --text-dim:rgba(232,224,208,0.55); --border:rgba(180,145,80,0.2); }}
    body {{ font-family: 'Segoe UI', sans-serif; background: var(--ink); color: var(--text); padding: 1rem; }}
    .container {{ max-width: 480px; margin: 0 auto; }}
    h1 {{ color: var(--gold); margin-bottom: 1rem; text-align: center; }}
    select {{ width: 100%; padding: 1rem; border-radius: 8px; background: var(--deep); color: var(--text); border: 1px solid var(--border); font-size: 1rem; }}
    .msg {{ color: #e63946; margin-bottom: 1rem; }}
  </style>
</head>
<body>
  <div class="container">
    <h1>🕌 Waktu Solat Malaysia</h1>
    <p class="msg">{message}</p>
    <select onchange="if(this.value) window.location.href='/zone/'+this.value">
      <option value="">Pilih Zon...</option>
{options}    </select>
  </div>
</body>
</html>"""
        return Response(html, headers={"Content-Type": "text/html; charset=utf-8"})

    def _prayer_icon(self, key: str) -> str:
        """Return emoji icon for prayer."""
        icons = {
            "imsak": "🌙",
            "fajr": "🌅",
            "syuruk": "☀️",
            "dhuhr": "🌤️",
            "asr": "⛅",
            "maghrib": "🌇",
            "isyak": "🌃",
        }
        return icons.get(key, "")

    def serve_sw_js(self):
        """Serve service worker for offline caching."""
        sw_js = """
const CACHE_NAME = 'waktu-solat-v1';
const APP_SHELL = [
  '/',
  '/manifest.webmanifest'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(APP_SHELL))
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  if (url.origin !== location.origin) return;
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(fetch(event.request));
    return;
  }
  event.respondWith(
    caches.open(CACHE_NAME).then(cache => {
      return cache.match(event.request).then(cached => {
        const networkFetch = fetch(event.request).then(response => {
          cache.put(event.request, response.clone());
          return response;
        }).catch(() => cached);
        return cached || networkFetch;
      });
    })
  );
});
"""
        return Response(
            sw_js,
            headers={
                "Content-Type": "application/javascript",
                "Cache-Control": "no-cache",
            },
        )

    def serve_manifest(self):
        """Serve PWA manifest."""
        manifest = {
            "name": "Waktu Solat Malaysia",
            "short_name": "Waktu Solat",
            "description": "Waktu solat untuk semua zon di Malaysia",
            "start_url": "/",
            "scope": "/",
            "display": "standalone",
            "orientation": "portrait",
            "background_color": "#0d1117",
            "theme_color": "#111820",
            "lang": "ms",
            "icons": [
                {
                    "src": "icons/icon.svg",
                    "sizes": "any",
                    "type": "image/svg+xml",
                    "purpose": "any maskable",
                }
            ],
        }
        return Response(
            json.dumps(manifest),
            headers={"Content-Type": "application/manifest+json"},
        )


def _to_minutes(time_str: str):
    """Convert HH:MM string to minutes, or None if invalid."""
    if time_str == "--:--":
        return None
    parts = time_str.split(":")
    return int(parts[0]) * 60 + int(parts[1])
