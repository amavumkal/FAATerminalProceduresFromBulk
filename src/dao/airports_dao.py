from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
import sys
from ..models import Airport


class AIRPORTS_DAO:

    def __init__(self):
        secret_json = json.load(open('./secret.json', 'r'))
        db_uri = secret_json['dbURI']
        engine = create_engine(db_uri)
        self.__session = sessionmaker(bind=engine)

    def __del__(self):
        self.__session.close_all()

    def add_airport(self, airport):
        s = self.__session()
        rs = None
        try:
            rs = s.add(airport)
            s.commit()
        except Exception as e:
            s.rollback()
            print(e, file=sys.stderr)
        finally:
            s.close()
        return rs

    def get_airport_by_icao_ident(self, ident):
        s = self.__session()
        rs = None
        try:
            rs = s.query(Airport).filter_by(icao_ident=ident).one()
        except Exception as e:
            print(e, file=sys.stderr)
        finally:
            s.close()
            return rs

    def get_airport_by_airport_ident(self, ident):
        s = self.__session()
        rs = None
        try:
            rs = s.query(Airport).filter_by(airport_ident=ident).one()
        except Exception as e:
            print(e, file=sys.stderr)
        finally:
            s.close()
            return rs

    def airport_exists_by_icao_or_airport_ident(self, airport):
        rs = None
        if airport.icao_ident:
            rs = self.get_airport_by_icao_ident(airport.icao_ident).one()
        elif airport.airport_ident:
            rs = self.get_airport_by_airport_ident(airport.airport_ident).one()
        return rs if rs else None
