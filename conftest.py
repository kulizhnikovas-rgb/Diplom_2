import pytest
import requests
import allure
from data.urls import URL
from helpers.user_helper import generate_random_user_data

@pytest.fixture
def user():
    user_data = generate_random_user_data()

    with allure.step("Предусловие: Регистрация нового пользователя"):
        response = requests.post(URL.CREATE_USER, json=user_data)
        token = response.json().get("accessToken")
        
    yield user_data, token, response

    if token:
        with allure.step("Постусловие: Удаление пользователя"):
            requests.delete(URL.USER_DATA, headers={"Authorization": token})


@pytest.fixture
def valid_ingredients():
    response = requests.get(URL.INGREDIENTS)
    ingredients_data = response.json().get("data", [])
    return [ing["_id"] for ing in ingredients_data[:2]]

@pytest.fixture
def register_user():
    user_info = {"token": None}

    yield user_info

    if user_info["token"]:
        with allure.step("Постусловие: Удаление зарегистрированного пользователя"):
            requests.delete(URL.USER_DATA, headers={"Authorization": user_info["token"]})