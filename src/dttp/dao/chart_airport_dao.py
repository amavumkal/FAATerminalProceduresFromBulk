from ..models import ChartAirport


class CHART_AIRPORT_DAO:

    def add(self, session, chart_airport):
        session.add(chart_airport)

