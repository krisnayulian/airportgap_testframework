from datetime import datetime

import requests
from assertpy import assert_that

BASE_URL = "https://airportgap.dev-tester.com/api"


def get_token(email, password):
    return requests.post(BASE_URL + "/tokens", data={
        "email": email,
        "password": password
    })


def get_my_favorite_airport(token):
    header = {
        "Authorization": f"Token {token}"
    }
    return requests.get(BASE_URL + "/favorites", headers=header)


def test_token():
    token = get_token(email="naruto@mailinator.com", password="shuriken")
    assert_that(token.status_code).is_equal_to(200)
    assert_that(token.json()).contains_key("token")
    assert_that(token.json().get("token")).is_not_empty()


def test_get_favorite():
    give_me_token = get_token(email="naruto@mailinator.com", password="shuriken")
    token = give_me_token.json().get("token")
    header = {
        "Authorization": f"Token {token}"
    }
    response = requests.get(BASE_URL + "/favorites", headers=header)
    data = response.json().get("data")
    assert_that(response.status_code).is_equal_to(200)
    assert_that(data).is_greater_than_or_equal_to(1)


def test_add_new_favorite():
    """
    Since the data is hardcoded, then it was not idempotent/repeatable
    This test will failed, if NRT already in my favorite list
    Need to remove after test teardown
    """
    give_me_token = get_token(email="naruto@mailinator.com", password="shuriken")
    token = give_me_token.json().get("token")

    before_add = get_my_favorite_airport(token)
    data_before = before_add.json().get("data")
    assert_that(before_add.text).does_not_contain("NRT")

    new_airport = {
        "airport_id": "NRT",
        "note": "I like Narita"
    }

    header = {
        "Authorization": f"Token {token}"
    }

    response = requests.post(BASE_URL + "/favorites", headers=header, data=new_airport)
    assert_that(response.status_code).is_equal_to(201)
    response_data = response.json().get("data")
    assert_that(response_data["attributes"]["airport"]["iata"]).is_equal_to(new_airport["airport_id"])
    assert_that(response_data["attributes"]["note"]).is_equal_to(new_airport["note"])

    after_add = get_my_favorite_airport(token)
    data_after = after_add.json().get("data")
    assert_that(len(data_after)).is_greater_than(len(data_before))
    assert_that(after_add.text).contains(new_airport["note"])


def test_update_favorite_note():
    give_me_token = get_token(email="naruto@mailinator.com", password="shuriken")
    token = give_me_token.json().get("token")

    before_add = get_my_favorite_airport(token)
    data_before = before_add.json().get("data")

    assert_that(len(data_before)).is_greater_than(0)
    id_airport_to_modify = data_before[0]["id"]

    header = {
        "Authorization": f"Token {token}"
    }

    # Add dynamic unique string with a timestamp
    new_note = {
        "note": f"The note for ID:{id_airport_to_modify} is changed at time: {datetime.now()} "
    }

    response = requests.patch(f"{BASE_URL}/favorites/{id_airport_to_modify}", headers=header, data=new_note)
    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.text).contains(new_note["note"])

    after_add = get_my_favorite_airport(token)
    data_after = after_add.json().get("data")
    for airport_data in data_after:
        if airport_data["id"] == id_airport_to_modify:
            print(f"Found the modified airport {id_airport_to_modify}")
            print("\nHere is the check for specific airport in an array data")
            assert_that(airport_data["attributes"]["note"]).is_equal_to(new_note["note"])


def test_delete_favorite():
    give_me_token = get_token(email="naruto@mailinator.com", password="shuriken")
    token = give_me_token.json().get("token")

    before_add = get_my_favorite_airport(token)
    data_before = before_add.json().get("data")

    assert_that(len(data_before)).is_greater_than(0)
    id_airport_to_delete = data_before[0]["id"]

    header = {
        "Authorization": f"Token {token}"
    }

    response = requests.delete(f"{BASE_URL}/favorites/{id_airport_to_delete}", headers=header)
    assert_that(response.status_code).is_equal_to(204)
    after_delete = get_my_favorite_airport(token)
    data_after = after_delete.json().get("data")
    assert_that(len(data_after)).is_less_than(len(data_before))