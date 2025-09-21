from kaggle.api.kaggle_api_extended import KaggleApi
from pathlib import Path

api=KaggleApi()
api.authenticate()

data_dir = Path('data')
data_dir.mkdir(exist_ok=True)

datasets=['lainguyn123/student-performance-factors','haseebindata/student-performance-predictions']

for dataset in datasets:
    api.dataset_download_files(dataset, path=data_dir, unzip=True)
    