from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Sequence
from sqlalchemy import String, Integer, Float, Boolean, Column
from src import models
from src import schemas
import pandas as pd
import numpy as np
import os
import glob
import time
import logging

Base = declarative_base()

logging.basicConfig(filename="docs/ingestion.log", level=logging.INFO)


def transform_yields_data_to_df():
    logging.info(
        f'Reading and transforming Yield Data at: {time.strftime("%H:%M:%S")}')
    yield_files = "data/yld_data/"
    yield_frames = []
    columns = ['year', 'yields']
    for file in glob.glob(os.path.join(yield_files, "*.txt")):
        # logging.info(f'Processing file {file}.')
        frame = pd.read_csv(file, delimiter='\t', names=columns)
    logging.info(
        f'Yield data ready to insert at {time.strftime("%H:%M:%S")}.')
    frame = frame.drop_duplicates(
        keep='first', inplace=False, ignore_index=False)
    return frame


def transform_weather_data_to_df():
    logging.info(
        f'Reading and transforming Weather Data at: {time.strftime("%H:%M:%S")}')
    weather_files = "data/wx_data/"
    columns = ['date', 'temperature_max*10',
               'temperature_min*10', 'precipitation*10']
    weather_files_data = []
    for file in glob.glob(os.path.join(weather_files, "*.txt")):
        # logging.info(f'Processing file {file}.')
        weather_frame = pd.read_csv(file, delimiter='\t', names=columns)
        weather_frame['stationId'] = file[-12:-4]
        weather_files_data.append(weather_frame)
        weather_data_df = pd.concat(weather_files_data, ignore_index=True)

    weather_data_df = weather_data_df.replace(-9999, np.nan)
    weather_data_df = weather_data_df.drop_duplicates(
        keep='first', inplace=False, ignore_index=False)
    weather_data_df['temperature_max_celcius'] = weather_data_df['temperature_max*10'].div(
        10).round(2)
    weather_data_df['temperature_min_celcius'] = weather_data_df['temperature_min*10'].div(
        10).round(2)
    # divide tenths of millimeter by 10 to arrive at centimeter
    weather_data_df['precipitation_ml'] = weather_data_df['precipitation*10'].div(
        10).round(2)
    # get the year
    weather_data_df['dateTime'] = pd.to_datetime(
        weather_data_df['date'].astype(str), format='%Y%m%d')
    weather_data_df['year'] = pd.DatetimeIndex(
        weather_data_df['dateTime']).year
    weather_data_df_reduced = weather_data_df[[
        'stationId', 'dateTime', 'temperature_max_celcius', 'temperature_min_celcius', 'precipitation_ml']]
    weather_data_df_reduced.columns = [
        'stationId', 'date', 'maxTemp', 'minTemp', 'precipitation']
    logging.info(
        f'Weather data ready to insert at {time.strftime("%H:%M:%S")}.')
    return weather_data_df_reduced


def transform_weatherStatistics_data_to_df(weather_data):
    pd.options.mode.chained_assignment = None
    logging.info(
        f'Reading and transforming Weather Data for statistics calculation at: {time.strftime("%H:%M:%S")}')
    # get the year
    weather_data_df_reduced = weather_data
    weather_data_df_reduced['year'] = pd.DatetimeIndex(
        weather_data_df_reduced['date']).year
    # complete weather_data_df in one dataframe with year, stationID, temperature_max/min and precipitation

    weather_avg_temperatures = weather_data_df_reduced[[
        'stationId', 'year', 'maxTemp', 'minTemp']]
    weather_avg_temperatures = weather_avg_temperatures.groupby(
        ['stationId', 'year']).mean().reset_index()

    weather_sum_precipitation = weather_data_df_reduced[[
        'precipitation', 'stationId', 'year']]

    weather_sum_precipitation = weather_sum_precipitation.groupby(
        ['stationId', 'year']).sum().reset_index()

    # Attention: Double check if this is the best way
    weatherStatistics_data = pd.merge(weather_avg_temperatures, weather_sum_precipitation, on=[
        "stationId", 'year'], how="outer")
    weatherStatistics_data.columns = ['stationId', 'year',
                                      'maxTempAvg', 'minTempAvg', 'precipitationSum']
    logging.info(
        f'Weather Data Statistics ready to insert at: {time.strftime("%H:%M:%S")}')
    return weatherStatistics_data


def get_number_of_entries(db, model):
    print(f'Retrieving {model} records ...')
    records = db.query(model).count()
    logging.info(
        f'At {time.strftime("%H:%M:%S")}, there are {records} for model {model} in the database.')
    return records


def data_to_db(data, model, db):
    db.bulk_insert_mappings(
        model, data.to_dict(orient="records"))
    logging.info(
        f'Ended {data} ingestion at {time.strftime("%H:%M:%S")}, and ingested {data.shape[0]} records.')
    db.commit()
