from schema.user import UserLogin, UserRegister
from database.models.user import User
from config.database import DBContext
from sqlalchemy import or_

database = DBContext().database


def validate_credentials(credentials: UserLogin) -> User | Exception:
    # Use database here to query
    user = database.query(User).filter(User.email == credentials.email, User.user_type == credentials.user_type).first()
    if user is None or not user.validate_password(credentials.password) or user.user_type != credentials.user_type:
        raise Exception(401, "Email or password is invalid")

    return user


def create_user(user: UserRegister) -> User | Exception:
    u = database.query(User).filter(or_(User.email == user.email, User.mobile_number == user.mobile_number)).first()
    if u is not None:
        raise Exception(422, 'This email or mobile no. already exists')
    u = User(
        name = user.full_name,
        email = user.email,
        password = user.password,
        user_type = user.user_type,
        mobile_number = user.mobile_number
    )
    database.add(u)
    database.commit()
    return u


def update_profile():
    pass


def change_password(user: User, old_password: str, new_password: str):
    db = next(database)
    if user.password == old_password:
        user.password = new_password
        db.update(user)
        db.commit()


def mark_mobile_number_verified(mobile_number: str):
    db = next(database)
    user = db.query(User).filter(mobile_number = mobile_number).first()
    user.mobile_verified = True
    db.update(user)
    db.commit()
