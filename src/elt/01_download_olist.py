import os
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi

LANDING_DIR = "./landing/olist"
DATASET = "olistbr/brazilian-ecommerce"
ZIP_NAME = f"{DATASET.split('/')[-1]}.zip"  # brazilian-ecommerce.zip

def main():
    os.makedirs(LANDING_DIR, exist_ok=True)
    api = KaggleApi(); api.authenticate()

    zip_path = os.path.join(LANDING_DIR, ZIP_NAME)
    if not os.path.exists(zip_path):
        api.dataset_download_files(DATASET, path=LANDING_DIR, quiet=False)
    else:
        print(f"{ZIP_NAME} já existe — ignorando download")

    matches = [f for f in os.listdir(LANDING_DIR) if f.endswith(".zip")]
    if not matches:
        raise FileNotFoundError(f"Nenhum ZIP em {LANDING_DIR}")
    zip_file = os.path.join(LANDING_DIR, matches[0])
    with zipfile.ZipFile(zip_file, 'r') as zf:
        zf.extractall(LANDING_DIR)
    print("Download & unzip concluído em", LANDING_DIR)

if __name__ == "__main__":
    main()
