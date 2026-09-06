# Waktu Solat Malaysia - Cloudflare Worker (SSR)

Server-side rendered version using Cloudflare Python Workers for better SEO
while maintaining offline PWA support via service worker.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Cloudflare Edge                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Python Worker (SSR)                                │   │
│  │  - Calculates prayer times server-side              │   │
│  │  - Renders HTML with times baked in                 │   │
│  │  - Adds SEO meta tags (OG, Twitter, JSON-LD)        │   │
│  │  - Serves service worker + manifest                 │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Browser                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Service Worker (Offline Cache)                     │   │
│  │  - Caches app shell on install                      │   │
│  │  - Stale-while-revalidate for pages                 │   │
│  │  - Falls back to cache when offline                 │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## URL Structure

| URL | Description |
|-----|-------------|
| `/` | Default zone (WLY01 - KL) |
| `/zone/JHR02` | Specific zone page (SSR) |
| `/?zone=JHR02` | Query param alternative |
| `/api/zone/JHR02` | JSON API for zone |
| `/sw.js` | Service worker |
| `/manifest.webmanifest` | PWA manifest |

## SEO Features

- **Server-rendered prayer times** in HTML (crawlable by search engines)
- **Dynamic title**: "Waktu Solat Kuala Lumpur, Putrajaya - 2026-09-06"
- **Meta description** with actual prayer times
- **Open Graph tags** for social sharing
- **Twitter Card** meta tags
- **JSON-LD structured data** for rich snippets
- **Per-zone URLs** for indexing (41 zones = 41 indexable pages)

## Offline Support

- Service worker caches app shell on first visit
- Stale-while-revalidate strategy for zone pages
- Full PWA installability maintained
- Offline badge shown when network unavailable

## Local Development

### Prerequisites

- [uv](https://docs.astral.sh/uv/#installation) package manager
- [Node.js](https://nodejs.org/en) (for workerd runtime)

### Setup & Run

```bash
# Run locally
uv run pywrangler dev

# Or using uvx (no install)
uvx --from workers-py pywrangler dev
```

### Deploy

```bash
uv run pywrangler deploy
```

## File Structure

```
.
├── src/
│   ├── entry.py          # Worker entry point (SSR handler)
│   ├── prayer.py         # Calculation engine
│   └── zones.py          # Zone data
├── wrangler.jsonc        # Worker configuration
├── pyproject.toml        # Python project config
├── sw.js                 # Service worker (static)
├── manifest.webmanifest  # PWA manifest (static)
└── icons/                # App icons
```

## Calculation Method

Same as original PWA:
- JAKIM calculation method (Rinto Anugraha formulas)
- MKI Ke-116 (November 2019): Fajr/Isha angle = 18°
- Ihtiyati margins: Subuh +2min, Zohor +2min, Asar +3min, Maghrib +1min, Isyak +2min
- Dual west/east columns showing time spread within each zone

## Performance

- **CPU time**: <1ms per request (well within 10ms free tier limit)
- **Memory**: <1MB (well within 128MB limit)
- **Free tier capacity**: 100,000 requests/day
- **Cache**: 5-minute CDN cache for SSR responses
