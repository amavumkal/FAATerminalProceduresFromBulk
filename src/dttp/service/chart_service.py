import sys
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..dao import CHARTS_DAO
from ..dao import AIRPORTS_DAO

class ChartService:

    def __init__(self):
        secret_json = json.load(open('./secret.json', 'r'))
        db_uri = secret_json['dbURI']
        engine = create_engine(db_uri)
        self.__session = sessionmaker(bind=engine)
        self.__charts_dao = CHARTS_DAO()
        self.__airports_dao = AIRPORTS_DAO()

    def add_charts(self, charts):
        s = self.__session()
        try:
            for chart in charts:
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





