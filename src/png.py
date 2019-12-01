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

    def __change_pdf_name_to_png(self, pdfName):
        ## //ToDo
        print('hello')
    def convert_pdfs_to_png(self, chart_directory):
        # print(os.getcwd())
        # print(os.listdir(chart_directory))
        CURRENT_DIRECTORY = os.getcwd()
        os.chdir(chart_directory);
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
            # pdf = Image(filename=file, resolution=50)
            # pdfImage = pdf.convert('png')
            # print(os.getcwd())
            # pdfImage.save(filename=file)
            # print(file)
            # for img in pdfImage.sequence:
            #     page=Image(image=img)
            #     page.save(filename=str(i) + '.png')
            #     i += 1
        os.chdir(CURRENT_DIRECTORY)

    def __delete_pdfs(self, chart_directory):
        current_working_directory = os.getcwd()
        os.chdir(chart_directory)
        filelist = [f for f in os.listdir(".") if f.endswith(".PDF")]
        for f in filelist:
            os.remove(f)
        os.chdir(current_working_directory)


# if __name__ == "__main__":






