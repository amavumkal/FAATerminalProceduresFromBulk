import os
import sys
import shutil
import pickle
from wand.image import Image
from charts import *

class Convert_To_PNG:

    def __init__(self, download_dir, png_dest_dir):
        self.__png_dest_dir = png_dest_dir
        self.__DOWNLOAD_DIRECTORY = download_dir
        self.charts = None

    # pre: takes no arguments.
    # post: all pdfs in __DOWNLOAD_DIRECTORY gets converted to pngs.
    def unpickle_charts (self, binary_file_path):
        charts = Charts(charts_in = pickle.load(open(binary_file_path,"rb")))
        self.charts = charts

    def convert_pdfs_to_png(self):
        for file in os.listdir(self.__DOWNLOAD_DIRECTORY):
            with Image(file=file) as img:
                img.format = 'jpeg'

    def __delete_pdfs(self):
        current_working_directory = os.getcwd()
        os.chdir(self.__DOWNLOAD_DIRECTORY)
        filelist = [f for f in os.listdir(".") if f.endswith(".PDF")]
        for f in filelist:
            os.remove(f)
        os.chdir(current_working_directory)

    def organize_png_files(self, png_dest_directory=None):
        if png_dest_directory:
            self.__png_dest_dir = png_dest_directory
        else:
            os.mkdir('charts')
            self.__png_dest_dir = 'charts'
        root_directory = os.getcwd()
        os.chdir(self.__png_dest_dir)

        if self.__charts:
            for chart in self.__charts:
                VOLUME_NAME = chart.get_volume_name()
                if not os.path.exists(VOLUME_NAME):
                    os.mkdir(VOLUME_NAME)
                try:
                    shutil.move(chart.get_pdf_name[:-3] + 'png', VOLUME_NAME)
                except:
                    print('could not convert ' + chart.get_pdf_name[:-3] + 'png')
        else:
            raise Exception('Charts list is empty')
        os.chdir(root_directory)


if __name__ == "__main__":
    downloads_dir = sys.argv[1]
    png_dest_dir = sys.argv[2]
    convert = Convert_To_PNG(downloads_dir,png_dest_dir)
    convert.unpickle_charts(sys.argv[1]+'/pickled_charts.bin')
    for chart in convert.charts:
        print(chart.get_pdf_name)







