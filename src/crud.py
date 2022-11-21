from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session
from datetime import date
from src import models


def get_weather(db: Session, stationId: int, date: date):
    if (stationId == None) and (date == None):
        return paginate(db.query(models.Weather))

    if stationId == None:
        return paginate(db.query(models.Weather).filter(models.Weather.date == date))

    if date == None:
        return paginate(db.query(models.Weather).filter(models.Weather.stationId == stationId))
    return paginate(db.query(models.Weather).filter(models.Weather.stationId == stationId, models.Weather.date == date))


def get_weather_statistics(db: Session, stationId: int, year: int):
    if (stationId == None) and (year == None):
        return paginate(db.query(models.WeatherStatistics))

    if stationId == None:
        return paginate(db.query(models.WeatherStatistics).filter(models.WeatherStatistics.year == year))

    if year == None:
        return paginate(db.query(models.WeatherStatistics).filter(models.WeatherStatistics.stationId == stationId))
    return paginate(db.query(models.WeatherStatistics).filter(models.WeatherStatistics.stationId == stationId).filter(models.WeatherStatistics.year == year))


def get_yields(db: Session, year: int):
    if year == None:
        return paginate(db.query(models.Yields))
    return paginate(db.query(models.Yields).filter(models.Yields.year == year))
