from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_load_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == [
        'Hi Corteva team, thank you for checking my assignment.']


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


def test_get_weather_count():
    response = client.get("/api/weather/?page=1&size=1")
    assert response.status_code == 200
    assert [response.json()['total']] == [1729957]


def test_get_yield_count():
    response = client.get("/api/yield/?page=1&size=1")
    assert response.status_code == 200
    assert [response.json()['total']] == [30]


def test_get_weather_statistics_count():
    response = client.get("/api/weather/stats/?page=1&size=1")
    assert response.status_code == 200
    assert [response.json()['total']] == [4820]


def test_get_weather_filter_station_110072():
    # testing my favorite station 110072 :)
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


def test_get_weather_stats_all_years_of_a_station():
    response = client.get(
        "api/weather/stats/?stationId=126580&page=1&size=50")
    assert response.status_code == 200
    assert response.json()['total'] == 30


def test_get_weather_stats_all_years_of_a_station_without_pagination_in_query_string():
    response = client.get("/api/weather/stats/?stationId=110072")
    assert response.status_code == 200
    assert response.json()['total'] == 30


def test_get_yield_value_for_year_1988():
    response = client.get("http://127.0.0.1:8000/api/yield/?year=1988")
    assert response.status_code == 200
    assert response.json()['items'][0]['yields'] == 125194
