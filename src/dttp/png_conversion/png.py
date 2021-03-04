import os
from wand.image import Image


class Convert_To_PNG:

    def __init__(self):
        self.charts = None

    @staticmethod
    def change_pdf_file_name_to_png(pdf_name):
        return pdf_name[:-4] + '.PNG'

    def convert_pdfs_to_png(self, chart_directory):
        CURRENT_DIRECTORY = os.getcwd()
        os.chdir(chart_directory);
        print('Converting Charts')
        for file in os.listdir('../../'):
            PNG_NAME = Convert_To_PNG.change_pdf_file_name_to_png(file)
            pdf_blob = self.convert_pdf_to_png(file)
            imageFile = open(PNG_NAME, "wb")
            imageFile.write(pdf_blob)
            imageFile.close()
            print('writing: ' + PNG_NAME)
            os.remove(file)
            print('removed: ' + file)
        os.chdir(CURRENT_DIRECTORY)

    def convert_pdf_to_png(self, chart_file):
        if chart_file.name[-4:].upper() == '.PDF':
            with Image(file=chart_file, resolution=75) as img:
                img.composite(img, 0, 0)
                img.format = 'png'
                return img.make_blob()

    def __delete_pdfs(self, chart_directory):
        current_working_directory = os.getcwd()
        os.chdir(chart_directory)
        filelist = [f for f in os.listdir("../..") if f.endswith(".PDF")]
        for f in filelist:
            os.remove(f)
        os.chdir(current_working_directory)


# if __name__ == "__main__":
#     ctp = Convert_To_PNG()
#     pdf_blob = ctp.convert_pdf_to_png("/home/arun/code/FAATerminalProceduresFromBulk/00865IL22L.PDF")
#     imageFile = open("/home/arun/code/FAATerminalProceduresFromBulk/00865IL22L.png", "wb")
#     imageFile.write(pdf_blob)
#     imageFile.close()







