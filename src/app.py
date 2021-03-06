from dttp.dttp_bulk import *
from dttp.service.chart_service import ChartService
from dttp.utils import get_current_cycl
from dttp.aws.lmb_fns import dttp_thumbnail_fn
import json


def main():
    meta_file = DttpBulk.download_metafile()
    charts = DttpBulk.parse_metafile_xml(meta_file)
    charts_service = ChartService()
    charts_service.add_charts(charts)
    DttpBulk('dttp_zipfiles').download_bulk_files()
    print(get_four_digit_cycle())
    print(get_current_cycl())

def dttp_thumbnail_trigger(event, context):
    dttp_thumbnail_fn(event, context)

if __name__ == '__main__':
    main()
