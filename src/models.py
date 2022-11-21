from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Float
from src.database import Base


class Weather(Base):
    __tablename__ = "weather"

    stationId = Column(Integer, primary_key=True)
    date = Column(Date, primary_key=True)
    maxTemp = Column(Integer, nullable=True)
    minTemp = Column(Integer, nullable=True)
    precipitation = Column(Integer, nullable=True)


class Yields(Base):
    __tablename__ = "yields"

    year = Column(Integer, primary_key=True, index=True)
    yields = Column(Integer)


class WeatherStatistics(Base):
    __tablename__ = 'weatherStatistics'
    # station id could also be a string, just saying.
    stationId = Column(Integer, primary_key=True)
    year = Column(Integer, primary_key=True)
    maxTempAvg = Column(Float, nullable=True)
    minTempAvg = Column(Float, nullable=True)
    precipitationSum = Column(Integer, nullable=True)
