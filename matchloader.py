import os
import json
import pandas as pd
import pycountry
from kaggle.api.kaggle_api_extended import KaggleApi

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_PATH = f"{BASE_DIR }/data/raw"
PROCESSED_PATH = f"{BASE_DIR }/data/processed"

os.makedirs(RAW_PATH, exist_ok=True)
os.makedirs(PROCESSED_PATH, exist_ok=True)

api = KaggleApi()
api.authenticate()
api.dataset_download_files(
    "patateriedata/all-international-football-results", path=RAW_PATH, unzip=True
)

(lambda d: (d.to_csv(f"{PROCESSED_PATH }/countries.csv", index=False), d)[1])(
    pd.read_csv(f"{RAW_PATH }/countries_names.csv")[["original_name", "current_name"]]
    .apply(lambda c: c.str.strip())
    .assign(
        iso_alpha=lambda df: df.current_name.map(
            lambda n: json.load(
                open(f"{BASE_DIR }/config/iso3_supp.json", encoding="utf-8")
            ).get(n)
            or (pycountry.countries.lookup(n).alpha_3 if n else None)
        )
    )
)

(lambda d: (d.to_csv(f"{PROCESSED_PATH }/matches.csv", index=False), d)[1])(
    pd.read_csv(f"{RAW_PATH }/all_matches.csv")
    .replace(
        dict(
            zip(
                pd.read_csv(f"{RAW_PATH }/countries_names.csv").original_name,
                pd.read_csv(f"{RAW_PATH }/countries_names.csv").current_name,
            )
        )
    )
    .assign(date=lambda df: pd.to_datetime(df.date, errors="coerce"))
)
