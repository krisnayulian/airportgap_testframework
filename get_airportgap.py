import requests
from assertpy import assert_that


def test_calculate_distance():
    payload = {
        "from": "LAE",
        "to": "NRT"
    }
    response = requests.post("https://airportgap.com/api/airports/distance", data=payload)
    data = response.json().get("data")
    assert_that(data["type"]).is_equal_to("airport_distance")
    assert_that(data["attributes"]).is_not_empty()
    assert_that(data).has_id("LAE-NRT")
    assert_that(data["attributes"]["kilometers"]).is_equal_to(4753.834755437252)


def test_get_airports_by_id_wrong_assertpy():
    """
    This one is to test how it's looks like when having error
    since we can not modify the response to be error, so what we can do is
    to make assertion is false
    """
    airport_id = "LAE"
    # action/WHEN
    response = requests.get(f'https://airportgap.com/api/airports/{airport_id}')
    data = response.json().get('data')
    data_airport = data["attributes"]
    # assertion/THEN
    assert_that(response.status_code).is_equal_to(200)
    assert_that(data_airport["name"]).contains("Airport")
    assert_that(data_airport["name"]).is_equal_to_ignoring_case("I want you to failed this times")