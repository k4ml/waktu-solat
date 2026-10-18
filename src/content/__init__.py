"""Editable site content: articles (artikel), guides (panduan) and
announcements (pengumuman).

Content is plain Python so it is bundled into the Worker automatically — no
database, no CMS and no build step. Edit a file, commit, and the GitHub
integration deploys it.

Adding an article
-----------------
1. Copy ``artikel_cara_menentukan_zon.py`` to ``artikel_<slug>.py``.
2. Fill in ``SLUG``, ``TITLE``, ``DESCRIPTION``, ``DATE`` and ``BODY``
   (``BODY`` is Markdown).
3. Import it below and add its ``ARTICLE`` dict to ``ARTIKEL``.

Adding a guide page
-------------------
Append a dict to ``PANDUAN`` in ``content/panduan.py``.

Adding an announcement
----------------------
Append a dict to ``PENGUMUMAN``. ``text`` is plain text (escaped for you).
``from``/``until`` are inclusive ISO dates; use ``None`` for "no end date".
"""

from datetime import date, datetime

from content import artikel_cara_menentukan_zon, artikel_mengapa_waktu_berbeza
from content.panduan import PANDUAN

# ---------------------------------------------------------------------------
# Articles — shown at /artikel/ and served at /artikel/<slug>/
# ---------------------------------------------------------------------------
ARTIKEL = [
    artikel_cara_menentukan_zon.ARTICLE,
    artikel_mengapa_waktu_berbeza.ARTICLE,
]

# ---------------------------------------------------------------------------
# Announcements — short notices shown as a banner on the prayer-time pages.
# Leave this list empty to show no banner at all.
# ---------------------------------------------------------------------------
PENGUMUMAN = [
    # {
    #     "id": "ramadan-1448",
    #     "text": "Jadual waktu solat Ramadan telah dikemas kini.",
    #     "url": "/panduan/ihtiyati/",   # optional link
    #     "from": "2027-02-01",          # optional, inclusive; None = no start
    #     "until": "2027-03-31",         # optional, inclusive; None = no end
    # },
]


def _parse_day(value):
    """Accept an ISO date/datetime string or a date, return a date or None."""
    if not value:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return datetime.strptime(str(value)[:10], "%Y-%m-%d").date()


def all_articles():
    """All published articles, newest first."""
    return sorted(ARTIKEL, key=lambda a: a["DATE"], reverse=True)


def get_article(slug: str):
    """Return the article with this slug, or None."""
    for article in ARTIKEL:
        if article["SLUG"] == slug:
            return article
    return None


def all_panduan():
    """Guide pages in display order."""
    return sorted(PANDUAN, key=lambda p: p.get("ORDER", 99))


def get_panduan(slug: str):
    """Return the guide page with this slug, or None."""
    for page in PANDUAN:
        if page["SLUG"] == slug:
            return page
    return None


def active_announcements(now=None):
    """Announcements whose date window includes today, in list order."""
    today = (now or datetime.now()).date()
    active = []
    for item in PENGUMUMAN:
        start = _parse_day(item.get("from"))
        end = _parse_day(item.get("until"))
        if start is not None and today < start:
            continue
        if end is not None and today > end:
            continue
        active.append(item)
    return active
