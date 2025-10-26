import os
from kaggle.api.kaggle_api_extended import KaggleApi

data_path = os.path.join(os.path.dirname(__file__), "data/raw")
os.makedirs(data_path, exist_ok=True)

api = KaggleApi()
api.authenticate()

api.dataset_download_files(
    "patateriedata/all-international-football-results", path=data_path, unzip=True
)
