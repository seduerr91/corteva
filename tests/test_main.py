from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

# test if server is runnable


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == [
        'Hi Corteva team, thank you for checking my assignment.']

# get the first data point


def test_get_weather_first_datapoint():
    response = client.get("/api/weather/?page=1&size=1")
    assert response.status_code == 200
    assert [response.json()] == [
        {
            "items": [
                {
                    "stationId": 257715,
                    "date": "1985-01-01",
                    "maxTemp": -8,
                    "minTemp": -14,
                    "precipitation": 0
                }
            ],
            "total": 1729957,
            "page": 1,
            "size": 1
        }
    ]

# get the total length of data points


def test_get_weather_total_len_1729957():
    response = client.get("/api/weather/?page=1&size=1")
    assert response.status_code == 200
    assert [response.json()['total']] == [1729957]

# filtering for a station


def test_get_weather_filter_station_110072():
    response = client.get("/api/weather/?stationId=110072&page=1&size=1")
    assert response.status_code == 200
    assert [response.json()] == [
        {
            "items": [
                {
                    "stationId": 110072,
                    "date": "1985-01-01",
                    "maxTemp": -2,
                    "minTemp": -12,
                    "precipitation": 9
                }
            ],
            "total": 10865,
            "page": 1,
            "size": 1
        }
    ]

# filtering for a date & check length on that date


# WEATHER_STATISTICS_TESTS

# filtering for statistics # all elements in table
def test_get_weather_stats():
    response = client.get("/api/weather/stats/")
    assert response.status_code == 200
    assert response.json()['total'] == 4820

# Check random value


def test_get_weather_stats_for_station_110072():
    response = client.get("/api/weather/stats/?stationId=110072")
    assert response.status_code == 200

    assert response.json()['total'] == 30


# YIELD_TESTS

# get total length of yields in database
def test_get_yield():
    response = client.get("/api/yield/")
    assert response.status_code == 200
    assert response.json()['total'] == 30

# test yield for year 1988 should be 125194


def test_get_yield_for_1988():
    response = client.get("http://127.0.0.1:8000/api/yield/?year=1988")
    assert response.status_code == 200
    assert response.json()['items'][0]['yields'] == 125194
