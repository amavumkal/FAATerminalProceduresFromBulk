import shutil
import requests
import xml.etree.ElementTree as ET
import threading
import io
import os
from .aws.s3 import AWSS3
from .models import Chart, Airport
from .utils import get_current_cycl, get_four_digit_cycle
from .service.chart_service import ChartService
class DttpBulk:
    def __init__(self, s3_folder):
        self.__charts = None
        self.__S3_FOLDER = s3_folder
        self.__ZIP_FILE_LETTERS = ['D', 'C', 'B', 'A']
        if not os.path.exists(self.__S3_FOLDER):
            os.mkdir(self.__S3_FOLDER)

    def __clear_dload_dir(self):
        for sub_dir in os.listdir(self.__S3_FOLDER):
            if os.path.isdir(sub_dir):
                shutil.rmtree(sub_dir)
            elif os.path.isfile(sub_dir):
                os.remove(sub_dir)

    # pre: method takes no arguments.
    # post: downloads charts from faa digital proand above, the specified commit will be merged to the current active branch. Most of the time, you will want to merge a branch with ducts site and saves to
    def download_bulk_files(self, db_thread=None):
        awss3 = AWSS3()
        s3_threads = []
        for letter in self.__ZIP_FILE_LETTERS:
            file_name = 'DDTPP%s_%s.zip' % (letter, get_current_cycl())
            url = 'https://aeronav.faa.gov/upload_313-d/terminal/' + file_name
            print('Downloading zip file: ' + url)
            data = requests.get(url)
            zip_file = io.BytesIO(data.content)
            zip_file.name = file_name
            if db_thread:
                db_thread.join()
            t = threading.Thread(target=awss3.save_to_bucket, args=(zip_file,), kwargs=({'folder': self.__S3_FOLDER}))
            print('Uploading zip file: ' + url)
            s3_threads.append(t)
            t.start()
        print('waiting for s3 uploads')
        for thread in s3_threads:
            thread.join()

    def get_charts(self):
        if self.__charts:
            return self.__charts
        else:
            raise Exception('Charts list is empty')


    @staticmethod
    def download_metafile():
        print('Downloading meta file')
        URL = 'http://aeronav.faa.gov/d-tpp/%s/xml_data/d-tpp_Metafile.xml' % (get_four_digit_cycle())
        print(URL)
        request = requests.get(URL)
        return io.BytesIO(request.content)

    @staticmethod
    def parse_metafile_xml_to_db():
        file_in = DttpBulk.download_metafile()
        chart_service = ChartService()
        tree = ET.parse(file_in)
        states = tree.findall('state_code')
        cycle = get_current_cycl()
        print('Parsing metafile')
        for state in states:
            state_name = state.attrib['ID']
            for city in state.findall('city_name'):
                city_name = city.attrib['ID']
                volume_name = city.attrib['volume']
                for airport in city.findall('airport_name'):
                    airport_id_icao = airport.attrib['icao_ident']
                    airport_id = airport.attrib['apt_ident']
                    for record in airport.findall('record'):
                        chart = Chart()
                        chart.cycle = cycle
                        airport = Airport()
                        airport.state = state_name
                        airport.city = city_name
                        airport.icao_ident = airport_id_icao
                        airport.airport_ident = airport_id
                        chart.volume = volume_name
                        chart.pdf_name = record.find('pdf_name').text
                        chart.procedure_name = record.find('chart_name').text
                        chart.png_name = chart.pdf_name[:len(chart.pdf_name) - 4] + '.PNG'
                        chart.chart_type = record.find('chart_code').text
                        chart_service.add_chart_async(chart, airport)
        print('Done Parsing: metafile')
        chart_service.wait_on_chart_threads()


if __name__ == "__main__":

    meta_file = DttpBulk.download_metafile()
    charts = DttpBulk.parse_metafile_xml_to_db(meta_file)
    charts_service = ChartService()
    charts_service.add_chart(charts)
    DttpBulk('dttp_zipfiles').download_bulk_files()
    print(get_four_digit_cycle())
    print(get_current_cycl())

