from ..models import Chart

class CHARTS_DAO:

    def add_chart(self, chart, session):
        rs = session.add(chart)
        return rs

    def chartExistsByChartNameAndAiportIdAndCycle(self, session):
        return session.query

    def get_all_charts_by_cycle(self, cycle, session):
        return session.query(Chart).filter_by(cycle=cycle).all()

