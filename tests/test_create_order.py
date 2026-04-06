import allure
import pytest
import requests

from utils.constants import CreateOrderErrorsText, Urls
from utils.ingredients_ids import IngredientsIds

class TestCreateOrder:
    @allure.feature('Функциональность создания заказа.')
    @allure.title('Проверка успешного создания заказа с авторизацией пользователя.')
    @pytest.mark.parametrize('ingredients', [
        [IngredientsIds.BUN_KRATORNAYA],
        [IngredientsIds.BUN_KRATORNAYA, IngredientsIds.SAUCE_SPICY_X],
    ])
    def test_create_order_with_auth(self, credentials, register_user, delete_user, ingredients):
        access_token = register_user(credentials)
        url = Urls.BASE_URL + Urls.CREATE_ORDER_PATH
        headers={"Authorization": f"{access_token}"}
        data = {'ingredients': ingredients}
        with allure.step("Запрос создания заказа для авторизованного пользователя."):
            response = requests.post(url, headers=headers, data=data)
        assert response.status_code == 200 and response.json()['success'] == True
        delete_user(credentials)

    @allure.feature('Функциональность создания заказа.')
    @allure.title('Проверка успешного создания заказа без авторизации пользователя.')
    @pytest.mark.parametrize('ingredients', [
        [IngredientsIds.BUN_KRATORNAYA],
        [IngredientsIds.BUN_KRATORNAYA, IngredientsIds.SAUCE_SPICY_X],
    ])
    def test_create_order_without_auth(self, ingredients):
        url = Urls.BASE_URL + Urls.CREATE_ORDER_PATH
        data = {'ingredients': ingredients}
        with allure.step("Запрос создания заказа для неавторизованного пользователя."):
            response = requests.post(url, data=data)
        assert response.status_code == 200 and response.json()['success'] == True

    @allure.feature('Функциональность создания заказа.')
    @allure.title('Проверка ошибки создания заказа без ингридиентов.')
    def test_create_order_without_ingredients(self):
        url = Urls.BASE_URL + Urls.CREATE_ORDER_PATH
        data = {'ingredients': []}
        with allure.step("Запрос создания заказа без ингридиентов."):
            response = requests.post(url, data=data)
        assert response.status_code == 400 and response.json()['message'] == CreateOrderErrorsText.NO_INGREDIENTS_PROVIDED

    @allure.feature('Функциональность создания заказа.')
    @allure.title('Проверка ошибки создания заказа с неправильным id ингридиента.')
    @pytest.mark.parametrize('ingredients', [
        [IngredientsIds.BUN_KRATORNAYA + 'wrong'],
    ])
    def test_create_order_with_wrong_ingredients(self, ingredients):
        url = Urls.BASE_URL + Urls.CREATE_ORDER_PATH
        data = {'ingredients': ingredients}
        with allure.step("Запрос создания заказа с неправильным id ингридиента."):
            response = requests.post(url, data=data)
        assert response.status_code == 500 and CreateOrderErrorsText.INTERNAL_SERVER_ERROR in response.text
