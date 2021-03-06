import shutil
import requests
import xml.etree.ElementTree as ET
import io
from png_conversion.png import *
from aws.s3 import AWSS3
from models import Chart, Airport
from utils import get_current_cycl, get_four_digit_cycle

class DttpBulk:
    def __init__(self, download_directory):
        self.__charts = None
        self.__DOWNLOAD_DIRECTORY = download_directory
        self.__ZIP_FILE_LETTERS = ['D', 'C', 'B', 'A']
        if not os.path.exists(self.__DOWNLOAD_DIRECTORY):
            os.mkdir(self.__DOWNLOAD_DIRECTORY)


    def set_charts(self, charts_in):
        self.__charts = charts_in

    def __clear_dload_dir(self):
        for sub_dir in os.listdir(self.__DOWNLOAD_DIRECTORY):
            if os.path.isdir(sub_dir):
                shutil.rmtree(sub_dir)
            elif os.path.isfile(sub_dir):
                os.remove(sub_dir)

    # pre: method takes no arguments.
    # post: downloads charts from faa digital proand above, the specified commit will be merged to the current active branch. Most of the time, you will want to merge a branch with ducts site and saves to
    def download_bulk_files(self):
        print('Downloading metafile')
        for letter in self.__ZIP_FILE_LETTERS:
            file_name = 'DDTPP%s_%s.zip' % (letter, get_current_cycl())
            url = 'https://aeronav.faa.gov/upload_313-d/terminal/' + file_name
            print('Downloading zip file: ' + url)
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                data = None
                for chunk in r.iter_content(chunk_size=819200):
                    if chunk:
                        if data:
                            data += chunk
                        else:
                            data = chunk
                zip_file = io.BytesIO(data)
                zip_file.name = file_name
                AWSS3().save_to_bucket(zip_file, folder=self.__DOWNLOAD_DIRECTORY)

    def get_charts(self):
        if self.__charts:
            return self.__charts
        else:
            raise Exception('Charts list is empty')

    def organize_charts(self):
        if not self.__charts:
            raise Exception('Charts list is empty')
        PWD = os.getcwd()
        chart_dict = {}
        os.chdir(self.__DOWNLOAD_DIRECTORY)
        for chart in self.__charts:
            PDF_NAME = chart.get_pdf_name()
            if PDF_NAME in chart_dict:
                continue
            else:
                chart_dict[PDF_NAME] = chart

        for file_name in os.listdir('../'):
            if file_name in chart_dict:
                chart = chart_dict[file_name]
            else:
                continue
            VOLUME = chart.get_volume_name()
            if not os.path.exists(VOLUME):
                os.mkdir(VOLUME)
            shutil.move(file_name, VOLUME)
        os.chdir(PWD)

    #bulk convert entire dload directory to png
    def convert_to_png(self):
        FOLDERS = os.listdir(self.__DOWNLOAD_DIRECTORY)
        png_convert = Convert_To_PNG()
        for folder in FOLDERS:
            FOLDER_PATH = os.path.join(self.__DOWNLOAD_DIRECTORY, folder)
            if os.path.isdir(FOLDER_PATH):
                png_convert.convert_pdfs_to_png(FOLDER_PATH)


    @staticmethod
    def download_metafile():
        URL = 'http://aeronav.faa.gov/d-tpp/%s/xml_data/d-tpp_Metafile.xml' % (get_four_digit_cycle())
        print(URL)
        request = requests.get(URL)
        return io.BytesIO(request.content)

    @staticmethod
    def parse_metafile_xml(fileIn):
        charts = []
        if not fileIn:
            fileIn = DttpBulk.download_metafile()
        tree = ET.parse(fileIn)
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
                        chart.airport = airport
                        charts.append(chart)
        print('Done Parsing: metafile')
        return charts




if __name__ == "__main__":
    # meta_file = DttpBulk.download_metafile()
    # charts = DttpBulk.parse_metafile_xml(meta_file)
    # charts_service = ChartService()
    # charts_service.add_charts(charts)
    DttpBulk('dttp_zipfiles').download_bulk_files()
    print(get_four_digit_cycle())
    print(get_current_cycl())

