import pytest
import requests
import allure
from data.urls import URL
from helpers.user_helper import generate_random_user_data

@allure.epic("Stellar Burgers API")
@allure.feature("Создание пользователя")
class TestCreateUser:
   
    @allure.title("Успешное создание уникального пользователя")
    def test_create_user_unique_data_success(self, register_user):
       user_data = generate_random_user_data()

       with allure.step("Отправить POST-запрос на регистрацию уникального пользователя"):
            response = requests.post(URL.CREATE_USER, json=user_data)

       with allure.step("Проверить статус-код и тело ответа"):
            assert response.status_code == 200
            assert response.json().get("success") is True

       token = response.json().get("accessToken")
       register_user["token"] = token

    @allure.title("Ошибка при создании уже зарегистрированного пользователя")
    def test_create_user_existing_data_shows_error(self, user):
        user_data, _, _ = user

        with allure.step("Повторно отправить запрос с теми же данными"):
            response = requests.post(URL.CREATE_USER, json=user_data)
            
        with allure.step("Проверить, что возвращается ошибка 403 Forbidden"):
            assert response.status_code == 403
            assert response.json().get("success") is False
            assert response.json().get("message") == "User already exists"
            
    @allure.title("Ошибка создания пользователя при незаполненном обязательном поле")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field_shows_error(self, missing_field):
        user_data = generate_random_user_data()
        user_data.pop(missing_field)

        with allure.step(f"Отправить POST-запрос без поля: {missing_field}"):
            response = requests.post(URL.CREATE_USER, json=user_data)

        with allure.step("Проверить, что возвращается ошибка 403"):
            assert response.status_code == 403
            assert response.json().get("success") is False
            assert response.json().get("message") == "Email, password and name are required fields"