from dttp_bulk import *
import json

def main():
    SECRET_JSON = json.load(open('secret.json', 'r'))
    DOWNLOAD_DIR = SECRET_JSON['dload_dir']
    dttp = DttpBulk(DOWNLOAD_DIR)

    CHARTS = dttp.get_charts()
    CHARTS.save_to_mongodb()
    dttp.convert_to_png()

if __name__ == "__main__":
    main()