import os
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_PATH, exist_ok=True)

api = KaggleApi()
api.authenticate()
api.dataset_download_files(
    "martj42/international-football-results-from-1872-to-2017",
    path=DATA_PATH,
    unzip=True,
)
