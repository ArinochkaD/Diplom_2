import allure
import pytest
import requests

from utils.constants import LoginErrorsText, Urls
from utils.credentials import Credentials

class TestLoginUser:
    @allure.feature('Функциональность авторизации пользователя.')
    @allure.title('Проверка успешной авторизации пользователя.')
    def test_login_user(self, registered_credentials: Credentials):
        url = Urls.BASE_URL + Urls.AUTH_USER_PATH
        with allure.step("Запрос авторизации пользователя."):
            response = requests.post(url, registered_credentials.toLoginMap())
        assert response.status_code == 200 and response.json()['accessToken'] is not None

    @allure.feature('Функциональность авторизации пользователя.')
    @allure.title('Проверка ошибки авторизации пользователя.')
    @allure.testcase('Авторизация с неправильным email или паролем.')
    @pytest.mark.parametrize('data', [
        {
            "email": Credentials.registered_user().email,
            "password": Credentials.registered_user().password + 'wrong',
        },
        {
            "email": Credentials.registered_user().email + 'wrong',
            "password": Credentials.registered_user().password,
        }
    ])
    def test_error_login_incorrect_data(self, data):
        url = Urls.BASE_URL + Urls.AUTH_USER_PATH
        with allure.step("Запрос авторизации пользователя с неверными данными."):
            response = requests.post(url, data)
        assert response.status_code == 401 and LoginErrorsText.INCORRECT in response.json()['message']

    @allure.feature('Функциональность авторизации пользователя.')
    @allure.title('Проверка ошибки авторизации пользователя.')
    @allure.testcase('Авторизация без email или пароля.')
    @pytest.mark.parametrize('data', [
        {
            "email": Credentials.registered_user().email,
            "password": "",
        },
        {
            "email": "",
            "password": Credentials.registered_user().password,
        }
    ])
    def test_error_login_without_data(self, data):
        url = Urls.BASE_URL + Urls.AUTH_USER_PATH
        with allure.step("Запрос авторизации пользователя с отсутствием данных."):
            response = requests.post(url, data)
        assert response.status_code == 401 and LoginErrorsText.INCORRECT in response.json()['message']
