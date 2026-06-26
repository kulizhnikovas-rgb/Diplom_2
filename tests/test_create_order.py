import requests
import allure
from data.urls import URL
from data.data import INVALID_INGREDIENTS

@allure.epic("Stellar Burgers API")
@allure.feature("Создание заказа")
class TestCreateOrder:
    
    @allure.title("Создание заказа с авторизацией")
    def test_create_order_authorized_user_success(self, user, valid_ingredients):
        _, token, _ = user
        payload = {"ingredients": valid_ingredients}
        headers = {"Authorization": token}

        with allure.step("Отправить POST-запрос на создание заказа с токеном авторизации"):
            response = requests.post(URL.CREATE_ORDER, json=payload, headers=headers)
            
        with allure.step("Проверить успешный ответ сервера"):
            assert response.status_code == 200
            assert response.json().get("success") is True 
            assert "order" in response.json() 

    @allure.title("Создание заказа без авторизации")
    def test_create_order_unauthorized_user_success(self, valid_ingredients):
        payload = {"ingredients": valid_ingredients}
        
        with allure.step("Отправить POST-запрос без хедера Authorization"):
            response = requests.post(URL.CREATE_ORDER, json=payload)
            
        with allure.step("Проверить статус 200"):
            assert response.status_code == 200
            assert response.json().get("success") is True
    
    @allure.title("Успешное создание заказа с валидными ингредиентами")
    def test_create_order_valid_ingredients_success(self, valid_ingredients):
        payload = {"ingredients": valid_ingredients}
        
        with allure.step("Отправить POST-запрос с валидным списком ингредиентов"):
            response = requests.post(URL.CREATE_ORDER, json=payload)
            
        with allure.step("Проверить, что заказ успешно создан"):
            assert response.status_code == 200
            assert response.json().get("success") is True


    @allure.title("Ошибка создания заказа без ингредиентов")
    def test_create_order_missing_ingredients_shows_error(self):
        payload = {"ingredients": []}
        
        with allure.step("Отправить POST-запрос с пустым массивом ингредиентов"):
            response = requests.post(URL.CREATE_ORDER, json=payload)
            
        with allure.step("Проверить ошибку 400 Bad Request и сообщение"):
            assert response.status_code == 400 
            assert response.json().get("success") is False 
            assert response.json().get("message") == "Ingredient ids must be provided"

    @allure.title("Ошибка создания заказа с неверным хешем ингредиентов")
    def test_create_order_invalid_ingredients_shows_error(self): 
        payload = {"ingredients": INVALID_INGREDIENTS}
        
        with allure.step("Отправить POST-запрос со сломанным хешем"):
            response = requests.post(URL.CREATE_ORDER, json=payload)
            
        with allure.step("Проверить, что сервер падает с ошибкой 500 Internal Server Error"):
            assert response.status_code == 500