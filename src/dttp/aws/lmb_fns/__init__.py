import logging
import os
from ..s3 import AWSS3
from zipfile import ZipFile
from io import BytesIO
from ...service.chart_service import ChartService
from ...utils import get_current_cycl
from ...png_conversion.png import Convert_To_PNG
logger = logging.getLogger()

def createChartsDic():
    charts = ChartService().get_all_charts_by_cycle(get_current_cycl())
    chart_dict = {}
    for chart in charts:
        chart_dict[chart.pdf_name] = chart
    return chart_dict


def dttp_unzip_fn(event, context):
    # retrieve bucket name and file_key from the S3 event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    logger.log(msg='file_key ' + file_key, level=20)
    aws_s3 = AWSS3(bucket_name)
    chart_dict = createChartsDic()
    logger.info('Reading {} from {}'.format(file_key, bucket_name))
    # get the object
    dttp_zip_file = aws_s3.get_obj_bin(file_key)
    dttp_pdfs = ZipFile(dttp_zip_file, 'r')
    temp_name = None

    for name in dttp_pdfs.namelist():
        uncompressed_pdf = BytesIO(dttp_pdfs.read(name))
        uncompressed_pdf.name = name
        temp_name = name
        try:
            if(name and name[-3:] == 'PDF'):
                aws_s3.save_to_bucket(uncompressed_pdf, folder='pdfs/'+chart_dict[name].volume)
            else:
                logger.critical("rejected file: " + name)
        except Exception as e:
            logger.critical('for filename: ' + temp_name + ' Folder: pdfs/'+chart_dict[name].volume )
            logger.exception(e)

    logger.critical('complete')
    aws_s3.delete_obj(file_key)

def dttp_thumbnail_fn(event, context):

    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    aws_s3 = None
    split_name = file_key.split('/')
    if not file_key[-3:] == 'PDF':
        return
    aws_s3 = AWSS3(bucket_name)
    logger.info('Reading {} from {}'.format(file_key, bucket_name))
    # get the object
    pdf = aws_s3.get_obj_bin(file_key)
    logger.critical('PDF retrived with name: ' + pdf.name)
    png_file = BytesIO(Convert_To_PNG().convert_pdf_to_png(pdf))
    png_file.name = split_name[-1][:-3] + 'PNG'
    try:
        aws_s3.save_to_bucket(png_file, folder='thumbnails/' + split_name[1])
    except Exception as e:
        logger.critical('for filename: ' + png_file.name)
        logger.exception(e)
