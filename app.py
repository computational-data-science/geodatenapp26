import streamlit as st
import pandas as pd
import math

# ------------------------------------
# Koordinaten der 15 Hauptstädte
# ------------------------------------
STADT_KOORDINATEN = {
    "Addis Ababa":   (9.0320,  38.7469),
    "Bahir Dar":     (11.5931, 37.3908),
    "Mekelle":       (13.4967, 39.4753),
    "Dire Dawa":     (9.5931,  41.8661),
    "Hawassa":       (7.0504,  38.4955),
    "Jimma":         (7.6780,  36.8340),
    "Adama":         (8.5400,  39.2700),
    "Gondar":        (12.6030, 37.4521),
    "Dessie":        (11.1333, 39.6333),
    "Assosa":        (10.0667, 34.5333),
    "Semera":        (11.7933, 40.9917),
    "Jijiga":        (9.3500,  42.8000),
    "Arba Minch":    (6.0333,  37.5500),
    "Debre Birhan":  (9.6833,  39.5333),
    "Nekemte":       (9.0833,  36.5500),
    "Äthopia": (10.5, 35.0),
    "Üthopia": (5.5, 40.5),
    "Öthopia": (13.0, 41.5),
}


# ------------------------------------
# Mapping: alle Varianten → Hauptstadt
# ------------------------------------
STADT_MAPPING = {
    # Addis Ababa
    "addis ababa": "Addis Ababa", "addis abeba": "Addis Ababa",
    "addiss ababa": "Addis Ababa", "addiss abeba": "Addis Ababa",
    "adis ababa": "Addis Ababa", "adis abeba": "Addis Ababa",
    "adiss ababa": "Addis Ababa", "adiss abeba": "Addis Ababa",
    "aa": "Addis Ababa", "a.a": "Addis Ababa", "a.a.": "Addis Ababa",
    "a a": "Addis Ababa", "a. a": "Addis Ababa", "a. a.": "Addis Ababa",
    "addisababa": "Addis Ababa", "addisabeba": "Addis Ababa",
    "adisababa": "Addis Ababa", "adisabeba": "Addis Ababa",
    "finfinnee": "Addis Ababa", "finfine": "Addis Ababa",
    "addis": "Addis Ababa",

    # Bahir Dar
    "bahir dar": "Bahir Dar", "bahirdar": "Bahir Dar",
    "bahir dare": "Bahir Dar", "bahia dar": "Bahir Dar",
    "bahor dar": "Bahir Dar", "bahairdar": "Bahir Dar",
    "baheredare": "Bahir Dar", "baherdar": "Bahir Dar",
    "b/dar": "Bahir Dar", "bdr": "Bahir Dar", "b/dr": "Bahir Dar",
    "b.dar": "Bahir Dar", "bhair dar": "Bahir Dar",

    # Mekelle
    "mekelle": "Mekelle", "mekele": "Mekelle", "mekell": "Mekelle",
    "mekela": "Mekelle", "mekele city": "Mekelle", "mekelle city": "Mekelle",
    "mekle": "Mekelle", "mekell": "Mekelle",

    # Dire Dawa
    "dire dawa": "Dire Dawa", "diredawa": "Dire Dawa",
    "dire dewa": "Dire Dawa", "dire dwa": "Dire Dawa",
    "dire daea": "Dire Dawa", "diredewa": "Dire Dawa",
    "d.d": "Dire Dawa",

    # Hawassa
    "hawassa": "Hawassa", "hawasa": "Hawassa", "hawasssa": "Hawassa",
    "hawass": "Hawassa", "hawwassa": "Hawassa", "hawassa city": "Hawassa",
    "awassa": "Hawassa", "hwassa": "Hawassa",

    # Jimma
    "jimma": "Jimma", "jima": "Jimma", "jmma": "Jimma",
    "jimma town": "Jimma",

    # Adama
    "adama": "Adama", "adamaa": "Adama", "adama town": "Adama",
    "adama city": "Adama", "adama/nazareth": "Adama",

    # Gondar
    "gondar": "Gondar", "gonder": "Gondar", "gondar town": "Gondar",
    "gonder town": "Gondar", "gondar city": "Gondar",

    # Dessie
    "dessie": "Dessie", "desse": "Dessie", "desie": "Dessie",
    "dessie town": "Dessie", "desi": "Dessie", "dessia": "Dessie",

    # Assosa
    "assosa": "Assosa", "asosa": "Assosa", "assossa": "Assosa",
    "asossa": "Assosa",

    # Semera
    "semera": "Semera", "semera town": "Semera", "samara": "Semera",
    "samera": "Semera", "semra": "Semera",

    # Jijiga
    "jijiga": "Jijiga", "jigjiga": "Jijiga", "jigiga": "Jijiga",
    "jijiga town": "Jijiga",

    # Arba Minch
    "arba minch": "Arba Minch", "arba mench": "Arba Minch",
    "arbaminch": "Arba Minch", "arb minch": "Arba Minch",
    "arba minch town": "Arba Minch", "arba-minch": "Arba Minch",

    # Debre Birhan
    "debre birhan": "Debre Birhan", "debre berhan": "Debre Birhan",
    "debrebirhan": "Debre Birhan", "debirebirhan": "Debre Birhan",
    "debre brhan": "Debre Birhan", "debir brehan": "Debre Birhan",

    # Nekemte
    "nekemte": "Nekemte", "nekemte town": "Nekemte",
    "nekemt": "Nekemte", "nekamte": "Nekemte",

    # ... bestehende Einträge ...
    "äthopia": "Äthopia",
    "üthopia": "Üthopia",
    "öthopia": "Öthopia",
}

def berechne_distanz(stadt1, stadt2):
    if stadt1 not in STADT_KOORDINATEN or stadt2 not in STADT_KOORDINATEN:
        return None
    lat1, lon1 = STADT_KOORDINATEN[stadt1]
    lat2, lon2 = STADT_KOORDINATEN[stadt2]
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return round(R * 2 * math.asin(math.sqrt(a)), 1)


@st.cache_data
def load_data():
    df = pd.read_csv("data/SupplierList.csv")
    df["Town_Clean"] = (
        df["Town"]
        .fillna("")
        .str.strip()
        .str.lower()
        .map(lambda x: STADT_MAPPING.get(x, None))
    )
    return df

df = load_data()

st.title("Ethiopia Supplier Finder")
st.write("Finde die nächsten Lieferanten für deine Baumaterialien.")

st.sidebar.header("🔍 Deine Suche")

eigener_standort = st.sidebar.selectbox(
    "Dein Standort",
    sorted(STADT_KOORDINATEN.keys())
)

alle_materialien = sorted(df["Business_Type"].dropna().str.strip().unique().tolist())
gewaehlte_materialien = st.sidebar.multiselect(
    "Welche Materialien brauchst du? (max. 5)",
    alle_materialien,
    max_selections=5
)


if gewaehlte_materialien:
    st.subheader(f"📍 Ergebnisse für: {eigener_standort}")

    for material in gewaehlte_materialien:
        st.markdown(f"###  {material}")

        
        gefiltert = df[
            (df["Business_Type"].str.strip() == material) &
            (df["Town_Clean"].notna())
        ].copy()

        if gefiltert.empty:
            st.warning("Keine Lieferanten mit bekanntem Standort gefunden.")
            continue

        
        gefiltert["Distanz_km"] = gefiltert["Town_Clean"].apply(
            lambda x: berechne_distanz(eigener_standort, x)
        )

       
        naechste = (
            gefiltert.dropna(subset=["Distanz_km"])
            .sort_values("Distanz_km")
            .head(5)[["Company_Name", "Town_Clean", "Distanz_km", "Preis"]]
            .rename(columns={
                "Company_Name": "Lieferant",
                "Town_Clean": "Stadt",
                "Distanz_km": "Distanz (km)",
                "Preis": "Preiskategorie"
            })
            .reset_index(drop=True)
        )

        st.dataframe(naechste)
        # ------------------------------------
        # Karte: Standorte der Top-5 Lieferanten
        # ------------------------------------
        karten_daten = naechste.copy()
        karten_daten["lat"] = karten_daten["Stadt"].map(lambda s: STADT_KOORDINATEN[s][0])
        karten_daten["lon"] = karten_daten["Stadt"].map(lambda s: STADT_KOORDINATEN[s][1])

        # Eigenen Standort auch mit anzeigen
        eigene_position = pd.DataFrame({
            "lat": [STADT_KOORDINATEN[eigener_standort][0]],
            "lon": [STADT_KOORDINATEN[eigener_standort][1]]
        })

        st.map(pd.concat([karten_daten[["lat", "lon"]], eigene_position]), size=20)
else:
    st.info("Wähle links deinen Standort und mindestens ein Material aus.")
