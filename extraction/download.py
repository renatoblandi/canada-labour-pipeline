import requests
from pathlib import Path

def download_table():
    api_url = "https://www150.statcan.gc.ca/t1/wds/rest/getFullTableDownloadCSV/14100287/en"
    r = requests.get(api_url, timeout=30)
    
    # triggers a HTTPError if not successful (!= 200-299)
    r.raise_for_status()

    data = r.json()
    if data["status"] != "SUCCESS":
        raise RuntimeError(f"StatCan API returned status: {data["status"]}")

    download_url = data["object"]
    download_r = requests.get(download_url, timeout=90)

    download_r.raise_for_status()

    # define download path
    file_path = Path("data/raw/14100287-eng.zip")
    file_path.parent.mkdir(parents=True, exist_ok=True)
    # download content
    file_path.write_bytes(download_r.content)
    print(f"Successfully downloaded zip to '{file_path}'")

    return file_path


if __name__ == "__main__":
    download_table()