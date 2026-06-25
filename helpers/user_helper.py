import random

def generate_random_user_data():
    num = random.randint(100000, 999000)
    return {
        "email": f"tester_{num}@yandex.ru",
        "password": f"pass_{num}",
        "name": f"User_{num}"
    }
