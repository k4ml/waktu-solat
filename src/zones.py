"""JAKIM prayer time zones for Malaysia.

Each zone stores westernmost (JAKIM's official reference) and easternmost boundary.
West is used because it's the latest point for Fajr and earliest for Maghrib.
"""

ZONES = {
    "Johor": {
        "JHR01 - Pulau Aur & Pulau Pemanggil": {
            "zone": "JHR01", "tz": 8,
            "west": {"lat": 2.40, "lng": 104.45, "label": "P.Pemanggil"},
            "east": {"lat": 2.46, "lng": 104.54, "label": "P.Aur"}
        },
        "JHR02 - Johor Bahru, Kota Tinggi, Mersing, Kulai": {
            "zone": "JHR02", "tz": 8,
            "west": {"lat": 1.48, "lng": 103.62, "label": "Kulai"},
            "east": {"lat": 2.43, "lng": 104.11, "label": "Mersing"}
        },
        "JHR03 - Kluang, Pontian": {
            "zone": "JHR03", "tz": 8,
            "west": {"lat": 1.49, "lng": 103.38, "label": "Pontian"},
            "east": {"lat": 2.02, "lng": 103.33, "label": "Kluang"}
        },
        "JHR04 - Batu Pahat, Muar, Segamat, Gemas, Tangkak": {
            "zone": "JHR04", "tz": 8,
            "west": {"lat": 1.86, "lng": 102.93, "label": "Parit Raja"},
            "east": {"lat": 2.52, "lng": 103.28, "label": "Segamat"}
        },
    },
    "Kedah": {
        "KDH01 - Kota Setar, Kubang Pasu, Pokok Sena": {
            "zone": "KDH01", "tz": 8,
            "west": {"lat": 6.35, "lng": 100.08, "label": "Kuala Kedah"},
            "east": {"lat": 6.10, "lng": 100.55, "label": "Pokok Sena"}
        },
        "KDH02 - Kuala Muda, Yan, Pendang": {
            "zone": "KDH02", "tz": 8,
            "west": {"lat": 5.73, "lng": 100.28, "label": "Kuala Muda"},
            "east": {"lat": 5.97, "lng": 100.72, "label": "Pendang"}
        },
        "KDH03 - Padang Terap, Sik": {
            "zone": "KDH03", "tz": 8,
            "west": {"lat": 6.22, "lng": 100.58, "label": "Padang Terap"},
            "east": {"lat": 5.70, "lng": 100.95, "label": "Sik"}
        },
        "KDH04 - Baling": {
            "zone": "KDH04", "tz": 8,
            "west": {"lat": 5.70, "lng": 100.75, "label": "Baling Barat"},
            "east": {"lat": 5.65, "lng": 101.02, "label": "Baling Timur"}
        },
        "KDH05 - Kulim, Bandar Baharu": {
            "zone": "KDH05", "tz": 8,
            "west": {"lat": 5.37, "lng": 100.43, "label": "Bandar Baharu"},
            "east": {"lat": 5.37, "lng": 100.72, "label": "Kulim"}
        },
        "KDH06 - Langkawi": {
            "zone": "KDH06", "tz": 8,
            "west": {"lat": 6.35, "lng": 99.63, "label": "P.Tuba"},
            "east": {"lat": 6.42, "lng": 100.12, "label": "Langkawi Timur"}
        },
        "KDH07 - Puncak Gunung Jerai": {
            "zone": "KDH07", "tz": 8, "elev": 1200,
            "west": {"lat": 5.79, "lng": 100.43, "label": "G.Jerai"},
            "east": {"lat": 5.79, "lng": 100.43, "label": "G.Jerai"}
        },
    },
    "Kelantan": {
        "KTN01 - Kota Bharu, Bachok, Pasir Puteh, Tumpat, Pasir Mas, Tanah Merah, Machang, Kuala Krai, Mukim Chiku": {
            "zone": "KTN01", "tz": 8,
            "west": {"lat": 5.43, "lng": 101.73, "label": "Jeli/Chiku"},
            "east": {"lat": 6.20, "lng": 102.37, "label": "Bachok"}
        },
        "KTN02 - Gua Musang, Jeli, Lojing": {
            "zone": "KTN02", "tz": 8,
            "west": {"lat": 4.88, "lng": 101.77, "label": "Gua Musang Barat"},
            "east": {"lat": 5.43, "lng": 101.73, "label": "Jeli"}
        },
    },
    "Melaka": {
        "MLK01 - Seluruh Negeri Melaka": {
            "zone": "MLK01", "tz": 8,
            "west": {"lat": 2.25, "lng": 102.07, "label": "Jasin/Merlimau"},
            "east": {"lat": 2.12, "lng": 102.52, "label": "Pantai Timur"}
        },
    },
    "Negeri Sembilan": {
        "NGS01 - Tampin, Jempol": {
            "zone": "NGS01", "tz": 8,
            "west": {"lat": 2.47, "lng": 102.03, "label": "Tampin"},
            "east": {"lat": 3.26, "lng": 102.42, "label": "Jempol"}
        },
        "NGS02 - Jelebu, Kuala Pilah, Rembau": {
            "zone": "NGS02", "tz": 8,
            "west": {"lat": 3.08, "lng": 101.83, "label": "Jelebu"},
            "east": {"lat": 2.72, "lng": 102.27, "label": "Kuala Pilah"}
        },
        "NGS03 - Port Dickson, Seremban": {
            "zone": "NGS03", "tz": 8,
            "west": {"lat": 2.53, "lng": 101.72, "label": "Port Dickson"},
            "east": {"lat": 2.82, "lng": 101.95, "label": "Seremban"}
        },
    },
    "Pahang": {
        "PHG01 - Pulau Tioman": {
            "zone": "PHG01", "tz": 8,
            "west": {"lat": 2.80, "lng": 104.12, "label": "P.Tioman Barat"},
            "east": {"lat": 2.80, "lng": 104.22, "label": "P.Tioman Timur"}
        },
        "PHG02 - Kuantan, Pekan, Muadzam Shah, Rompin": {
            "zone": "PHG02", "tz": 8,
            "west": {"lat": 3.42, "lng": 102.75, "label": "Muadzam Shah"},
            "east": {"lat": 3.97, "lng": 103.40, "label": "Kuantan"}
        },
        "PHG03 - Jerantut, Temerloh, Maran, Bera, Chenor, Jengka": {
            "zone": "PHG03", "tz": 8,
            "west": {"lat": 3.45, "lng": 102.00, "label": "Bera Barat"},
            "east": {"lat": 3.97, "lng": 102.82, "label": "Maran"}
        },
        "PHG04 - Bentong, Lipis, Raub": {
            "zone": "PHG04", "tz": 8,
            "west": {"lat": 3.53, "lng": 101.68, "label": "Bentong"},
            "east": {"lat": 4.18, "lng": 102.05, "label": "Kuala Lipis"}
        },
        "PHG05 - Genting Sempah, Janda Baik, Bukit Tinggi": {
            "zone": "PHG05", "tz": 8, "elev": 800,
            "west": {"lat": 3.40, "lng": 101.72, "label": "Genting Sempah"},
            "east": {"lat": 3.68, "lng": 101.87, "label": "Bukit Tinggi"}
        },
        "PHG06 - Cameron Highlands, Genting Highlands, Bukit Fraser": {
            "zone": "PHG06", "tz": 8, "elev": 1500,
            "west": {"lat": 3.30, "lng": 101.37, "label": "Bukit Fraser"},
            "east": {"lat": 4.48, "lng": 101.42, "label": "Cameron Highlands"}
        },
    },
    "Perak": {
        "PRK01 - Tapah, Slim River, Tanjung Malim": {
            "zone": "PRK01", "tz": 8,
            "west": {"lat": 3.70, "lng": 101.08, "label": "Tanjung Malim"},
            "east": {"lat": 4.20, "lng": 101.47, "label": "Tapah"}
        },
        "PRK02 - Kuala Kangsar, Sg.Siput, Ipoh, Batu Gajah, Kampar": {
            "zone": "PRK02", "tz": 8,
            "west": {"lat": 4.45, "lng": 100.73, "label": "Larut Barat"},
            "east": {"lat": 4.77, "lng": 101.20, "label": "Kuala Kangsar"}
        },
        "PRK03 - Lenggong, Pengkalan Hulu, Grik": {
            "zone": "PRK03", "tz": 8,
            "west": {"lat": 5.20, "lng": 100.87, "label": "Lenggong"},
            "east": {"lat": 5.45, "lng": 101.30, "label": "Grik"}
        },
        "PRK04 - Temengor, Belum": {
            "zone": "PRK04", "tz": 8,
            "west": {"lat": 5.33, "lng": 101.22, "label": "Temengor"},
            "east": {"lat": 5.72, "lng": 101.55, "label": "Belum"}
        },
        "PRK05 - Teluk Intan, Bagan Datuk, Seri Iskandar, Kg.Gajah, Lumut": {
            "zone": "PRK05", "tz": 8,
            "west": {"lat": 3.88, "lng": 100.75, "label": "Bagan Datuk"},
            "east": {"lat": 4.05, "lng": 101.07, "label": "Seri Iskandar"}
        },
        "PRK06 - Selama, Taiping, Parit Buntar, Bagan Serai": {
            "zone": "PRK06", "tz": 8,
            "west": {"lat": 5.05, "lng": 100.50, "label": "Parit Buntar"},
            "east": {"lat": 5.65, "lng": 100.98, "label": "Selama"}
        },
        "PRK07 - Bukit Larut": {
            "zone": "PRK07", "tz": 8, "elev": 1000,
            "west": {"lat": 4.87, "lng": 100.80, "label": "Bukit Larut"},
            "east": {"lat": 4.87, "lng": 100.80, "label": "Bukit Larut"}
        },
    },
    "Perlis": {
        "PLS01 - Kangar, Padang Besar, Arau": {
            "zone": "PLS01", "tz": 8,
            "west": {"lat": 6.45, "lng": 100.08, "label": "Kuala Perlis"},
            "east": {"lat": 6.72, "lng": 100.37, "label": "Padang Besar"}
        },
    },
    "Pulau Pinang": {
        "PNG01 - Seberang Perai, Pulau Pinang": {
            "zone": "PNG01", "tz": 8,
            "west": {"lat": 5.42, "lng": 100.18, "label": "P.Pinang Barat"},
            "east": {"lat": 5.42, "lng": 100.57, "label": "Seberang Perai Timur"}
        },
    },
    "Sabah": {
        "SBH01 - Sandakan Timur, Bukit Garam, Semawang, Temanggong, Tambisan, Sukau": {
            "zone": "SBH01", "tz": 8,
            "west": {"lat": 5.43, "lng": 117.82, "label": "Bukit Garam"},
            "east": {"lat": 5.72, "lng": 118.20, "label": "Tambisan"}
        },
        "SBH02 - Sandakan Barat, Beluran, Telupid, Kuamut": {
            "zone": "SBH02", "tz": 8,
            "west": {"lat": 5.70, "lng": 117.50, "label": "Beluran"},
            "east": {"lat": 5.85, "lng": 118.13, "label": "Sandakan Barat"}
        },
        "SBH03 - Lahad Datu, Kunak, Silabukan, Tungku, Sahabat, Semporna": {
            "zone": "SBH03", "tz": 8,
            "west": {"lat": 5.08, "lng": 117.57, "label": "Lahad Datu"},
            "east": {"lat": 4.48, "lng": 118.62, "label": "Semporna"}
        },
        "SBH04 - Bandar Tawau, Balong, Merotai, Kalabakan, Tawau Barat/Timur": {
            "zone": "SBH04", "tz": 8,
            "west": {"lat": 4.60, "lng": 117.60, "label": "Kalabakan"},
            "east": {"lat": 4.25, "lng": 118.12, "label": "Bandar Tawau"}
        },
        "SBH05 - Kudat, Kota Marudu, Pitas, Pulau Banggi": {
            "zone": "SBH05", "tz": 8,
            "west": {"lat": 6.52, "lng": 116.60, "label": "Kota Marudu"},
            "east": {"lat": 7.25, "lng": 117.33, "label": "P.Banggi"}
        },
        "SBH06 - Gunung Kinabalu": {
            "zone": "SBH06", "tz": 8, "elev": 3000,
            "west": {"lat": 6.10, "lng": 116.55, "label": "G.Kinabalu"},
            "east": {"lat": 6.10, "lng": 116.55, "label": "G.Kinabalu"}
        },
        "SBH07 - Kota Kinabalu, Ranau, Tuaran, Penampang, Papar, Putatan, Kota Belud": {
            "zone": "SBH07", "tz": 8,
            "west": {"lat": 5.87, "lng": 115.73, "label": "Papar"},
            "east": {"lat": 6.35, "lng": 116.70, "label": "Kota Belud"}
        },
        "SBH08 - Keningau, Tambunan, Nabawan, Pensiangan": {
            "zone": "SBH08", "tz": 8,
            "west": {"lat": 4.73, "lng": 115.85, "label": "Nabawan"},
            "east": {"lat": 5.46, "lng": 116.22, "label": "Tambunan"}
        },
        "SBH09 - Beaufort, Sipitang, Tenom, Membakut, Kuala Penyu, Weston, Long Pa Sia": {
            "zone": "SBH09", "tz": 8,
            "west": {"lat": 5.08, "lng": 115.48, "label": "Sipitang"},
            "east": {"lat": 5.10, "lng": 115.97, "label": "Tenom"}
        },
    },
    "Sarawak": {
        "SWK01 - Limbang, Lawas, Sundar, Terusan": {
            "zone": "SWK01", "tz": 8,
            "west": {"lat": 4.73, "lng": 114.77, "label": "Sundar"},
            "east": {"lat": 5.00, "lng": 115.42, "label": "Lawas"}
        },
        "SWK02 - Miri, Niah, Bekenu, Sibuti, Marudi, Belaga": {
            "zone": "SWK02", "tz": 8,
            "west": {"lat": 3.72, "lng": 113.73, "label": "Subis/Bekenu"},
            "east": {"lat": 4.40, "lng": 114.33, "label": "Marudi"}
        },
        "SWK03 - Bintulu, Tatau, Sebauh, Song, Balingian, Kapit": {
            "zone": "SWK03", "tz": 8,
            "west": {"lat": 2.02, "lng": 112.53, "label": "Song"},
            "east": {"lat": 3.25, "lng": 113.23, "label": "Bintulu"}
        },
        "SWK04 - Sibu, Dalat, Oya, Igan, Kanowit": {
            "zone": "SWK04", "tz": 8,
            "west": {"lat": 2.33, "lng": 111.45, "label": "Igan/Oya"},
            "east": {"lat": 2.33, "lng": 112.07, "label": "Kanowit"}
        },
        "SWK05 - Sarikei, Julau, Bitangor, Rajang, Belawai, Matu, Daro": {
            "zone": "SWK05", "tz": 8,
            "west": {"lat": 2.25, "lng": 111.43, "label": "Matu/Daro"},
            "east": {"lat": 2.12, "lng": 111.98, "label": "Sarikei"}
        },
        "SWK06 - Sri Aman, Betong, Spaoh, Pusa, Saratok, Roban, Debak, Kabong, Lingga, Engkelili": {
            "zone": "SWK06", "tz": 8,
            "west": {"lat": 1.23, "lng": 111.10, "label": "Lubuk Antu"},
            "east": {"lat": 1.55, "lng": 111.82, "label": "Betong"}
        },
        "SWK07 - Samarahan, Simunjan, Serian, Sebuyau, Meludam": {
            "zone": "SWK07", "tz": 8,
            "west": {"lat": 1.52, "lng": 110.28, "label": "Tebedu"},
            "east": {"lat": 1.48, "lng": 110.60, "label": "Asajaya"}
        },
        "SWK08 - Kuching, Bau, Lundu, Sematan": {
            "zone": "SWK08", "tz": 8,
            "west": {"lat": 1.80, "lng": 109.63, "label": "Sematan"},
            "east": {"lat": 1.55, "lng": 110.50, "label": "Kuching"}
        },
        "SWK09 - Zon Khas (Kawasan Khas)": {
            "zone": "SWK09", "tz": 8,
            "west": {"lat": 1.50, "lng": 110.25, "label": "Zon Khas Barat"},
            "east": {"lat": 1.50, "lng": 110.42, "label": "Zon Khas Timur"}
        },
    },
    "Selangor": {
        "SGR01 - Gombak, Petaling, Sepang, Hulu Langat, Hulu Selangor, Shah Alam": {
            "zone": "SGR01", "tz": 8,
            "west": {"lat": 3.13, "lng": 101.38, "label": "Kapar/Klang"},
            "east": {"lat": 3.65, "lng": 101.92, "label": "Hulu Selangor"}
        },
        "SGR02 - Kuala Selangor, Sabak Bernam": {
            "zone": "SGR02", "tz": 8,
            "west": {"lat": 3.63, "lng": 100.98, "label": "Sabak Bernam"},
            "east": {"lat": 3.35, "lng": 101.42, "label": "Kuala Selangor"}
        },
        "SGR03 - Klang, Kuala Langat": {
            "zone": "SGR03", "tz": 8,
            "west": {"lat": 2.90, "lng": 101.18, "label": "Banting"},
            "east": {"lat": 3.05, "lng": 101.57, "label": "Klang"}
        },
    },
    "Terengganu": {
        "TRG01 - Kuala Terengganu, Marang, Kuala Nerus": {
            "zone": "TRG01", "tz": 8,
            "west": {"lat": 5.31, "lng": 102.83, "label": "Marang"},
            "east": {"lat": 5.35, "lng": 103.20, "label": "Kuala Terengganu"}
        },
        "TRG02 - Besut, Setiu": {
            "zone": "TRG02", "tz": 8,
            "west": {"lat": 5.42, "lng": 102.40, "label": "Setiu"},
            "east": {"lat": 5.70, "lng": 102.83, "label": "Besut"}
        },
        "TRG03 - Hulu Terengganu": {
            "zone": "TRG03", "tz": 8,
            "west": {"lat": 4.97, "lng": 102.55, "label": "Hulu Trg Barat"},
            "east": {"lat": 5.10, "lng": 103.02, "label": "Hulu Trg Timur"}
        },
        "TRG04 - Kemaman, Dungun": {
            "zone": "TRG04", "tz": 8,
            "west": {"lat": 4.27, "lng": 103.03, "label": "Dungun"},
            "east": {"lat": 4.23, "lng": 103.50, "label": "Kemaman"}
        },
    },
    "W.P. Kuala Lumpur & Putrajaya": {
        "WLY01 - Kuala Lumpur, Putrajaya": {
            "zone": "WLY01", "tz": 8,
            "west": {"lat": 3.14, "lng": 101.58, "label": "KL Barat"},
            "east": {"lat": 2.92, "lng": 101.75, "label": "Putrajaya"}
        },
    },
    "W.P. Labuan": {
        "WLY02 - Labuan": {
            "zone": "WLY02", "tz": 8,
            "west": {"lat": 5.28, "lng": 115.17, "label": "Labuan Barat"},
            "east": {"lat": 5.35, "lng": 115.28, "label": "Labuan Timur"}
        },
    },
}


def get_zone(state: str, zone_name: str) -> dict | None:
    """Get zone data by state and zone name."""
    state_zones = ZONES.get(state)
    if state_zones is None:
        return None
    return state_zones.get(zone_name)


def get_zone_by_code(code: str) -> tuple | None:
    """Find zone by code (e.g., 'JHR02'). Returns (state, zone_name, zone_data) or None."""
    for state, zones in ZONES.items():
        for zone_name, data in zones.items():
            if data["zone"] == code:
                return state, zone_name, data
    return None


def get_all_zones_flat() -> list:
    """Get flat list of all zones with state info."""
    result = []
    for state, zones in ZONES.items():
        for zone_name, data in zones.items():
            result.append({
                "state": state,
                "zone_name": zone_name,
                "zone": data["zone"],
            })
    return result
