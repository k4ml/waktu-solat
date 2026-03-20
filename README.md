# 🕌 Waktu Solat Malaysia

A small installable Malaysian prayer time calculator. No API calls, no dependencies, and after the first online visit it can run fully offline from a phone home screen.

**[→ Live Demo](https://your-username.github.io/waktu-solat)**

---

## Features

- **All 41 JAKIM zones** across Peninsular Malaysia, Sabah, and Sarawak
- **Dual west/east columns** — western boundary (JAKIM official reference) and eastern boundary of each zone, showing the time spread within a zone
- **Live countdown** to next prayer, ticking every second
- **Hijri date** computed locally
- **Installable PWA** — add to home screen on Android or iPhone/iPad
- **Fully offline after first load** — app shell, icons, and manifest are cached locally
- **Selection persistence** — remembers the user's last chosen state/zone on the device

---

## Files

| File | Purpose |
|---|---|
| `index.html` | Main application UI and calculation logic |
| `dev-tools.html` | Developer cross-check tools |
| `manifest.webmanifest` | PWA manifest for installation |
| `sw.js` | Service worker for offline caching |
| `icons/` | Local app icons used by the manifest and browsers |

---

## Calculation Method

Based on **Rinto Anugraha's *Mekanika Benda Langit*** (Universiti Gadjah Mada), the same reference used by JAKIM and Indonesian Kemenag.

### Sun Altitude & Ihtiyati Per Prayer

| Prayer | Sun Altitude | Ihtiyati | Notes |
|---|---|---|---|
| Imsak | — | — | 10 minutes before Subuh |
| Subuh / Fajr | −18° (MKI Ke-116, November 2019) | +10 min | JAKIM/Kemenag standard |
| Syuruk | −0.833° − 0.0347√h | +0 min | h = elevation in metres |
| Zohor | Solar transit | +2 min | Sun crosses local meridian |
| Asar | Shafi'i formula¹ | +3 min | Malaysia uses Shafi'i madhab |
| Maghrib | −0.833° − 0.0347√h | +1 min | Same altitude as Syuruk |
| Isyak | −18° | +2 min | JAKIM/Kemenag standard |

> ¹ Shafi'i Asar altitude = `arctan(1 / (1 + tan|lat − δ|))` where δ = solar declination

**Ihtiyati** (الاحتياط) is a precautionary margin added to the raw astronomical value before flooring to the nearest minute. These values were confirmed by cross-referencing JAKIM e-solat published data for zones JHR02 and WLY01.

### Why Two Columns?

JAKIM uses the **westernmost point** of each zone as its single reference coordinate. This ensures the entire zone is safely past imsak at the same announced time. The eastern boundary column shows how much earlier prayers begin at the other end — ranging from a few minutes for small zones up to 10–15 minutes for large ones like PHG and SBH.

---

## Key Findings During Development

These were discovered by cross-checking the calculation against live JAKIM data:

**1. Formula bug — T must stay in radians**

Anugraha's declination series:
```
DELTA = 0.37877 + 23.264 × sin(57.297×T − 79.547) + …
```
The `57.297` factor (`180/π`) converts T from radians to degrees *inside* the `sinD()` call. Pre-converting T to degrees first before multiplying by 57.297 shifts Subuh by 12–15 minutes.

**2. Ihtiyati is not widely documented but is measurable**

Most public references state JAKIM uses Fajr at 20° and Isha at 18° — and stop there. In practice JAKIM adds a per-prayer ihtiyati on top. Subuh is consistently exactly 10 minutes later than the raw astronomical floor. This is the single largest source of discrepancy in third-party implementations.

**3. JAKIM's reference coordinate is not the city centre**

For JHR02, using Johor Bahru city coordinates (1.55°N, 103.75°E) gives a different result from JAKIM's published table. The actual reference is the zone's western boundary — approximately 1.48°N, 103.62°E (Kulai area). Each 0.25° longitude ≈ 1 minute of time difference.

**4. Asar differs by madhab**

Shafi'i Asar (used in Malaysia) occurs 30–60 minutes earlier than Hanafi Asar depending on latitude and season.

---

## Disclaimer

> **For general guidance only.** Times may differ by 1–2 minutes from officially published JAKIM times due to coordinate approximations and zone boundary assumptions. For authoritative prayer times, refer to:
> - [e-Solat JAKIM](https://www.e-solat.gov.my)
> - Your state's Majlis Agama Islam
> - The annual Taqwim Solat published by JAKIM

---

## Dev Tools

`waktu-solat-devtools.html` contains the interactive tools used during development to validate the calculation:

| Tab | What it does |
|---|---|
| 1 · JAKIM Comparison | Paste any JAKIM times and compare minute-by-minute against local calculation with colour-coded diff |
| 2 · Coordinate Probe | Scan a lat/lng range to find which coordinate produces a specific target prayer time |
| 3 · Ihtiyati Probe | Automatically find ihtiyati values that best fit a set of JAKIM times across all prayers |
| 4 · JAKIM API Fetch | Attempt live fetch from `e-solat.gov.my` API; includes `curl` and Node.js scripts for CORS bypass |
| 5 · Source Scripts | Original Node.js scripts run in terminal during development, fully commented |

---

## Running Locally

No build step. For install/offline support, serve over `http://localhost` or HTTPS so the service worker can register:

```bash
git clone https://github.com/your-username/waktu-solat.git
cd waktu-solat

npx serve .
# then open http://localhost:3000
```

Direct `file://` opening still shows the calculator, but browser install prompts and offline caching will not work there because service workers are disabled on `file://`.

## Mobile Install

1. Open the deployed app once while online.
2. Use the in-app install button if the browser offers it.
3. If no button appears:
   - **iPhone/iPad (Safari):** Share → Add to Home Screen
   - **Android (Chrome/Edge):** browser menu → Install app / Add to Home screen
4. After installation, launch from the home screen icon. The cached app should continue working without internet.

---

## References

- Rinto Anugraha, *Mekanika Benda Langit*, Universiti Gadjah Mada — [PDF](https://simpan.ugm.ac.id/s/GcxKuyZWn8Rshnn)
- [JAKIM e-Solat](https://www.e-solat.gov.my) — official Malaysian prayer times
- [Step by Step: Calculating Prayer Times](https://radhifadlillah.com/blog/2020-09-06-calculating-prayer-times/) — English summary of Anugraha's method

---

## License

MIT
