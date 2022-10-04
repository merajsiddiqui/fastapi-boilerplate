from schema.user import UserLogin
from database.models.user import User


def validate_credentials(credentials: UserLogin) -> User | None:
    if credentials.email == 'merajsiddiqui@outlook.com' and credentials.password == 'kota@9811':
        return User(email = credentials.email, password = credentials.password)
    return None
