# Corteva Challenge by Seb

Hi there, this is my repo for Corteva's challenge. Thank you for putting me on this challenge. It was great fun!
Please find the following aspects in this README.

1. Instructions on how to run / test the code of this repository
2. My approach
3. Answers to Problems 1 - 4
4. Misc
5. Open Questions

## 1. Instructions on how to run / test the code of this repository

- $ bash setup.sh: to install dependencies
- $ bash run.sh: to start the FastAPI server, and ingest the data. Please interact with the server via localhost:8000/docs/ (compare giphy). The server can be stopped with 'control+c' on MacOS. Ingestion logs are provided in docs under ingestion.log.
- $ bash tests.sh: to run the unit tests. Please find a report in docs/test_report.html. Attention: They only succeed if the run script, was run once since the database is only ingested in that process.
- $ bash cleanup.sh: to remove all generated files to reset the project (i.e., database, test_report, logs).
- $ bash docker.sh: Optionally run the server in a Docker container for easy deployment. (Please make sure you have Docker installed on your machine.)
  - Docker must be installed in order to use it. It can be downloaded from: <https://www.docker.com/>
  - Once the container is running, you can open the CLI and run the tests in there, as the bash scripts are also avaible.

## 2. My Approach

1. In order to advance this coding assignment, I started with getting an overview of the data by conducting an exploratory analysis of the provided data. Please check docs/data_exploration.ipynb for my approach.
2. Next, I researched different technology options, and decided to implement the assignment with FastAPI and a SQLAlchemy server (justification in Answer 4).
3. After having running systems, I reused the code from the exploratory phase to ingest the database.
4. Then, I went through the prompt and identified additional requirements to implement (testing, pagination, duplicate checking) and considered extensions (bash scripts, docker) to make using this repository more convenient (please use docs/todos.md as a resource).
5. Finally, I compiled this readme file.

## 3. Answers to Problems 1 - 4

### Answer to Problem 1: Data Modeling

In this assingment, we'll use SQLite, because it uses a single file and Python has integrated support.
The data models look as follows (from src/models.py):

`
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
`

Please note, that stationId is an Integer, since I truncated the USC in every file. This is a design choice, and could be reversed quickly. This is an aspect I want to clarify (see open question at the end).

### Answer to Problem 2: Ingestion

The weather and field data will be ingested upon startup of the server. I used Pandas and Numpy extract (from txt files), transform (e.g. groupby functions) and load (bulk save to database) to ingest the database. The bulk approach was chosen to fill in the data since it is the most efficient use of Python. Duplicates are being checked in the transformation (implemented in pandas) earlier in the process.
Please note that the ingestion runs automatically upon server startup.

### Answer to Problem 3 - Data Analysis

All calculations are being conducted in the file 'ingest.py', and carefully explained in docs/data_exploration.ipynb. Please refer to docs/data_exploration.ipynb for understanding my approach. Thank you.

Please find the model definition below (from src/models.py):

`
  class WeatherStatistics(Base):
    __tablename__ = 'weatherStatistics'
    # station id could also be a string, just saying.
    stationId = Column(Integer, primary_key=True)
    year = Column(Integer, primary_key=True)
    maxTempAvg = Column(Float, nullable=True)
    minTempAvg = Column(Float, nullable=True)
    precipitationSum = Column(Integer, nullable=True)
`

### Answer to Problem 4 - REST API

As a web framework, I use FastAPI since it comes with an integrated openAPI front end that provides a convenient way to interact with the microservices (<http://localhost:8000/docs>). Flask and Django are also great options, and I would have been okay implementing this, if it would have been a requirement.

There are tests for the APIs, its results can be found in docs/report.html. You can run tests after the server was started, since the startup process only ingests the data base.

## 4. Misc

Thank you for reviewing, Seb.

The following resources helped a lot for compiling this repository:

- <https://www.andrewvillazon.com/move-data-to-db-with-sqlalchemy/>
- <https://fastapi.tiangolo.com/tutorial/sql-databases/>

## 5. Open questions

- In the data, I removed the prefix of the stationId which was a redundant 'USC'. This allowed me to save the stationId as an Integer. Would you prefer the full String as a stationId?
