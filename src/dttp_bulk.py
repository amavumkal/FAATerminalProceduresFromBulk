import requests
import datetime
import zipfile
import shutil
from io import BytesIO
import xml.etree.ElementTree as ET
import os
import pickle
from charts import *

class DttpBulk:
    def __init__(self, download_directory):  
        self.__charts = None
        self.__DOWNLOAD_DIRECTORY = download_directory
        if not os.path.exists(self.__DOWNLOAD_DIRECTORY):
            os.mkdir(self.__DOWNLOAD_DIRECTORY)

    def set_charts(self,charts_in):
        self.__charts = charts_in 

    #pre: method takes no arguments.
    #post: downloads charts from faa digital proand above, the specified commit will be merged to the current active branch. Most of the time, you will want to merge a branch with ducts site and saves to
    def download(self):
        print('download fn top' + self.__DOWNLOAD_DIRECTORY)
        META_FILE_DIR = './meta'
        DttpBulk.download_metafile(META_FILE_DIR)
        current_working_directory = os.getcwd()
        os.chdir(self.__DOWNLOAD_DIRECTORY)
        ZIP_FILE_LETTERS = ['D', 'C', 'B', 'A']
        for letter in ZIP_FILE_LETTERS:
            url = 'https://aeronav.faa.gov/upload_313-d/terminal/DDTPP%s_%s.zip' % (letter, self.get_current_cycl())
            print('Downloading zip file: ' + url)
            request = requests.get(url)
            file = zipfile.ZipFile(BytesIO(request.content))
            file.extractall(path='./')
        os.chdir(current_working_directory)
        self.__charts = DttpBulk.parse_metafile_xml('./meta/d-TPP_Metafile.xml')
        self.organize_charts()

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
        
        for file_name in os.listdir('./'):
            if file_name in chart_dict:
                chart = chart_dict[file_name]
            else:
                continue
            VOLUME = chart.get_volume_name()
            if not os.path.exists(VOLUME):
                os.mkdir(VOLUME)
            shutil.move(file_name, VOLUME)
        os.chdir(PWD)
    @staticmethod
    def download_metafile(dest_directory):
        URL = 'http://aeronav.faa.gov/d-tpp/%s/xml_data/d-tpp_Metafile.xml' % (DttpBulk.get_four_digit_cycle())
        request = requests.get(URL)
        open(dest_directory + '/d-TPP_Metafile.xml', 'wb').write(request.content)
  

    @staticmethod
    def parse_metafile_xml(fileIn):
        tree = ET.parse(fileIn)
        charts = Charts(cycle=DttpBulk.get_four_digit_cycle())
        states = tree.findall('state_code')
        print('Parsing: ' + fileIn)
        for state in states:
            state_name = state.attrib['ID']
            for city in state.findall('city_name'):
                volume_name = city.attrib['volume']
                for airport in city.findall('airport_name'):
                    airport_id_icao = airport.attrib['icao_ident']
                    airport_id = airport.attrib['apt_ident']
                    for record in airport.findall('record'):
                        chart = Chart()
                        chart.set_state_name(state_name)
                        chart.set_volume_name(volume_name)
                        chart.set_airport_id_icao(airport_id_icao)
                        chart.set_airport_id(airport_id)
                        chart.set_pdf_name(record.find('pdf_name').text)
                        chart.set_procedure_name(record.find('chart_name').text)
                        chart.set_chart_type(record.find('chart_code').text)
                        charts.append_chart(chart)
        print('Done Parsing: ' + fileIn)
        return charts

    @staticmethod
    def get_current_cycl():
        PRESENT = datetime.datetime.now()  # present time
        TIME_DELTA = datetime.timedelta(days=28)  # used to increase date by 28 days. FAA chart cycle
        CYCLE_BASE = datetime.datetime(2016, 8, 18)  # reference point for faa cycles
        date_increment = CYCLE_BASE
        while ((date_increment + TIME_DELTA) <= PRESENT):  # loop while cycle date is less than current date.
            date_increment = date_increment + TIME_DELTA

        date_increment = date_increment + TIME_DELTA  # adds TIME_DELTA one more time since faa cycle attribute is based on end of cycle
        cycle_month = str(date_increment.month)
        cycle_day = str(date_increment.day)
        cycle_year = str(date_increment.year)[-2:]
        if (len(cycle_month) == 1):  # if single digit month adds 0 to resulting string
            cycle_month = "0" + cycle_month
        if (len(cycle_day) == 1):  # if single digit month adds 0 to resulting string
            cycle_day = "0" + cycle_day

        return (cycle_year + cycle_month + cycle_day)

    @staticmethod 
    def get_four_digit_cycle(): 
        PRESENT = datetime.datetime.now()  # present time
        TIME_DELTA = datetime.timedelta(days=28)  # used to increase date by 28 days. FAA chart cycle
        CYCLE_BASE = datetime.datetime(2016, 8, 18)  # reference point for faa cycles
        date_increment = CYCLE_BASE
        while ((date_increment + TIME_DELTA) <= PRESENT):  # loop while cycle date is less than current date.
            date_increment = date_increment + TIME_DELTA
        date_increment = date_increment + TIME_DELTA  # adds TIME_DELTA one more time since faa cycle attribute is based on end of cycle
        cycle_month = str(date_increment.month)
        cycle_year = str(date_increment.year)[-2:]
        if (len(cycle_month) == 1):  # if single digit month adds 0 to resulting string
            cycle_month = "0" + cycle_month
       

        return (cycle_year + cycle_month)

if __name__ == "__main__":
    print('dttp_bulk')
