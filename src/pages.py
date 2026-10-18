"""HTML for the content pages: article/guide indexes, their pages and sitemap.

The prayer-time app keeps its own template in ``template.py``; these pages reuse
the same palette and header treatment but are plain reading pages, so they carry
their own (smaller) stylesheet.
"""

import json
from datetime import datetime
from html import escape

from content import (
    active_announcements,
    all_articles,
    all_panduan,
    get_article,
    get_panduan,
)
from md import render as render_markdown

# Shared by every page kind. Conventions match template.py: @@NAME@@ markers so
# the surrounding CSS/HTML needs no escaping.
_SHELL_HEAD = """<!DOCTYPE html>
<html lang="ms">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>@@TITLE@@</title>
<meta name="theme-color" content="#111820">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Waktu Solat">
<meta name="mobile-web-app-capable" content="yes">
<meta name="description" content="@@DESCRIPTION@@">
<link rel="canonical" href="@@CANONICAL@@">

<!-- Open Graph -->
<meta property="og:type" content="@@OG_TYPE@@">
<meta property="og:url" content="@@CANONICAL@@">
<meta property="og:title" content="@@TITLE@@">
<meta property="og:description" content="@@DESCRIPTION@@">
<meta property="og:locale" content="ms_MY">

<!-- Twitter -->
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="@@TITLE@@">
<meta name="twitter:description" content="@@DESCRIPTION@@">

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
    --r:12px; --sans:'Segoe UI',system-ui,sans-serif;
  }
  *,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
  body{background:var(--ink);color:var(--text);font-family:var(--sans);min-height:100vh;overflow-x:hidden;line-height:1.75;}
  body::before{content:'';position:fixed;inset:0;z-index:0;background:radial-gradient(ellipse 80% 50% at 50% -10%,rgba(42,122,114,.18) 0%,transparent 60%),radial-gradient(ellipse 60% 40% at 100% 100%,rgba(201,168,76,.08) 0%,transparent 55%);pointer-events:none;}
  #app{position:relative;z-index:1;max-width:680px;margin:0 auto;padding:0 18px 60px;}

  header{text-align:center;padding:28px 0 14px;}
  .arabic-title{font-family:'Noto Naskh Arabic','Amiri',serif;font-size:clamp(22px,6vw,32px);color:var(--gold);line-height:1.3;display:block;margin-bottom:4px;text-decoration:none;}
  .latin-title{font-size:10px;letter-spacing:.3em;color:var(--text-dim);text-transform:uppercase;font-weight:600;}
  .hline{width:80px;height:1px;background:linear-gradient(to right,transparent,var(--gold),transparent);margin:12px auto 0;}

  nav.mainmenu{display:flex;gap:8px;justify-content:center;align-items:center;margin:16px 0 22px;font-size:11px;letter-spacing:.16em;text-transform:uppercase;font-weight:600;}
  nav.mainmenu a{color:var(--gold);text-decoration:none;opacity:.7;border:1px solid transparent;border-radius:999px;padding:7px 15px;transition:opacity .2s,border-color .2s,background .2s;}
  nav.mainmenu a:hover{opacity:1;}
  nav.mainmenu a.active{opacity:1;border-color:var(--border);background:var(--gold-dim);}

  .article{background:var(--panel);border:1px solid var(--border);border-radius:var(--r);padding:22px 22px 26px;}
  .article h1{font-size:clamp(20px,5vw,28px);color:var(--gold-light);line-height:1.35;margin-bottom:8px;font-weight:600;}
  .article-meta{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--text-muted);margin-bottom:18px;font-weight:600;}
  .article h2{font-size:17px;color:var(--gold);margin:24px 0 8px;font-weight:600;}
  .article h3{font-size:15px;color:var(--gold-light);margin:20px 0 6px;font-weight:600;}
  .article h2:first-child,.article h3:first-child{margin-top:0;}
  .article p{margin-bottom:12px;color:var(--text-dim);font-size:15px;}
  .article strong{color:var(--text);font-weight:600;}
  .article a{color:var(--teal-light);text-decoration:none;}
  .article a:hover{text-decoration:underline;}
  .article ul,.article ol{padding-left:22px;margin:0 0 12px;}
  .article li{font-size:15px;color:var(--text-dim);margin-bottom:5px;}
  .article blockquote{border-left:2px solid var(--gold);padding:2px 0 2px 14px;margin:0 0 12px;color:var(--text-muted);font-style:italic;}
  .article code{font-family:monospace;font-size:12.5px;background:rgba(201,168,76,.1);color:var(--gold-light);padding:1px 5px;border-radius:3px;}
  .article pre{background:var(--deep);border:1px solid var(--border);border-radius:8px;padding:12px 14px;overflow-x:auto;margin-bottom:12px;}
  .article pre code{background:none;color:var(--text-dim);padding:0;}
  .article hr{border:none;border-top:1px solid var(--border);margin:22px 0;}
  .article table{width:100%;border-collapse:collapse;font-size:14px;margin:0 0 14px;}
  .article th{font-size:9.5px;letter-spacing:.15em;text-transform:uppercase;color:var(--text-muted);padding:6px 10px;text-align:left;border-bottom:1px solid var(--border);font-weight:600;}
  .article td{padding:7px 10px;color:var(--text-dim);border-bottom:1px solid rgba(255,255,255,.04);}
  .article tr:last-child td{border-bottom:none;}

  .notice{background:rgba(201,168,76,.08);border:1px solid rgba(201,168,76,.28);border-radius:10px;padding:12px 14px;margin-bottom:16px;font-size:14px;color:var(--text-dim);display:flex;gap:10px;align-items:flex-start;}
  .notice-tag{font-size:9px;letter-spacing:.16em;text-transform:uppercase;color:var(--gold);border:1px solid rgba(201,168,76,.3);border-radius:999px;padding:3px 8px;white-space:nowrap;font-weight:600;flex-shrink:0;}
  .notice a{color:var(--gold-light);text-decoration:none;}
  .notice a:hover{text-decoration:underline;}

  .list{display:flex;flex-direction:column;gap:12px;}
  .list-item{display:block;background:var(--panel);border:1px solid var(--border);border-radius:var(--r);padding:16px 18px;text-decoration:none;transition:border-color .2s,background .2s;}
  .list-item:hover{border-color:var(--gold);background:var(--gold-dim);}
  .list-item h2{font-size:17px;color:var(--gold-light);font-weight:600;margin-bottom:4px;}
  .list-item time{font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--text-muted);font-weight:600;}
  .list-item .step{font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);font-weight:600;}
  .list-item p{font-size:14px;color:var(--text-dim);margin-top:8px;}
  .page-title{font-size:16px;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);font-weight:600;margin-bottom:14px;}
  .empty{color:var(--text-muted);font-size:14px;font-style:italic;}

  footer{text-align:center;padding:24px 0 0;font-size:11px;color:var(--text-muted);font-style:italic;border-top:1px solid var(--border);margin-top:28px;line-height:1.8;}
  footer a{color:var(--gold);text-decoration:none;}
  footer a:hover{text-decoration:underline;}
</style>
</head>
<body>
<div id="app">
  <header>
    <a class="arabic-title" href="/">وقت الصلاة</a>
    <div class="latin-title">Waktu Solat Malaysia</div>
    <div class="hline"></div>
  </header>
@@MENU@@
"""

_FOOTER = """  <footer>
    <p>Kaedah <span>JAKIM</span> · Anugraha "Mekanika Benda Langit" · MKI Ke-116 (2019)</p>
    <p style="margin-top:8px;">Oleh <a href="https://kamal.koditi.my/" target="_blank" rel="noopener">kamal.koditi.my</a> · Maklum balas: <a href="https://x.com/k4ml" target="_blank" rel="noopener">@k4ml</a></p>
  </footer>
</div>
</body>
</html>
"""

_SITE_SUFFIX = " - Waktu Solat Malaysia"


def _sub(template: str, **values) -> str:
    """Substitute @@NAME@@ markers, failing loudly on a missing value."""
    html = template
    for key, value in values.items():
        html = html.replace(f"@@{key.upper()}@@", str(value))
    if "@@" in html:
        leftover = sorted({part.split("@@", 1)[0] for part in html.split("@@")[1::2]})
        raise ValueError(f"unsubstituted template markers: {leftover}")
    return html


def _main_menu(active: str = "") -> str:
    """Top-level menu shown on every content page: Artikel | Panduan."""
    links = []
    for label, href, key in (
        ("Artikel", "/artikel/", "artikel"),
        ("Panduan", "/panduan/", "panduan"),
    ):
        if key == active:
            links.append(f'<a href="{href}" class="active" aria-current="page">{label}</a>')
        else:
            links.append(f'<a href="{href}">{label}</a>')
    return '<nav class="mainmenu" aria-label="Menu utama">' + "".join(links) + "</nav>"


def notice_banner(now=None) -> str:
    """Banner markup for the active announcements ('' when there are none)."""
    items = active_announcements(now)
    if not items:
        return ""
    blocks = []
    for item in items:
        text = escape(item.get("text", ""))
        url = item.get("url")
        if url:
            text += f' <a href="{escape(url, quote=True)}">Selanjutnya →</a>'
        blocks.append(
            '<div class="notice">\n'
            '  <span class="notice-tag">Pengumuman</span>\n'
            f"  <div>{text}</div>\n"
            "</div>"
        )
    return "\n".join(blocks)


def _shell(title, description, canonical, json_ld, body, active="", og_type="article") -> str:
    return _sub(
        _SHELL_HEAD + "@@BODY@@" + _FOOTER,
        title=escape(title),
        description=escape(description, quote=True),
        canonical=canonical,
        og_type=og_type,
        json_ld=json.dumps(json_ld, ensure_ascii=False),
        menu=_main_menu(active),
        body=body,
    )


def _doc(title, meta_html: str, markdown: str) -> str:
    """A reading page: heading, optional meta line, Markdown body."""
    meta = f'  <div class="article-meta">{meta_html}</div>\n' if meta_html else ""
    return (
        '<article class="article">\n'
        f"  <h1>{escape(title)}</h1>\n"
        f"{meta}"
        f"  {render_markdown(markdown)}\n"
        "</article>"
    )


def render_article(slug: str, site_origin: str = ""):
    """Render one article page, or None if the slug is unknown."""
    article = get_article(slug)
    if article is None:
        return None

    canonical = f"{site_origin}/artikel/{article['SLUG']}/"
    published = str(article["DATE"])
    body = _doc(
        article["TITLE"],
        f'<time datetime="{escape(published)}">{_display_date(article["DATE"])}</time>',
        article["BODY"],
    )
    json_ld = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": article["TITLE"],
        "description": article["DESCRIPTION"],
        "datePublished": published,
        "inLanguage": "ms",
        "mainEntityOfPage": canonical,
        "author": {"@type": "Person", "name": "kamal.koditi.my"},
    }
    return _shell(
        title=article["TITLE"] + _SITE_SUFFIX,
        description=article["DESCRIPTION"],
        canonical=canonical,
        json_ld=json_ld,
        body=body,
        active="artikel",
    )


def render_panduan(slug: str, site_origin: str = ""):
    """Render one guide page, or None if the slug is unknown."""
    page = get_panduan(slug)
    if page is None:
        return None

    canonical = f"{site_origin}/panduan/{page['SLUG']}/"
    body = _doc(page["TITLE"], "", page["BODY"])
    json_ld = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": page["TITLE"],
        "description": page["DESCRIPTION"],
        "inLanguage": "ms",
        "mainEntityOfPage": canonical,
        "isPartOf": {"@type": "CollectionPage", "name": "Panduan", "url": f"{site_origin}/panduan/"},
        "author": {"@type": "Person", "name": "kamal.koditi.my"},
    }
    return _shell(
        title=page["TITLE"] + _SITE_SUFFIX,
        description=page["DESCRIPTION"],
        canonical=canonical,
        json_ld=json_ld,
        body=body,
        active="panduan",
    )


def render_index(site_origin: str = "", now=None) -> str:
    """Render /artikel/ — announcements plus the article list."""
    canonical = f"{site_origin}/artikel/"
    articles = all_articles()

    parts = ['<h1 class="page-title">Artikel</h1>']
    # Announcements are optional; when there are none, nothing is emitted.
    banner = notice_banner(now)
    if banner:
        parts.append(banner)

    if articles:
        items = []
        for article in articles:
            items.append(
                f'<a class="list-item" href="/artikel/{article["SLUG"]}/">\n'
                f"  <time datetime=\"{escape(str(article['DATE']))}\">"
                f"{_display_date(article['DATE'])}</time>\n"
                f"  <h2>{escape(article['TITLE'])}</h2>\n"
                f"  <p>{escape(article['DESCRIPTION'])}</p>\n"
                "</a>"
            )
        parts.append('<div class="list">\n' + "\n".join(items) + "\n</div>")
    else:
        parts.append('<p class="empty">Belum ada artikel.</p>')

    json_ld = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Artikel Waktu Solat",
        "inLanguage": "ms",
        "url": canonical,
        "hasPart": [
            {
                "@type": "BlogPosting",
                "headline": a["TITLE"],
                "url": f"{site_origin}/artikel/{a['SLUG']}/",
                "datePublished": str(a["DATE"]),
            }
            for a in articles
        ],
    }
    return _shell(
        title="Artikel Waktu Solat Malaysia",
        description=(
            "Panduan waktu solat Malaysia: cara memilih zon JAKIM, sebab waktu "
            "solat berbeza antara daerah, dan nota kaedah pengiraan."
        ),
        canonical=canonical,
        json_ld=json_ld,
        body="\n".join(parts),
        active="artikel",
        og_type="website",
    )


def render_panduan_index(site_origin: str = "", now=None) -> str:
    """Render /panduan/ — the guide index."""
    canonical = f"{site_origin}/panduan/"
    pages = all_panduan()

    parts = ['<h1 class="page-title">Panduan</h1>']
    banner = notice_banner(now)
    if banner:
        parts.append(banner)

    if pages:
        items = []
        for i, page in enumerate(pages, start=1):
            items.append(
                f'<a class="list-item" href="/panduan/{page["SLUG"]}/">\n'
                f'  <span class="step">{i:02d}</span>\n'
                f"  <h2>{escape(page['TITLE'])}</h2>\n"
                f"  <p>{escape(page['DESCRIPTION'])}</p>\n"
                "</a>"
            )
        parts.append('<div class="list">\n' + "\n".join(items) + "\n</div>")
    else:
        parts.append('<p class="empty">Belum ada panduan.</p>')

    json_ld = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Panduan Waktu Solat",
        "inLanguage": "ms",
        "url": canonical,
        "hasPart": [
            {
                "@type": "WebPage",
                "name": p["TITLE"],
                "url": f"{site_origin}/panduan/{p['SLUG']}/",
                "position": i,
            }
            for i, p in enumerate(pages, start=1)
        ],
    }
    return _shell(
        title="Panduan Waktu Solat Malaysia",
        description=(
            "Panduan lengkap waktu solat Malaysia: penafian, zon dan titik "
            "rujukan JAKIM, ihtiyati, kaedah pengiraan astronomik dan tarikh "
            "Hijri."
        ),
        canonical=canonical,
        json_ld=json_ld,
        body="\n".join(parts),
        active="panduan",
        og_type="website",
    )


def render_sitemap(urls) -> str:
    """Render a sitemap.xml from a list of (loc, lastmod) tuples."""
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for loc, lastmod in urls:
        entry = ["  <url>", f"    <loc>{escape(loc)}</loc>"]
        if lastmod:
            entry.append(f"    <lastmod>{escape(str(lastmod))}</lastmod>")
        entry.append("  </url>")
        lines.extend(entry)
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


_MONTHS_MS = [
    "Januari", "Februari", "Mac", "April", "Mei", "Jun",
    "Julai", "Ogos", "September", "Oktober", "November", "Disember",
]


def _display_date(value) -> str:
    """'18 Oktober 2026' from an ISO date string or date object."""
    if isinstance(value, str):
        value = datetime.strptime(value[:10], "%Y-%m-%d").date()
    return f"{value.day} {_MONTHS_MS[value.month - 1]} {value.year}"
