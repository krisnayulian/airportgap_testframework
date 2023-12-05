import requests
from assertpy import assert_that

BASE_URL = "https://airportgap.dev-tester.com/api"


def test_get_all_airports():
    response = requests.get(f'{BASE_URL}/airports')
    data = response.json().get('data')

    assert_that(response.status_code).is_equal_to(200)
    assert_that(data).is_greater_than_or_equal_to(5)


def test_get_airports_by_id():
    # arrange/GIVEN
    airport_id = "LAE"
    # action/WHEN
    response = requests.get(f'{BASE_URL}/airports/{airport_id}')
    data = response.json().get('data')
    data_airport = data["attributes"]
    # assertion/THEN
    assert_that(response.status_code).is_equal_to(200)
    assert_that(data_airport["name"]).is_equal_to("Nadzab Airport")


def test_get_not_found_airport():
    airport_id = "NOTFOUND"
    response = requests.get(f'{BASE_URL}/airports/{airport_id}')
    assert_that(response.status_code).is_equal_to(404)
    assert_that(response.json()).contains_key("errors")
    assert_that(response.text).contains("The page you requested could not be found")


def test_calculate_distance():
    payload = {
        "from": "LAE",
        "to": "NRT"
    }
    response = requests.post("https://airportgap.dev-tester.com/api/airports/distance", data=payload)
    data = response.json().get("data")
    assert_that(data["type"]).is_equal_to("airport_distance")
    assert_that(data["attributes"]).is_not_empty()
    assert_that(data).has_id("LAE-NRT")
    assert_that(data["attributes"]["kilometers"]).is_equal_to(4753.834755437252)
