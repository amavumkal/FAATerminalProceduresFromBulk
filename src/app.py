from dttp.dttp_bulk import *
from dttp.service.chart_service import ChartService
from dttp.utils import get_current_cycl
from dttp.aws.lmb_fns import dttp_thumbnail_fn
import logging

logger = logging.getLogger()


def main():
    previous_cycle = ChartService().get_latest_cycle()
    if previous_cycle is not None and int(get_current_cycl()) <= previous_cycle:
        return
    logger.critical('Downloading meta file')
    meta_file_local = DttpBulk.download_metafile()
    charts_local = DttpBulk.parse_metafile_xml(meta_file_local)
    charts_service_local = ChartService()
    logger.critical('Adding charts to DB')
    charts_service_local.add_charts(charts_local)
    DttpBulk('dttp_zipfiles').download_bulk_files()
    if previous_cycle:
        charts_service_local.delete_cycle(previous_cycle)
    print(get_four_digit_cycle())
    print(get_current_cycl())


def dttp_thumbnail_trigger(event, context):
    dttp_thumbnail_fn(event, context)


if __name__ == '__main__':
    main()
