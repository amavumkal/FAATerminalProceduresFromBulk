from ..models import Chart
from sqlalchemy import delete


class CHARTS_DAO:

    def add_chart(self, chart, session):
        rs = session.add(chart)
        return rs

    def chartExistsByChartNameAndAiportIdAndCycle(self, session):
        return session.query

    def get_all_charts_by_cycle(self, session, cycle):
        return session.query(Chart).filter_by(cycle=cycle).all()

    def get_latest_cycle(self, session):
        cycle = None
        charts = session.query(Chart).distinct('cycle').all()
        for chart in charts:
            if not cycle:
                cycle = chart.cycle
            elif chart.cycle > cycle:
                cycle = chart.cycle
        return cycle

    def delete_cycle(self, session, cycle):
        session.query(Chart).filter(Chart.cycle == cycle).delete()
