import logging
from ..s3 import AWSS3
from io import BytesIO
from ...png_conversion.png import Convert_To_PNG


def dttp_thumbnail_fn(event, context):
    logger = logging.getLogger()
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
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
