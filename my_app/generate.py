from my_app.models.users import Users
from my_app.utils import fake_data_generator

if __name__ == '__main__':
    for i in range(200):
        data = fake_data_generator(Users)
        Users.insert(data)
