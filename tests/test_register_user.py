import allure
import requests

from utils.constants import Urls, RegisterErrorsText
from utils.credentials import Credentials

class TestRegisterUser:
    @allure.feature('Функциональность создания пользователя.')
    @allure.title('Проверка успешной регистрации пользователя.')
    def test_register_user(self, credentials: Credentials, delete_user):
        url = Urls.BASE_URL + Urls.CREATE_USER_PATH
        with allure.step("Запрос регистрации пользователя."):
            response = requests.post(url, credentials.toRegisterMap())
        assert response.status_code == 200 and response.json()['success'] == True
        delete_user(credentials)

    @allure.feature('Функциональность создания пользователя.')
    @allure.title('Проверка ошибки регистрации зарегистрированного пользователя.')
    def test_error_register_registered_user(self, credentials: Credentials, delete_user):
        url = Urls.BASE_URL + Urls.CREATE_USER_PATH
        with allure.step("Запрос регистрации пользователя."):
            requests.post(url, credentials.toRegisterMap())
        with allure.step("Запрос регистрации уже зерегистрированного пользователя."):
            response = requests.post(url, credentials.toRegisterMap())
        assert response.status_code == 403 and RegisterErrorsText.ALREADY_EXISTS in response.json()['message'] and response.json()['success'] is False
        delete_user(credentials)

    @allure.feature('Функциональность создания пользователя.')
    @allure.title('Проверка ошибки регистрации пользователя при неполных данных.')
    def test_error_register_incorrect_credentials(self, credentials: Credentials):
        url = Urls.BASE_URL + Urls.CREATE_USER_PATH
        with allure.step("Запрос регистрации пользователя с неверными данными."):
            response = requests.post(url, credentials.toIncorrectRegisterMap())
        assert response.status_code == 403 and RegisterErrorsText.INCORRECT_DATA in response.json()['message'] and response.json()['success'] is False

    @allure.feature('Функциональность создания пользователя.')
    @allure.title('Проверка успешности удаления зарегистрированного пользователя.')
    def test_delete_registered_user(self, credentials: Credentials):
        with allure.step("Запрос регистрации пользователя."):
            requests.post(Urls.BASE_URL + Urls.CREATE_USER_PATH, credentials.toRegisterMap())
        with allure.step("Запрос авторизации зарегистрированного пользователя."):
            login_response = requests.post(Urls.BASE_URL + Urls.AUTH_USER_PATH, credentials.toLoginMap())
        access_token = login_response.json()['accessToken']
        headers = {"Authorization": f"{access_token}"}
        with allure.step("Запрос на удаление зарегистрированного пользователя."):
            delete_response = requests.delete(Urls.BASE_URL + Urls.DELETE_USER_PATH, headers=headers)
        assert delete_response.status_code == 202
