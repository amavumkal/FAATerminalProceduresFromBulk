from dttp.dttp_bulk import *
from dttp.service.chart_service import ChartService
import json


def main():
    SECRET_JSON = json.load(open('secret.json', 'r'))
    DOWNLOAD_DIR = SECRET_JSON['dload_dir']
    dttp = DttpBulk(DOWNLOAD_DIR)
    CHARTS = dttp.get_charts()
    CHARTS.save_to_mongodb()
    dttp.convert_to_png()



if __name__ == '__main__':
    print(ChartService().get_all_charts_by_cycle(DttpBulk.get_current_cycl()))
