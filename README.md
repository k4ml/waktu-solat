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
│  │  - Cache-first with offline navigation fallback      │   │
│  │  - Falls back to cache when offline                 │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## URL Structure

| URL | Description |
|-----|-------------|
| `/` | Default zone (JHR02 - Johor) |
| `/zon/<slug>/` | Zone page by place slug, e.g. `/zon/johor-bahru/` (canonical) |
| `/zon/<CODE>/` | Zone page by JAKIM code, e.g. `/zon/JHR02/` |
| `/?zone=JHR02` | Query param alternative |
| `/api/zon/<CODE>/` | JSON API for zone, e.g. `/api/zon/JHR02/` |
| `/sw.js` | Service worker |
| `/manifest.webmanifest` | PWA manifest |
| `/icons/*` | App icons (static assets) |
| `/dev-tools` | Development reference page (static assets) |

## SEO Features

- **Server-rendered prayer times** in HTML (crawlable by search engines)
- **Dynamic title**: "Waktu Solat Kuala Lumpur, Putrajaya - 2026-09-06"
- **Canonical + og:url** per zone (dedupes `/`, `/?zone=`, and `/zon/<CODE>/` against `/zon/<slug>/`)
- Canonical origin is set by the `SITE_ORIGIN` var rather than the request host. Redirects still use the request host. See [Preview deployments](#preview-deployments) for Preview behaviour.
- **Meta description** with actual prayer times
- **Open Graph tags** for social sharing
- **Twitter Card** meta tags
- **JSON-LD structured data** for rich snippets
- **Per-zone URLs** for indexing (59 zones = 59 indexable pages)

## Offline Support

- Service worker caches the app shell on first visit
- Cache-first strategy for pages, with an offline navigation fallback
- Full PWA installability: icons and maskable icon served from `public/`
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

### Preview deployments

Requires Wrangler 4.135.0+ (the version `pywrangler` resolves). Preview settings
live in the `previews` block of `wrangler.jsonc`; assets and `compatibility_*`
stay at the top level.

```bash
# Preview name defaults to the current git branch
uv run pywrangler preview

# Or name it explicitly
uv run pywrangler preview --name my-branch
```

Previews need no `SITE_ORIGIN` of their own. They do not inherit top-level vars,
so with an empty `previews` block a Preview canonicalises to whichever host
served the request: the Preview URL is correct, and the per-deployment URL
(`<deployment-id>-…`) merely self-references. That is harmless because Cloudflare
adds `X-Robots-Tag: noindex` to `workers.dev` Preview URLs.

Add `previews.vars.SITE_ORIGIN` on a branch only if you also want the
per-deployment URL to canonicalise to the Preview URL, for example
`https://<preview-name>-waktu-solat.kamal-mustafa.workers.dev`, where
`<preview-name>` is the git branch (or whatever you pass to `--name`). A branch
cut from such a branch inherits the stale value, so leaving it out is the better
default. Only the top-level `SITE_ORIGIN` affects production.

## File Structure

```
.
├── src/
│   ├── entry.py          # Worker entry point (SSR handler, sw.js + manifest)
│   ├── template.py       # Page template (mirrors index.html markup/CSS/JS)
│   ├── prayer.py         # Calculation engine
│   └── zones.py          # Zone data
├── public/               # Static assets served by the worker
│   ├── icons/            # App icons + maskable icon
│   └── dev-tools.html    # Development reference page
├── wrangler.jsonc        # Worker configuration
├── pyproject.toml        # Python project config
└── index.html            # Original client-rendered PWA
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
