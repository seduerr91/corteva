
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate

from fastapi import Depends, FastAPI, HTTPException
from typing import Union, List, Any, Iterator
from sqlalchemy.orm import Session
from datetime import date
import logging
import time
from src import schemas, crud, database, ingest, models
from src.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.on_event("startup")
def on_startup() -> None:

    db = SessionLocal()
    # Check if there are records in the database, else ingest on startup.
    yield_records = ingest.get_number_of_entries(db, models.Yields)
    if yield_records < 1:
        print(f'There are no yield records in DB. Starting ingesting yield data... (please find details in docs/ingestion.log).')
        yields_data = ingest.transform_yields_data_to_df()
        ingest.data_to_db(yields_data, models.Yields, db)

    else:
        print(f'There are {yield_records} yield records in DB.')

    weather_records = ingest.get_number_of_entries(db, models.Weather)
    if weather_records < 1:
        print(f'There are no weather records in DB. Starting ingesting weather data, and calculating respective weather statistics. This will take a second (please find details in docs/ingestion.log).')
        weather_data = ingest.transform_weather_data_to_df()

        ingest.data_to_db(weather_data, models.Weather, db)
        db.query(models.WeatherStatistics).delete()
        db.commit()
        weather_statistics_data = ingest.transform_weatherStatistics_data_to_df(
            weather_data)

        ingest.data_to_db(weather_statistics_data,
                          models.WeatherStatistics, db)
    else:
        print(f'There are {weather_records} weather records in DB.')
    db.flush()
    db.close()


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Using SQLAlchemy could potentially require some "waiting".
# But as SQLAlchemy doesn't have compatibility for using await directly, we don't use it.

@app.get("/")
def index_hi():
    return {'Hi Corteva team, thank you for checking my assignment.'}


@app.get("/api/weather/", response_model=Page[schemas.Weather])
def read_weather(stationId: Union[int, None] = None, date: Union[date, None] = None, db: Session = Depends(get_db)):
    db_weather = crud.get_weather(db, stationId=stationId, date=date)

    if db_weather is None:
        raise HTTPException(
            status_code=404, detail="Station or date not available")

    return db_weather


@app.get("/api/weather/stats/", response_model=Page[schemas.WeatherStatistics])
def read_weather_statistics(stationId: Union[int, None] = None, year: Union[int, None] = None, db: Session = Depends(get_db)):
    db_weather_statistics = crud.get_weather_statistics(
        db, stationId=stationId, year=year)

    if db_weather_statistics is None:
        raise HTTPException(
            status_code=404, detail="Station or year not available")

    return db_weather_statistics


@app.get("/api/yield/", response_model=Page[schemas.Yields])
def read_yields(year: Union[int, None] = None, db: Session = Depends(get_db)):
    db_yield = crud.get_yields(db, year=year)

    if db_yield is None:
        raise HTTPException(
            status_code=404, detail=f"No yield for year {year} found.")

    return db_yield


add_pagination(app)
