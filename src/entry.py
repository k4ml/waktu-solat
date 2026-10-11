"""Cloudflare Worker entry point for Waktu Solat Malaysia - SSR with offline PWA support."""

import json
from datetime import datetime, timedelta
from html import escape
from urllib.parse import urlparse, parse_qs

from workers import Response, WorkerEntrypoint

from prayer import calc_times, fmt_min, diff_str, to_hijri, MYT
from template import render as render_template
from zones import ZONES, get_zone_by_code, get_all_zones_flat

# Default zone - the original PWA opens on Johor (JHR02).
DEFAULT_ZONE = "JHR02"

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
PRAYER_NAMES = {p["key"]: p["name"] for p in PRAYERS}
PRAYER_ICONS = {
    "imsak": "🌙",
    "fajr": "🌅",
    "syuruk": "☀️",
    "dhuhr": "🌤️",
    "asr": "⛅",
    "maghrib": "🌇",
    "isyak": "🌃",
}

# The five obligatory prayers: highlighted when current, and used for the next
# prayer countdown. Imsak and Syuruk are excluded, as in the original.
ACTIVE_KEYS = ["fajr", "dhuhr", "asr", "maghrib", "isyak"]

DAY_NAMES = ["Isnin", "Selasa", "Rabu", "Khamis", "Jumaat", "Sabtu", "Ahad"]
MONTH_NAMES = ["Jan", "Feb", "Mac", "Apr", "Mei", "Jun", "Jul", "Ogo", "Sep", "Okt", "Nov", "Dis"]


class Default(WorkerEntrypoint):
    """Main Worker entry point."""

    async def fetch(self, request):
        """Handle incoming requests."""
        url = urlparse(request.url)
        base_url = f"{url.scheme}://{url.netloc}"

        # Force trailing slash on page URLs (SEO canonicalization).
        original_path = url.path or "/"
        if (
            original_path not in ("/", "")
            and not original_path.endswith("/")
            and "." not in original_path.rsplit("/", 1)[-1]
        ):
            new_url = f"{base_url}{original_path}/"
            if url.query:
                new_url += f"?{url.query}"
            return Response("", status=301, headers={"Location": new_url})

        path = original_path.rstrip("/") or "/"

        # API endpoint for JSON data
        if path.startswith("/api/zone/"):
            return self.api_zone(path.split("/")[-1].upper())

        # Service worker
        if path == "/sw.js":
            return self.serve_sw_js()

        # Manifest
        if path == "/manifest.webmanifest":
            return self.serve_manifest()

        # Zone page: /zone/JHR02
        if path.startswith("/zone/"):
            return self.render_zone_page(path.split("/")[-1].upper(), base_url)

        # Root - default zone, overridable with ?zone=JHR02
        if path == "/":
            zone_param = parse_qs(url.query).get("zone", [None])[0]
            return self.render_zone_page((zone_param or DEFAULT_ZONE).upper(), base_url)

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
        return self.build_times(found, datetime.now(MYT))

    def build_times(self, found, now: datetime):
        """Build the per-zone times payload from a (state, zone_name, data) tuple."""
        state, zone_name, data = found
        elev = data.get("elev", 10)

        west_times = calc_times(
            now, data["west"]["lat"], data["west"]["lng"], data["tz"], elev
        )
        east_times = calc_times(
            now, data["east"]["lat"], data["east"]["lng"], data["tz"], elev
        )

        return {
            "zone": data["zone"],
            "state": state,
            "zone_name": zone_name,
            "date": now.strftime("%Y-%m-%d"),
            "hijri": to_hijri(now),
            "west": {
                "label": data["west"]["label"],
                "lat": data["west"]["lat"],
                "lng": data["west"]["lng"],
                "times": {k: fmt_min(v) for k, v in west_times.items()},
            },
            "east": {
                "label": data["east"]["label"],
                "lat": data["east"]["lat"],
                "lng": data["east"]["lng"],
                "times": {k: fmt_min(v) for k, v in east_times.items()},
            },
        }

    def active_prayer(self, west_min: dict, now: datetime):
        """Current prayer period, matching the original render().

        Returns the last obligatory prayer whose time has passed, or None before
        Subuh.
        """
        now_min = now.hour * 60 + now.minute + now.second / 60
        for key in reversed(ACTIVE_KEYS):
            t = west_min.get(key)
            if t is not None and now_min >= t:
                return key
        return None

    def next_prayer(self, west_min: dict, now: datetime, data: dict):
        """Next prayer after `now` on the west (official) times.

        Returns (key, minutes_from_local_midnight). The minutes exceed 1440 when
        the next prayer is tomorrow's Fajr, matching the original countdown.
        """
        now_min = now.hour * 60 + now.minute + now.second / 60
        for key in ACTIVE_KEYS:
            t = west_min.get(key)
            if t is not None and now_min < t:
                return key, t

        # Nothing left today: use tomorrow's Fajr, computed for tomorrow's date.
        tomorrow = now + timedelta(days=1)
        elev = data.get("elev", 10)
        tmr = calc_times(
            tomorrow, data["west"]["lat"], data["west"]["lng"], data["tz"], elev
        )
        if tmr["fajr"] is None:
            return None, None
        return "fajr", tmr["fajr"] + 1440

    def render_zone_page(self, zone_code: str, base_url: str = ""):
        """Render the full SSR page for a zone, matching the original PWA."""
        found = get_zone_by_code(zone_code)
        if found is None:
            return self.render_zone_selector("Zon tidak ditemui")

        state, zone_name, data = found
        now = datetime.now(MYT)
        elev = data.get("elev", 10)
        west_min = calc_times(
            now, data["west"]["lat"], data["west"]["lng"], data["tz"], elev
        )
        east_min = calc_times(
            now, data["east"]["lat"], data["east"]["lng"], data["tz"], elev
        )
        west_times = {k: fmt_min(v) for k, v in west_min.items()}
        east_times = {k: fmt_min(v) for k, v in east_min.items()}

        active_key = self.active_prayer(west_min, now)
        next_key, next_min = self.next_prayer(west_min, now, data)
        next_name = PRAYER_NAMES.get(next_key, "—") if next_key else "—"
        next_time = fmt_min(next_min) if next_min is not None else "—"

        # Countdown to the next prayer. Absolute minutes from local midnight, so
        # tomorrow's Fajr (>= 1440) is handled like the original.
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
        if next_min is None:
            countdown = "--:--:--"
            next_at_ms = 0
        else:
            target = midnight + timedelta(minutes=next_min)
            diff_seconds = int((target - now).total_seconds())
            if diff_seconds < 0:
                diff_seconds += 86400
            countdown = (
                f"{diff_seconds // 3600:02d}:"
                f"{(diff_seconds % 3600) // 60:02d}:"
                f"{diff_seconds % 60:02d}"
            )
            next_at_ms = int(target.timestamp() * 1000)

        # Zone selector options
        state_options = ""
        for s in ZONES:
            selected = " selected" if s == state else ""
            state_options += (
                f'        <option value="{escape(s)}"{selected}>{escape(s)}</option>\n'
            )

        zone_options = ""
        for zn, zn_data in ZONES[state].items():
            selected = " selected" if zn == zone_name else ""
            zone_options += (
                f'        <option value="{escape(zn_data["zone"])}"{selected}>'
                f"{escape(zn)}</option>\n"
            )

        # Zone reference note, exactly as the original builds it
        zone_info = (
            f"Zon <b>{escape(data['zone'])}</b> &nbsp;·&nbsp; "
            f"Barat: <b>{escape(data['west']['label'])}</b> "
            f"({data['west']['lat']:.2f}°N, {data['west']['lng']:.2f}°E) &nbsp;·&nbsp; "
            f"Timur: <b>{escape(data['east']['label'])}</b> "
            f"({data['east']['lat']:.2f}°N, {data['east']['lng']:.2f}°E)"
        )

        # Prayer rows
        rows = []
        for p in PRAYERS:
            key = p["key"]
            is_active = key == active_key
            row_class = (
                "prayer-row"
                + (" dim-row" if p["dim"] else "")
                + (" active" if is_active else "")
            )
            d = diff_str(_to_minutes(west_times[key]), _to_minutes(east_times[key]))
            row = (
                f'      <div class="{row_class}">\n'
                f'        <div class="prayer-icon">{PRAYER_ICONS.get(key, "")}</div>\n'
                f'        <div class="prayer-info">\n'
                f'          <span class="prayer-name-ms">{p["name"]}</span>\n'
                f'          <span class="prayer-name-ar">{p["ar"]}</span>\n'
                f"        </div>\n"
                f'        <div class="t-cell">\n'
                f'          <span class="t-val w">{west_times[key]}</span>\n'
            )
            if d:
                row += f'          <span class="t-diff">{d}</span>\n'
            row += (
                f"        </div>\n"
                f'        <div class="t-cell"><span class="t-val e">{east_times[key]}</span></div>\n'
            )
            if is_active:
                row += '        <span class="active-badge">Sekarang</span>\n'
            row += "      </div>"
            rows.append(row)
        prayer_rows = "\n".join(rows)

        # SEO
        location = zone_name.split(" - ", 1)[1] if " - " in zone_name else zone_name
        title = f"Waktu Solat {location} - {now.strftime('%Y-%m-%d')}"
        description = (
            f"Waktu solat hari ini di {location}, {state}. "
            f"Subuh {west_times['fajr']}, Zohor {west_times['dhuhr']}, "
            f"Asar {west_times['asr']}, Maghrib {west_times['maghrib']}, "
            f"Isyak {west_times['isyak']}."
        )
        canonical = f"{base_url}/zone/{zone_code}/"

        json_ld = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": title,
            "description": description,
            "datePublished": now.strftime("%Y-%m-%d"),
            "mainEntity": {
                "@type": "ItemList",
                "name": f"Waktu Solat {location}",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": i + 1,
                        "name": p["name"],
                        "description": f"{west_times[p['key']]} ({data['west']['label']})",
                    }
                    for i, p in enumerate(PRAYERS)
                ],
            },
        }

        html = render_template(
            title=escape(title),
            description=escape(description, quote=True),
            canonical=canonical,
            json_ld=json.dumps(json_ld, ensure_ascii=False),
            state_options=state_options,
            zone_options=zone_options,
            zone_info=zone_info,
            hijri=to_hijri(now),
            day_name=DAY_NAMES[now.weekday()],
            miladi=f"{now.day} {MONTH_NAMES[now.month - 1]} {now.year}",
            next_name=next_name,
            next_time=next_time,
            countdown=countdown,
            prayer_rows=prayer_rows,
            zones_data=json.dumps(
                {s: list(ZONES[s].keys()) for s in ZONES}, ensure_ascii=False
            ),
            next_at_ms=next_at_ms,
            current_state=json.dumps(state),
            current_zone=json.dumps(zone_name),
        )

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
            options += (
                f'        <option value="{escape(z["zone"])}">'
                f"{escape(z['state'])} - {escape(z['zone_name'])}</option>\n"
            )

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
    <p class="msg">{escape(message)}</p>
    <select onchange="if(this.value) window.location.href='/zone/'+this.value">
      <option value="">Pilih Zon...</option>
{options}    </select>
  </div>
</body>
</html>"""
        return Response(html, headers={"Content-Type": "text/html; charset=utf-8"})

    def serve_sw_js(self):
        """Serve the service worker for offline caching.

        Same cache-first strategy and offline navigation fallback as the
        original PWA, but the app shell caches the SSR homepage rather than
        index.html, which this worker does not serve.
        """
        sw_js = """const CACHE_NAME = 'waktu-solat-v6';
const APP_SHELL = [
  './',
  '/manifest.webmanifest',
  '/icons/icon.svg',
  '/icons/icon-maskable.svg'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(async cache => {
      await Promise.allSettled(APP_SHELL.map(asset => cache.add(asset)));
      await self.skipWaiting();
    })
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;

  event.respondWith(
    caches.match(event.request).then(cached => {
      if (cached) return cached;

      return fetch(event.request).then(response => {
        if (!response || response.status !== 200 || response.type === 'opaque') {
          return response;
        }
        const copy = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(event.request, copy));
        return response;
      }).catch(() => {
        if (event.request.mode === 'navigate') {
          return caches.match('./');
        }
        return cached;
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
        """Serve the PWA manifest - identical to the original manifest.webmanifest."""
        manifest = {
            "name": "Waktu Solat Malaysia",
            "short_name": "Waktu Solat",
            "id": "./",
            "description": (
                "Kalkulator waktu solat Malaysia yang boleh dipasang pada telefon "
                "dan digunakan tanpa internet selepas lawatan pertama."
            ),
            "start_url": "./",
            "scope": "./",
            "display": "standalone",
            "background_color": "#0d1117",
            "theme_color": "#111820",
            "lang": "ms",
            "orientation": "portrait-primary",
            "icons": [
                {
                    "src": "icons/icon.svg",
                    "sizes": "any",
                    "type": "image/svg+xml",
                    "purpose": "any",
                },
                {
                    "src": "icons/icon-maskable.svg",
                    "sizes": "any",
                    "type": "image/svg+xml",
                    "purpose": "maskable",
                },
            ],
        }
        return Response(
            json.dumps(manifest, ensure_ascii=False),
            headers={"Content-Type": "application/manifest+json"},
        )


def _to_minutes(time_str: str):
    """Convert HH:MM string to minutes, or None if invalid."""
    if time_str == "--:--":
        return None
    parts = time_str.split(":")
    return int(parts[0]) * 60 + int(parts[1])
