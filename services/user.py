from schema.user import UserLogin, UserRegister
from database.models.user import User
from config.database import get_database
from sqlalchemy import or_

database = get_database()


def validate_credentials(credentials: UserLogin) -> User | None:
    # Use database here to query
    db = next(database)
    user = db.query(User).filter(email = credentials.email).first()
    print(user)
    return None


def create_user(user: UserRegister) -> User | Exception:
    db = next(database)
    u = db.query(User).filter(or_(email = user.email, mobile_number = user.mobile_number)).first()
    print(u, 'here')
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


def update_profile():
    pass


def change_password():
    pass
