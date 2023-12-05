import requests
from assertpy import assert_that


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