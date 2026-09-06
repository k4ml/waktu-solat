"""Cloudflare Worker entry point for Waktu Solat Malaysia - SSR with offline PWA support."""

import json
from datetime import datetime
from urllib.parse import urlparse, parse_qs

from workers import Response, WorkerEntrypoint

from prayer import calc_times, fmt_min, diff_str, to_hijri, PRAYERS, MYT
from zones import ZONES, get_zone_by_code, get_all_zones_flat

# Default zone (most populated area - KL)
DEFAULT_ZONE = "WLY01"


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

    def render_zone_page(self, zone_code: str):
        """Render full HTML page with server-rendered prayer times."""
        result = self.get_zone_times(zone_code)

        if result is None:
            return self.render_zone_selector("Zon tidak ditemui")

        zone_data = get_zone_by_code(zone_code)
        state, zone_name, _ = zone_data

        prayer_rows = ""
        for p in PRAYERS:
            key = p["key"]
            w_time = result["west"]["times"][key]
            e_time = result["east"]["times"][key]
            d = diff_str(_to_minutes(w_time), _to_minutes(e_time))
            dim_class = ' class="dim"' if p["dim"] else ""
            prayer_rows += f"""        <tr{dim_class}>
          <td class="p-name">{p["name"]}</td>
          <td class="p-time west">{w_time}</td>
          <td class="p-time east">{e_time}</td>
          <td class="p-diff">{d}</td>
        </tr>\n"""

        zone_options = self.build_zone_options(zone_name)

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
                        "name": pr["name"],
                        "description": f"{result['west']['times'][pr['key']]} ({result['west']['label']})",
                    }
                    for i, pr in enumerate(PRAYERS)
                ],
            },
        }

        html = f"""<!DOCTYPE html>
<html lang="ms">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
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
  <meta name="theme-color" content="#0d1b2a">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="Waktu Solat">

  <!-- JSON-LD -->
  <script type="application/ld+json">{json.dumps(json_ld, ensure_ascii=False)}</script>

  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🕌</text></svg>">

  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: #0d1b2a;
      color: #e0e1dd;
      min-height: 100vh;
      padding: 1rem;
    }}
    .container {{ max-width: 480px; margin: 0 auto; }}
    h1 {{ font-size: 1.25rem; margin-bottom: 0.5rem; color: #ffd166; }}
    .date-strip {{ font-size: 0.875rem; color: #778da9; margin-bottom: 1rem; }}
    .zone-select {{ margin-bottom: 1rem; }}
    select {{
      width: 100%;
      padding: 0.75rem;
      border-radius: 8px;
      border: 1px solid #415a77;
      background: #1b263b;
      color: #e0e1dd;
      font-size: 0.875rem;
    }}
    .prayer-table {{
      width: 100%;
      border-collapse: collapse;
      background: #1b263b;
      border-radius: 12px;
      overflow: hidden;
    }}
    .prayer-table th {{
      background: #415a77;
      padding: 0.75rem 0.5rem;
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    .prayer-table td {{
      padding: 0.875rem 0.5rem;
      border-bottom: 1px solid #0d1b2a;
      text-align: center;
    }}
    .prayer-table tr:last-child td {{ border-bottom: none; }}
    .prayer-table tr.dim {{ opacity: 0.6; }}
    .p-name {{ text-align: left !important; font-weight: 500; }}
    .p-time {{ font-variant-numeric: tabular-nums; font-size: 1.125rem; }}
    .p-time.west {{ color: #ffd166; }}
    .p-time.east {{ color: #06d6a0; }}
    .p-diff {{ font-size: 0.75rem; color: #778da9; }}
    .legend {{ display: flex; gap: 1rem; margin: 0.75rem 0; font-size: 0.75rem; color: #778da9; }}
    .legend span::before {{ content: "● "; }}
    .legend .west::before {{ color: #ffd166; }}
    .legend .east::before {{ color: #06d6a0; }}
    .footer {{ margin-top: 1.5rem; font-size: 0.75rem; color: #778da9; text-align: center; }}
    .footer a {{ color: #ffd166; }}
    .offline-badge {{ display: none; background: #e63946; color: white; padding: 0.5rem; border-radius: 8px; text-align: center; margin-bottom: 1rem; font-size: 0.875rem; }}
    @media (max-width: 360px) {{
      .p-time {{ font-size: 1rem; }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <h1>🕌 Waktu Solat Malaysia</h1>
    <div class="date-strip">{result['hijri']} • {result['date']}</div>

    <div class="offline-badge" id="offlineBadge">📡 Luar talian - Menggunakan data cache</div>

    <div class="zone-select">
      <select id="zoneSelect" onchange="changeZone(this.value)">
{zone_options}
      </select>
    </div>

    <div class="legend">
      <span class="west">Barat ({result['west']['label']})</span>
      <span class="east">Timur ({result['east']['label']})</span>
    </div>

    <table class="prayer-table">
      <thead>
        <tr>
          <th></th>
          <th>Barat</th>
          <th>Timur</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
{prayer_rows}      </tbody>
    </table>

    <div class="footer">
      <p>Kiraan menggunakan kaedah JAKIM (MKI Ke-116, 2019)</p>
      <p><a href="/">Semua Zon</a></p>
    </div>
  </div>

  <script>
    if ('serviceWorker' in navigator) {{
      navigator.serviceWorker.register('/sw.js');
    }}
    function changeZone(code) {{
      window.location.href = '/zone/' + code;
    }}
    function updateOnlineStatus() {{
      var badge = document.getElementById('offlineBadge');
      if (badge) {{
        badge.style.display = navigator.onLine ? 'none' : 'block';
      }}
    }}
    window.addEventListener('online', updateOnlineStatus);
    window.addEventListener('offline', updateOnlineStatus);
    updateOnlineStatus();
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
  <meta name="description" content="Waktu solat untuk semua zon di Malaysia. Kiraan menggunakan kaedah JAKIM (MKI Ke-116, 2019).">
  <meta property="og:title" content="Waktu Solat Malaysia">
  <meta property="og:description" content="Waktu solat untuk semua zon di Malaysia">
  <style>
    body {{ font-family: sans-serif; background: #0d1b2a; color: #e0e1dd; padding: 1rem; }}
    .container {{ max-width: 480px; margin: 0 auto; }}
    h1 {{ color: #ffd166; margin-bottom: 1rem; }}
    select {{ width: 100%; padding: 1rem; border-radius: 8px; background: #1b263b; color: #e0e1dd; border: 1px solid #415a77; font-size: 1rem; }}
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

    def build_zone_options(self, selected_zone: str) -> str:
        """Build HTML options for zone selector."""
        options = ""
        for state, zones in ZONES.items():
            for zone_name, data in zones.items():
                code = data["zone"]
                selected = " selected" if zone_name == selected_zone else ""
                label = zone_name.split(" - ", 1)[1] if " - " in zone_name else zone_name
                options += f'        <option value="{code}"{selected}>{state} - {label}</option>\n'
        return options

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
            "background_color": "#0d1b2a",
            "theme_color": "#0d1b2a",
            "lang": "ms",
            "icons": [
                {
                    "src": "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🕌</text></svg>",
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
