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

    def __init__(self, download_directory = None):
        self.__ZIP_FILE_LETTERS = ['E', 'D', 'C', 'B', 'A']
        self.__charts = None
        self.__DOWNLOAD_DIRECTORY = download_directory + '/Charts'
        root_directory = os.getcwd()

        if not os.path.exists(download_directory):
            if not download_directory:
                raise Exception('No Directory Passed in')
            else:
                raise Exception('path ' + download_directory + 'does not exist')
        os.chdir(download_directory)
        if not os.path.exists("Charts"):
            os.mkdir("Charts")
        os.chdir("Charts")
        os.chdir(root_directory)

    def set_charts(self,charts_in):
        self.__charts = charts_in 
        
    def pickle_up_charts (self):
        current_working_directory = os.getcwd()
        if self.__charts == None:
            raise Exception('charts obj is empty no obj to pickle')
        os.chdir(self.__DOWNLOAD_DIRECTORY)
        print('pickling charts')
        binary_file = open('pickled_charts.bin', mode='wb')
        pickle.dump(self.__charts, binary_file)
        binary_file.close()
        
        os.chdir(current_working_directory) 

    #pre: method takes no arguments.
    #post: downloads charts from faa digital products site and saves to
    def download(self):
        current_working_directory = os.getcwd()
        os.chdir(self.__DOWNLOAD_DIRECTORY)
        for letter in self.__ZIP_FILE_LETTERS:
            url = 'http://www.aeronav.faa.gov/upload_313-d/terminal/DDTPP%s_%s.zip' % (letter, self.get_current_cycl())
            print('Downloading zip file: ' + url)
            request = requests.get(url)
            file = zipfile.ZipFile(BytesIO(request.content))
            file.extractall(path=self.__DOWNLOAD_DIRECTORY)
            if letter == 'E':
                if os.path.isfile('./README_Directions dTPP browser setup.pdf'):
                    os.remove('./README_Directions dTPP browser setup.pdf')
                if os.path.exists('d-TPP DVD Folder Structure'):
                    try:
                        shutil.rmtree('d-TPP DVD Folder Structure')
                    except:
                        print ("couldn't delete d-TPP DVD Folder")
                if os.path.exists('compare_pdf'):
                    try:
                        shutil.rmtree('compare_pdf')
                    except:
                        print("couldn't delete compare_pdf")
                if os.path.isfile('d-TPP_Metafile.xml'):
                    self.__charts = self.parse_metafile_xml('d-TPP_Metafile.xml')
            for chart in self.__charts.get_charts():
                if os.path.isfile(chart.get_chart_name()):
                    chart.has_downloaded = True
        self.pickle_up_charts()
        os.chdir(current_working_directory)

    def get_charts(self):
        if self.__charts:
            return self.__charts
        else:
            raise Exception('Charts list is empty')


    @staticmethod
    def parse_metafile_xml(fileIn):
        charts = Charts(charts_in=None)
        charts_object = None
        tree = ET.parse(fileIn)
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
                        chart.set_procedure_name(record.find('chart_code').text)
                        chart.set_chart_name((record.find('chart_name').text).replace('/','_'))
                        chart.set_pdf_name(record.find('pdf_name').text)
                        if chart.get_pdf_name()[-8:] == '_CMP.PDF':
                            continue
                        charts.append_chart(chart)

        print('Done Parsing: ' + fileIn)
        return charts

    @staticmethod
    def get_current_cycl():
        PRESENT = datetime.datetime.now()  # present time
        TIME_DELTA = datetime.timedelta(days=28)  # used to increase date by 28 days. FAA chart cycle
        cycle_base = datetime.datetime(2016, 8, 18)  # reference point for faa cycles

        while ((cycle_base + TIME_DELTA) <= PRESENT):  # loop while cycle date is less than current date.
            cycle_base = cycle_base + TIME_DELTA

        cycle_base = cycle_base + TIME_DELTA  # adds TIME_DELTA one more time since faa cycle attribute is based on end of cycle
        cycle_month = str(cycle_base.month)

        if (len(cycle_month) == 1):  # if single digit month adds 0 to resulting string
            cycle_month = "0" + cycle_month

        return (str(cycle_base.year) + cycle_month)


if __name__ == "__main__":
    DttpBulk = DttpBulk(download_directory='/Users/arunmavumkal/Desktop/Charts_2')
    DttpBulk.set_charts(DttpBulk.parse_metafile_xml('/Users/arunmavumkal/Desktop/Charts_2/Charts/d-TPP_Metafile.xml'))
    DttpBulk.pickle_up_charts()




