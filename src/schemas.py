from datetime import date
from pydantic import BaseModel
from typing import Optional


class Weather(BaseModel):
    stationId: Optional[int]
    date: Optional[date]
    maxTemp: Optional[int]
    minTemp: Optional[int]
    precipitation: Optional[int]

    class Config:
        orm_mode = True


class Yields(BaseModel):
    year: int
    yields: int

    class Config:
        orm_mode = True


class WeatherStatistics(BaseModel):
    stationId: Optional[int]
    year: Optional[int]
    maxTempAvg: Optional[float]
    minTempAvg: Optional[float]
    precipitationSum: Optional[int]

    class Config:
        orm_mode = True
