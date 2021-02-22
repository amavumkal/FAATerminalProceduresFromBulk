import os
import sys
import shutil
import pickle
from wand.image import Image
from wand.color import Color
from charts import *

class Convert_To_PNG:

    def __init__(self):
        self.charts = None

    def convert_pdfs_to_png(self, chart_directory):
        CURRENT_DIRECTORY = os.getcwd()
        os.chdir(chart_directory);
        print('Converting Charts')
        for file in os.listdir('./'):
            if file[-4:].upper() == '.PDF':
                with Image(filename=file, resolution=75) as img:
                    with Image(width=img.width, height=img.height, background=Color("white")) as bg:
                        bg.composite(img, 0, 0)
                        PNG_NAME = file[:-4] + '.PNG'
                        bg.save(filename=PNG_NAME)
                        print('writing: ' + PNG_NAME)
                        os.remove(file)
                        print('removed: ' + file)
        os.chdir(CURRENT_DIRECTORY)

    def convert_pdf_to_png(self, chart):
        if file[-4:].upper() == '.PDF':
            with Image(filename=file, resolution=75) as img:
                with Image(width=img.width, height=img.height, background=Color("white")) as bg:
                    bg.composite(img, 0, 0)
                    PNG_NAME = file[:-4] + '.PNG'
                    return bg

    def __delete_pdfs(self, chart_directory):
        current_working_directory = os.getcwd()
        os.chdir(chart_directory)
        filelist = [f for f in os.listdir(".") if f.endswith(".PDF")]
        for f in filelist:
            os.remove(f)
        os.chdir(current_working_directory)


# if __name__ == "__main__":






