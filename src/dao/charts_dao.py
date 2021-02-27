from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
import sys
from .airports_dao import AIRPORTS_DAO


class CHARTS_DAO:

    def __init__(self):
        secret_json = json.load(open('./secret.json', 'r'))
        db_uri = secret_json['dbURI']
        engine = create_engine(db_uri)
        self.__session = sessionmaker(bind=engine)

    def __del__(self):
        self.__session.close_all()

    def add_charts(self, charts):
        s = self.__session()
        airports_dao = AIRPORTS_DAO()
        try:

            for chart in charts:
                airport = chart.airport
                airprt_rs = None
                if airport.icao_ident:
                    airprt_rs = airports_dao.get_airport_by_icao_ident(airport.icao_ident)
                elif airport.airport_ident:
                    airprt_rs = airports_dao.get_airport_by_airport_ident(airport.airport_ident)
                chart.airport_id = airprt_rs.id if airprt_rs else airports_dao.add_airport(airport).id
                return s.add(chart)
            s.commit()
        except Exception as e:
            s.rollback()
            print(e, file=sys.stderr)
        finally:
            s.close()
