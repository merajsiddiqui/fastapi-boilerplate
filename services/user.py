from schema.user import UserLogin, UserRegister
from database.models.user import User
from config.database import get_database

database = get_database()


def validate_credentials(credentials: UserLogin) -> User | None:
    # Use database here to query
    if credentials.email == 'merajsiddiqui@outlook.com' and credentials.password == 'kota@9811':
        return User(email = credentials.email, password = credentials.password)
    return None


def create_user(user: UserRegister):
    db = next(database)
    u = User(
        name = user.full_name,
        email = user.email,
        password = user.password,
        user_type = user.user_type,
        mobile_number = user.mobile_number
    )
    db.add(u)
    db.commit()
    return u
