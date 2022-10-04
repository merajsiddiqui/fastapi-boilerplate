from schema.user import UserLogin
from database.models.user import User
from config.database import get_database

database = get_database()


def validate_credentials(credentials: UserLogin) -> User | None:
    # Use database here to query
    if credentials.email == 'merajsiddiqui@outlook.com' and credentials.password == 'kota@9811':
        return User(email = credentials.email, password = credentials.password)
    return None
