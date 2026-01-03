import pandas as pd
import re
from pathlib import Path

LOCATIONS_PATH = "../uscities.csv"

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def load_us_location_index():
    df = pd.read_csv(LOCATIONS_PATH)

    cities = set(normalize(c) for c in df["city"].dropna())
    states = set(normalize(s) for s in df["state_name"].dropna())
    state_codes = set(normalize(s) for s in df["state_id"].dropna())

    # common aliases
    aliases = {
        "sf": "san francisco",
        "nyc": "new york",
        "la": "los angeles",
        "bay area": "san francisco",
    }

    return {
        "cities": cities,
        "states": states,
        "state_codes": state_codes,
        "aliases": aliases,
    }


US_LOCATIONS = load_us_location_index()


def is_us_location(location: str) -> bool:
    if not location:
        return False

    loc = normalize(location)

    # fast paths
    if "us remote" in loc or "remote us" in loc:
        return True

    # split multi-location strings
    parts = [p.strip() for p in loc.split(",")]

    for part in parts:
        if part in US_LOCATIONS["cities"]:
            return True
        if part in US_LOCATIONS["states"]:
            return True
        if part in US_LOCATIONS["state_codes"]:
            return True
        if part in US_LOCATIONS["aliases"]:
            return True

    return False

