# Download daily maximum temperature and precipitation (ERA5 reanalysis)
# for a few cities in the Po Valley, from the free Open-Meteo archive API.
# Data: ERA5 (Copernicus), via Open-Meteo (CC BY 4.0)

import time
from pathlib import Path

import pandas as pd
import requests

CITIES = {
    "Milano":   (45.46, 9.19),
    "Piacenza": (45.05, 9.70),
    "Mantova":  (45.16, 10.79),
    "Bologna":  (44.49, 11.34),
    "Padova":   (45.41, 11.88),
    "Rovigo":   (45.07, 11.79),
}

START = "1950-01-01"
END = "2025-12-31"
URL = "https://archive-api.open-meteo.com/v1/archive"

out_dir = Path("data")
out_dir.mkdir(exist_ok=True)

for city, (lat, lon) in CITIES.items():
    out_file = out_dir / f"{city}.csv"
    if out_file.exists():                 # already downloaded -> skip
        print(f"{city}: already downloaded")
        continue

    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": START,
        "end_date": END,
        "daily": "temperature_2m_max,precipitation_sum",
        "timezone": "Europe/Rome",
        "models": "era5",
    }

    # the free API has a limit per minute: if we hit it (error 429), wait and try again
    for attempt in range(5):
        r = requests.get(URL, params=params, timeout=120)
        if r.status_code != 429:
            break
        print(f"{city}: too many requests, waiting 70 s...")
        time.sleep(70)
    r.raise_for_status()
    daily = r.json()["daily"]

    df = pd.DataFrame({
        "date": pd.to_datetime(daily["time"]),
        "tmax": daily["temperature_2m_max"],      # °C
        "precip": daily["precipitation_sum"],      # mm/day
    })
    df.to_csv(out_file, index=False)
    print(f"{city}: {len(df)} days, {df['tmax'].isna().sum()} missing Tmax")
    time.sleep(30)   # long series count as many requests: be patient with the free API