from src.dttp.models import Airport


class AIRPORTS_DAO:

    def add_airport(self, airport, session):
        session.add(airport)
        return airport

    def get_airport_by_icao_ident(self, ident, session):
        return session.query(Airport).filter_by(icao_ident=ident).first()

    def get_airport_by_airport_ident(self, ident, session):
        return session.query(Airport).filter_by(airport_ident=ident).first()

    def airport_exists_by_icao_or_airport_ident(self, airport, session):
        rs = None
        if airport.icao_ident:
            rs = self.get_airport_by_icao_ident(airport.icao_ident, session)
        elif airport.airport_ident:
            rs = self.get_airport_by_airport_ident(airport.airport_ident, session)
        return rs if rs else None
