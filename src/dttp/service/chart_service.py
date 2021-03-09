import sys
import json
import threading
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..dao import CHARTS_DAO
from ..dao import AIRPORTS_DAO

class ChartService:

    MAX_THREADS = 15

    def __init__(self):
        secret_json = json.load(open('./secret.json', 'r'))
        db_uri = secret_json['dbURI']
        engine = create_engine(db_uri)
        self.__session = sessionmaker(bind=engine)
        self.__charts_dao = CHARTS_DAO()
        self.__airports_dao = AIRPORTS_DAO()
        self.__chart_threads_dict = {}
        self.__chart_thread_lock = threading.Lock()

    def add_chart(self, chart):
        s = self.__session()
        try:
            airport = chart.airport
            airprt_rs = None
            if airport.icao_ident:
                airprt_rs = self.__airports_dao.get_airport_by_icao_ident(airport.icao_ident, s)
            elif airport.airport_ident:
                airprt_rs = self.__airports_dao.get_airport_by_airport_ident(airport.airport_ident, s)
            if airprt_rs:
                chart.airport_id = airprt_rs.id
                chart.airport.id = airprt_rs.id
            else:
                chart.airport = self.__airports_dao.add_airport(airport, s)
                chart.airport_id = chart.airport.id
            self.__charts_dao.add_chart(chart, s)
            s.commit()
        except Exception as e:
            s.rollback()
            print(e, file=sys.stderr)
        finally:
            s.close()

    def __manage_chart_threads(self):
        self.__chart_thread_lock.acquire()
        thread_dict = self.__chart_threads_dict
        dict_len = len(self.__chart_threads_dict)
        if dict_len >= self.MAX_THREADS:
            threads_to_remove_keys = []
            while dict_len >= self.MAX_THREADS:
                for key in thread_dict.keys():
                    if not thread_dict[key].isAlive():
                        threads_to_remove_keys.append(key)
                        dict_len -= 1
                for key in threads_to_remove_keys:
                    thread_dict.pop(key)
                if dict_len >= self.MAX_THREADS:
                    time.sleep(.1)
        self.__chart_thread_lock.release()

    def wait_on_chart_threads(self):
        for key in self.__chart_threads_dict:
            self.__chart_threads_dict[key].join()

    def add_chart_async(self, chart):
        self.__manage_chart_threads()
        t = threading.Thread(target=self.add_chart, args=(chart,))
        self.__chart_thread_lock.acquire()
        if chart.pdf_name in self.__chart_threads_dict.keys():
            i = 0
            new_pdf_name = chart.pdf_name + str(i)
            while new_pdf_name in self.__chart_threads_dict.keys():
                i += 1
                new_pdf_name = chart.pdf_name + str(i)

        else:
            self.__chart_threads_dict[chart.pdf_name] = t
        t.start()
        self.__chart_thread_lock.release()

    def get_all_charts_by_cycle(self, cycle):
        s = self.__session()
        charts = self.__charts_dao.get_all_charts_by_cycle(s, cycle)
        s.close()
        return charts

    def get_latest_cycle(self):
        s = self.__session()
        cycle = self.__charts_dao.get_latest_cycle(s)
        s.close()
        return cycle

    def delete_cycle(self, cycle):
        s = self.__session()
        try:
            self.__charts_dao.delete_cycle(s, cycle)
        except Exception as e:
            s.rollback()
            print(e, file=sys.stderr)
        finally:
            s.close()





