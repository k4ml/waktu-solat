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
│  │  - Caches app shell + visited pages on install       │   │
│  │  - Network-first for pages/API, cache-first assets   │   │
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
| `/artikel/` | Article index |
| `/artikel/<slug>/` | Article page, e.g. `/artikel/cara-menentukan-zon-waktu-solat/` |
| `/panduan/` | Guide index (Peringatan & Kaedah Pengiraan) |
| `/panduan/<slug>/` | Guide page, e.g. `/panduan/ihtiyati/` |
| `/sitemap.xml` | Sitemap (root, zone pages, articles and guides) |
| `/robots.txt` | Robots file pointing at the sitemap |
| `/sw.js` | Service worker |
| `/manifest.webmanifest` | PWA manifest |
| `/icons/*` | App icons (static assets) |
| `/dev-tools` | Development reference page (static assets) |

## SEO Features

- **Server-rendered prayer times** in HTML (crawlable by search engines)
- **Dynamic title**: zone pages use e.g. "Waktu Solat Kuala Lumpur, Putrajaya - 2026-09-06"; the root is "Waktu Solat Malaysia"
- **Canonical + og:url**: the root (`/`) canonicalises to itself; `/?zone=`, `/zon/<CODE>/`, and `/zon/<slug>/` canonicalise to `/zon/<slug>/`
- Canonical origin is set by the `SITE_ORIGIN` var rather than the request host. Redirects still use the request host. See [Preview deployments](#preview-deployments) for Preview behaviour.
- **Meta description**: the root page describes the app; zone pages list that zone's prayer times
- **Open Graph tags** for social sharing
- **Twitter Card** meta tags
- **JSON-LD structured data** for rich snippets
- **Per-zone URLs** for indexing (59 zones = 59 indexable pages)
- **Articles** at `/artikel/<slug>/` with `BlogPosting` structured data
- **Guide pages** at `/panduan/<slug>/` (penafian, zon, ihtiyati, kaedah pengiraan, isu teknikal, tarikh Hijri, dev tools)
- **`sitemap.xml`** listing every indexable URL, referenced from `robots.txt`

## Offline Support

- Service worker caches the app shell on first visit
- Network-first for pages and the JSON API (so SSR times never go stale), falling back to the cache when offline; static assets are cache-first
- Full PWA installability: icons and maskable icon served from `public/`
- Offline badge shown when network unavailable

## Managing Content

Content lives in the repository as plain Python modules, so it is bundled into
the Worker automatically. There is no CMS, database or build step: edit a file,
commit, and the GitHub integration deploys it. Everything can also be edited
straight from GitHub's web editor (open the file, click the pencil, commit).

All content is under `src/content/`:

| What | Where | Published at |
|------|-------|--------------|
| Articles | `src/content/artikel_*.py` | `/artikel/<slug>/` |
| Article index | generated from `ARTIKEL` | `/artikel/` |
| Guide pages | `src/content/panduan.py` | `/panduan/<slug>/` |
| Guide index | generated from `PANDUAN` | `/panduan/` |
| Announcements | `PENGUMUMAN` in `src/content/__init__.py` | banner on every prayer-time page |

Every content page carries the top menu (`Artikel | Panduan`) and the site
header, both linking back to the prayer-time app.

### Adding an article

1. Copy an existing file, e.g. `artikel_cara_menentukan_zon.py`, to
   `artikel_<slug>.py`.
2. Set `SLUG`, `TITLE`, `DESCRIPTION`, `DATE` (ISO, e.g. `2026-10-18`) and
   `BODY`. `BODY` is Markdown: headings, lists, tables, links, code and inline
   HTML all render.
3. Import the module in `src/content/__init__.py` and add its `ARTICLE` dict to
   the `ARTIKEL` list.

The article then appears on `/artikel/` (newest first) and gets its own
SEO-ready page at `/artikel/<slug>/`, including canonical, Open Graph, Twitter
card and `BlogPosting` JSON-LD. `sitemap.xml` picks it up automatically.

### Adding or editing a guide page

Guide pages are the reference content under `/panduan/` — this is where the
app's former "Peringatan & Kaedah Pengiraan" modal now lives. Append a dict to
`PANDUAN` in `src/content/panduan.py` with `SLUG`, `TITLE`, `DESCRIPTION`, a
Markdown `BODY` and an `ORDER` for its position in the index.

Each entry becomes a real page at `/panduan/<slug>/`, listed on `/panduan/` and
included in `sitemap.xml`.

### Adding an announcement

Append a dict to `PENGUMUMAN` in `src/content/__init__.py`:

```python
PENGUMUMAN = [
    {
        "id": "ramadan-1448",
        "text": "Jadual waktu solat Ramadan telah dikemas kini.",
        "url": "/panduan/ihtiyati/",   # optional link
        "from": "2027-02-01",          # optional, inclusive; None = no start
        "until": "2027-03-31",         # optional, inclusive; None = no end
    },
]
```

`text` is plain text (escaped for you). The banner shows on every zone page
while today falls inside the `from`/`until` window. **When the list is empty, or
no item is active, no "Pengumuman" banner is rendered at all.** It ships empty,
so a fresh deploy shows nothing until you add an item.

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

Production deploys on push to `main`, through the Cloudflare GitHub integration,
so no local deploy step is needed. `uv run pywrangler deploy` remains available
for a manual deploy:

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
│   ├── pages.py          # Article/guide/index/sitemap HTML
│   ├── md.py             # Markdown renderer (mistune)
│   ├── content/          # Editable content: articles + guides + announcements
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
