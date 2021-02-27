from src.dttp.models import Chart

class CHARTS_DAO:

    def add_chart(self, chart, session):
        rs = session.add(chart)
        return rs

    def chartExistsByChartNameAndAiportIdAndCycle(self, session):
        return session.query


