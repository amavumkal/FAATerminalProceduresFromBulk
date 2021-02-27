from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Airport(Base):
    __tablename__ = 'airports'

    id = Column(Integer, primary_key=True, autoincrement=True)
    airport_ident = Column(String(3), nullable=False)
    icao_ident = Column(String(4), nullable=True)
    airport_name = Column(String(50), nullable=True)
    state = Column(String(2), nullable=False)
    city = Column(String(50), nullable=False)
    charts = relationship('Chart', back_populates='airport')


class Chart(Base):
    __tablename__ = 'charts'

    id = Column(Integer, primary_key= True, autoincrement=True, nullable=False)
    pdf_name = Column(String(50), nullable=False)
    png_name = Column(String(50), nullable=False)
    volume = Column(String(4), nullable=False)
    procedure_name = Column(String(50), nullable=False)
    chart_type = Column(String(10), nullable=False)
    airport_id = Column(Integer, ForeignKey('airports.id'))
    airport = relationship('Airport', back_populates='charts')
