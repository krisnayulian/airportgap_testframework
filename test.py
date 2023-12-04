import requests


def test_get_all_airports():
    response = requests.get('https://airportgap.dev-tester.com/api/airports')
    data = response.json().get('data')

    assert response.status_code == 200
    assert len(data) > 5