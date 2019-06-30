class Charts:
    def __init__(self, charts_in=None, cycle=''):
        self.__charts = charts_in
        self.__cycle = cycle

    def get_charts(self):
        return self.__charts

    def append_chart(self, chart_in):
        if self.__charts == None:
            self.__charts = []
        self.__charts.append(chart_in)

    def set_charts(self, charts_in):
        self.__charts = charts_in


class Chart:
    def __init__(self):
        self.__airport_id_icao = ''
        self.__airport_id = ''
        self.__state_name = ''
        self.__procedure_name = ''
        self.__pdf_name = ''
        self.__chart_name = ''
        self.__volume_name = ''
        self.has_downloaded = False

    # pre: string airport_id must be declared and defined as a valid 4 character airport icao id.
    # post: stores airport_id in private member __airport_id_icao
    def set_airport_id_icao(self, airport_id):
        self.__airport_id_icao = airport_id

    # pre: string airport_id must be declared and defined as a valid 3 character airport id.
    # post: stores airport_id in private member __airport_id
    def set_airport_id(self, airport_id):
        self.__airport_id = airport_id

    # pre: string region_name must be declared and defined.
    # post: stores region_name in private member __region_name
    def set_state_name(self, region_name):
        self.__state_name = region_name

    # pre: string procedure_name must be declared and defined.
    # post: stores procedure_name in private member __procedure_name
    def set_procedure_name(self, procedure_name):
        self.__procedure_name = procedure_name

    # pre: string pdf_url must be declared and defined with valid url string.
    # post: stores pdf_url in private member __pdf_url
    def set_pdf_name(self, pdf_url):
        self.__pdf_name = pdf_url

    # pre: string chart_name must be declared and defined.
    # post: stores chart_name in private member __chart_name
    def set_chart_name(self, chart_name):
        self.__chart_name = chart_name

    # pre: string volume must be declared and defined.
    # post: stores chart_name in private member __volume_name
    def set_volume_name(self, volume):
        self.__volume_name = volume

    # pre: method takes no arguments
    # post: returns private member of type string __airport_id_icao
    def get_airport_id_icao(self):
        return self.__airport_id_icao

    # pre: method takes no arguments
    # post: returns private member of type string __airport_id
    def get_airport_id(self):
        return self.__airport_id

    # pre: method takes no arguments
    # post: returns private member of type string __state_name
    def get_state_name(self):
        return self.__state_name

    # pre: method takes no arguments
    # post: returns string private member of type string __procedure_name
    def get_procedure_name(self):
        return self.__procedure_name

    # pre: method takes no arguments
    # post: returns private member of type string __pdf_url
    def get_pdf_name(self):
        return self.__pdf_name

    # pre: method takes no arguments
    # post: returns private member of type string __chart_name
    def get_chart_name(self):
        return self.__chart_name

    # pre: method takes no arguments
    # post: returns private member of type string __volume_name
    def get_volume_name(self):
        return self.__volume_name