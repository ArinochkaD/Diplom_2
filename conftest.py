import sys
import os

import allure
import pytest
import requests

from utils.constants import Urls
from utils.credentials import Credentials, CredentialsGenerator

# Добавляем текущую директорию в sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

@pytest.fixture
def credentials():
    return CredentialsGenerator.generate()

@pytest.fixture
def registered_credentials():
    return Credentials.registered_user()

@pytest.fixture
def delete_user():
    def _delete(credentials: Credentials):
        with allure.step("Запрос авторизации зарегистрированного пользователя."):
            login_response = requests.post(Urls.BASE_URL + Urls.AUTH_USER_PATH, credentials.toLoginMap())
        access_token = login_response.json()['accessToken']
        headers = {"Authorization": f"{access_token}"}
        with allure.step("Запрос на удаление зарегистрированного пользователя."):
            delete_response = requests.delete(Urls.BASE_URL + Urls.DELETE_USER_PATH, headers=headers)
        return delete_response.status_code == 200
    return _delete

@pytest.fixture
def register_user():
    def _register(credentials: Credentials):
        with allure.step("Запрос регистрации пользователя."):
            requests.post(Urls.BASE_URL + Urls.CREATE_USER_PATH, credentials.toRegisterMap())
        with allure.step("Запрос авторизации зарегистрированного пользователя."):
            login_response = requests.post(Urls.BASE_URL + Urls.AUTH_USER_PATH, credentials.toLoginMap())
        access_token = login_response.json()['accessToken']
        return access_token
    return _register
