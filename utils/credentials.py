from faker import Faker

class Credentials:
    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name

    def toRegisterMap(self):
        return {
            "email": self.email,
            "password": self.password,
            "name": self.name
        }
    
    def toLoginMap(self):
        return {
            "email": self.email,
            "password": self.password
        }
    
    def toIncorrectRegisterMap(self):
        return {
            "email": self.email,
            "name": self.name
        }

    @staticmethod
    def registered_user():
        return Credentials('arinaTestCourier@denum.ru', 'testpass12', 'Arina')

class CredentialsGenerator:
    @staticmethod
    def generate():
        faker = Faker()
        return Credentials(faker.email(), faker.password(), faker.first_name())
