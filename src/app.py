from dttp.dttp_bulk import *
from dttp.service.chart_service import ChartService
from dttp.utils import get_current_cycl
from dttp.aws.lmb_fns import dttp_thumbnail_fn
import logging

logger = logging.getLogger()

def main():
    chart_service = ChartService()
    previous_cycle = chart_service.get_latest_cycle()
    if previous_cycle is not None and int(get_current_cycl()) <= previous_cycle:
        return
    logger.critical('Downloading meta file')
    t = threading.Thread(target=DttpBulk.parse_metafile_xml_to_db)

    logger.critical('Adding charts to DB')
    t.start()
    DttpBulk('dttp_zipfiles').download_bulk_files(t)
    if t.is_alive():
        t.join()
    if previous_cycle:
        chart_service.delete_cycle(previous_cycle)


def dttp_thumbnail_trigger(event, context):
    dttp_thumbnail_fn(event, context)


if __name__ == '__main__':
    main()
