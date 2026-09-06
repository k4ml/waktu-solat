"""Prayer time calculation engine - ported from JavaScript to Python.

Uses JAKIM calculation method (Rinto Anugraha "Mekanika Benda Langit" formulas).
MKI Ke-116 (November 2019): Fajr/Isha angle = 18°.
"""
import math
from datetime import datetime, timezone, timedelta

R = math.pi / 180
sinD = lambda d: math.sin(d * R)
cosD = lambda d: math.cos(d * R)
tanD = lambda d: math.tan(d * R)
acosD = lambda x: math.acos(max(-1, min(1, x))) / R
atanD = lambda x: math.atan(x) / R

# Malaysia timezone (UTC+8)
MYT = timezone(timedelta(hours=8))


def julian_date(y: int, m: int, d: int) -> float:
    """Calculate Julian Day number for given date."""
    if m <= 2:
        y -= 1
        m += 12
    A = math.floor(y / 100)
    B = 2 - A + math.floor(A / 4)
    return math.floor(365.25 * (y + 4716)) + math.floor(30.6001 * (m + 1)) + d + B - 1524.5


def sun_decl_and_eot(jd: float) -> tuple:
    """Calculate solar declination and equation of time.
    
    Returns (DELTA, ET) where:
    - DELTA: solar declination in degrees
    - ET: equation of time in minutes
    """
    # T in radians - Anugraha's series uses T*rad-to-deg conversion inside sinD
    T = 2 * math.pi * (jd - 2451545) / 365.25
    
    # sinD argument: 57.297*T converts T (radians) to degrees for sinD function
    DELTA = (0.37877
        + 23.264 * sinD(57.297 * T - 79.547)
        + 0.3812 * sinD(2 * 57.297 * T - 82.682)
        + 0.17132 * sinD(3 * 57.297 * T - 59.722))
    
    U = (jd - 2451545) / 36525
    L0 = 280.46607 + 36000.7698 * U
    
    ET = (-(1789 + 237 * U) * sinD(L0) - (7146 - 62 * U) * cosD(L0)
          + (9934 - 14 * U) * sinD(2 * L0) - (29 + 5 * U) * cosD(2 * L0)
          + (74 + 10 * U) * sinD(3 * L0) + (320 - 4 * U) * cosD(3 * L0)
          - 212 * sinD(4 * L0)) / 1000
    
    return DELTA, ET


def hour_angle(lat: float, delta: float, alt: float) -> float | None:
    """Calculate hour angle for given sun altitude.
    
    Returns hour angle in degrees, or None if sun never reaches altitude.
    """
    c = (sinD(alt) - sinD(lat) * sinD(delta)) / (cosD(lat) * cosD(delta))
    if c < -1 or c > 1:
        return None
    return acosD(c)


def calc_times(date: datetime, lat: float, lng: float, tz: int, elev: float = 10) -> dict:
    """Calculate prayer times for given date, location, and timezone.
    
    Returns dict with prayer names as keys and integer minutes from midnight as values.
    """
    jd = julian_date(date.year, date.month, date.day)
    DELTA, ET = sun_decl_and_eot(jd)
    
    # Solar transit
    TT = 12 + tz - (lng / 15) - (ET / 60)
    
    # Sun altitudes
    SA_HOR = -0.8333 - 0.0347 * math.sqrt(elev)
    SA_ASR = atanD(1 / (1 + tanD(abs(lat - DELTA))))
    
    # Hour angles
    HA_F = hour_angle(lat, DELTA, -18)  # MKI Ke-116: 18° for Fajr
    HA_S = hour_angle(lat, DELTA, SA_HOR)
    HA_A = hour_angle(lat, DELTA, SA_ASR)
    HA_I = hour_angle(lat, DELTA, -18)  # 18° for Isha
    
    # Raw times in decimal hours
    raw_fajr = HA_F - HA_F / 15 if HA_F is not None else None
    raw_syuruk = TT - HA_S / 15 if HA_S is not None else None
    raw_asr = TT + HA_A / 15 if HA_A is not None else None
    raw_maghrib = TT + HA_S / 15 if HA_S is not None else None
    raw_isyak = TT + HA_I / 15 if HA_I is not None else None
    
    # Apply ihtiyati and floor to minute (JAKIM's method)
    def apply_iht(raw, iht):
        if raw is None:
            return None
        return math.floor((raw + iht / 60) * 60)
    
    fajr_min = apply_iht(raw_fajr, 2)
    imsak_min = fajr_min - 10 if fajr_min is not None else None
    syuruk_min = apply_iht(raw_syuruk, 0)
    dhuhr_min = math.floor((TT + 2 / 60) * 60)
    asr_min = apply_iht(raw_asr, 3)
    maghrib_min = apply_iht(raw_maghrib, 1)
    isyak_min = apply_iht(raw_isyak, 2)
    
    return {
        'imsak': imsak_min,
        'fajr': fajr_min,
        'syuruk': syuruk_min,
        'dhuhr': dhuhr_min,
        'asr': asr_min,
        'maghrib': maghrib_min,
        'isyak': isyak_min,
    }


def fmt_min(m: int | None) -> str:
    """Format integer minutes to HH:MM string."""
    if m is None:
        return '--:--'
    m = ((m % 1440) + 1440) % 1440
    return f"{m // 60:02d}:{m % 60:02d}"


def diff_str(w_min: int | None, e_min: int | None) -> str:
    """Calculate diff string between west and east minute values."""
    if w_min is None or e_min is None:
        return ''
    d = e_min - w_min
    if d == 0:
        return ''
    # east = more longitude = earlier time = smaller minute = negative diff
    return f"−{abs(d)}m" if d < 0 else f"+{d}m"


def to_hijri(date: datetime) -> str:
    """Convert Gregorian date to Hijri date using tabular Islamic calendar."""
    jd = math.floor(julian_date(date.year, date.month, date.day)) + 0.5
    l = jd - 1948440 + 10632
    n = math.floor((l - 1) / 10631)
    l2 = l - 10631 * n + 354
    j = (math.floor((10985 - l2) / 5316) * math.floor((50 * l2) / 17719) +
         math.floor(l2 / 5670) * math.floor((43 * l2) / 15238))
    l3 = (l2 - math.floor((30 - j) / 15) * math.floor((17719 * j) / 50) -
          math.floor(j / 16) * math.floor((15238 * j) / 43) + 29)
    mo = math.floor((24 * l3) / 709)
    dy = round(l3 - math.floor((709 * mo) / 24))  # Round to handle floating point
    yr = 30 * n + j - 30
    
    MH = ['Muharram', 'Safar', 'Rabiul Awal', 'Rabiul Akhir',
          'Jamadil Awal', 'Jamadil Akhir', 'Rejab', 'Syaaban',
          'Ramadan', 'Syawal', 'Zulkaedah', 'Zulhijjah']
    return f"{dy} {MH[mo - 1]} {yr}H"


# Prayer metadata
PRAYERS = [
    {'key': 'imsak', 'name': 'Imsak', 'ar': 'إمساك', 'dim': True},
    {'key': 'fajr', 'name': 'Subuh', 'ar': 'الفجر', 'dim': False},
    {'key': 'syuruk', 'name': 'Syuruk', 'ar': 'الشروق', 'dim': True},
    {'key': 'dhuhr', 'name': 'Zohor', 'ar': 'الظهر', 'dim': False},
    {'key': 'asr', 'name': 'Asar', 'ar': 'العصر', 'dim': False},
    {'key': 'maghrib', 'name': 'Maghrib', 'ar': 'المغرب', 'dim': False},
    {'key': 'isyak', 'name': 'Isyak', 'ar': 'العشاء', 'dim': False},
]
