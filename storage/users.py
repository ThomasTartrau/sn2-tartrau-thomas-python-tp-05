from passlib.context import CryptContext

from storage.todos import Todos

class Users:
    pwd_context: CryptContext = None
    users = []

    def __init__(self, pwd_context: CryptContext):
        self.pwd_context = pwd_context

    def get(self):
        return self.users
    
    def get_by_username(self, username):
        for u in self.users:
            if u.username == username:
                return u
        return None
    
    def add(self, user):
        if self.get_by_username(user.username) is not None:
            return False
        self.users.append(user)
        return True
    
    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password):
        return self.pwd_context.hash(password)
