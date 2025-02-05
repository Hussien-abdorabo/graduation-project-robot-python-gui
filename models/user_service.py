import random

class UserService:
    def __init__(self):
        self.SIMULATED_USERS = [
            {"username": "Alice", "age": 28, "email": "alice@example.com"},
            {"username": "Bob", "age": 32, "email": "bob@example.com"},
            {"username": "Charlie", "age": 25, "email": "charlie@example.com"}
        ]

    def get_random_user(self):
        """ Returns a randomly selected user. """
        return random.choice(self.SIMULATED_USERS)
