import requests
import allure
from data.urls import URL


@allure.epic("Stellar Burgers API")
@allure.feature("Авторизация пользователя")
class TestLoginUser:
    
    @allure.title("Успешный вход под существующим пользователем")
    def test_login_user_valid_credentials_success(self, user):
        user_data, _, _ = user

        login_payload = {
            "email": user_data["email"],
            "password": user_data["password"]
        }

        with allure.step("Отправить POST-запрос на авторизацию"):
            response = requests.post(URL.LOGIN_USER, json=login_payload)
            
        with allure.step("Проверить статус 200 и наличие токена"):
            assert response.status_code == 200
            assert response.json().get("success") is True
            assert "accessToken" in response.json()

    @allure.title("Ошибка авторизации с неверным логином и паролем")
    def test_login_user_invalid_credentials_shows_error(self):
        invalid_payload = {
            "email": "wrong_burger_email_123@yandex.ru",
            "password": "wrong_password_999"
        }
        
        with allure.step("Отправить запрос с невалидными кредами"):
            response = requests.post(URL.LOGIN_USER, json=invalid_payload)
            
        with allure.step("Проверить ошибку 401 Unauthorized"):
            assert response.status_code == 401
            assert response.json().get("success") is False


