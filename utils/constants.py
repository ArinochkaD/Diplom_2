class Urls:
    BASE_URL = 'https://stellarburgers.education-services.ru'
    CREATE_USER_PATH = '/api/auth/register'
    DELETE_USER_PATH = '/api/auth/user'
    AUTH_USER_PATH = '/api/auth/login'
    CREATE_ORDER_PATH = '/api/orders'
    GET_INGREDIENTS_PATH = '/api/ingredients'

class RegisterErrorsText:
    ALREADY_EXISTS = "User already exists"
    INCORRECT_DATA = "Email, password and name are required fields"

class LoginErrorsText:
    INCORRECT = "email or password are incorrect"

class CreateOrderErrorsText:
    NO_INGREDIENTS_PROVIDED = "Ingredient ids must be provided"
    INTERNAL_SERVER_ERROR = "Internal Server Error"
