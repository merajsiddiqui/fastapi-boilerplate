import bcrypt
from abc import ABC
from sqlalchemy.sql import func
from config.database import Base
from sqlalchemy.orm import validates
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, TypeDecorator


class PasswordHash(Mutable):
    def __init__(self, hash_, rounds = None):
        assert len(hash_) == 60, 'bcrypt hash should be 60 chars.'
        assert (str(hash_)).count('$'), 'bcrypt hash should have 3x "$".'
        self.hash = str(hash_)
        self.rounds = int(self.hash.split('$')[2])
        self.desired_rounds = rounds or self.rounds

    def __eq__(self, candidate):
        """Hashes the candidate string and compares it to the stored hash.

        If the current and desired number of rounds differ, the password is
        re-hashed with the desired number of rounds and updated with the results.
        This will also mark the object as having changed (and thus need updating).
        """
        if isinstance(candidate, str):
            candidate = candidate.encode('utf8')
            if self.hash == bcrypt.hashpw(candidate, self.hash.encode('utf8')):
                if self.rounds < self.desired_rounds:
                    self._rehash(candidate)
                return True
        return False

    def __repr__(self):
        """Simple object representation."""
        return '<{}>'.format(type(self).__name__)

    @classmethod
    def coerce(cls, key, value):
        """Ensure that loaded values are PasswordHashes."""
        if isinstance(value, PasswordHash):
            return value
        return super(PasswordHash, cls).coerce(key, value)

    @classmethod
    def new(cls, password, rounds):
        """Returns a new PasswordHash object for the given password and rounds."""
        if isinstance(password, str):
            password = password.encode('utf8')
        return cls(cls._new(password, rounds))

    @staticmethod
    def _new(password, rounds):
        """Returns a new bcrypt hash for the given password and rounds."""
        return bcrypt.hashpw(password, bcrypt.gensalt(rounds))

    def _rehash(self, password):
        """Recreates the internal hash and marks the object as changed."""
        self.hash = self._new(password, self.desired_rounds)
        self.rounds = self.desired_rounds
        self.changed()


class Password(TypeDecorator):
    """Allows storing and retrieving password hashes using PasswordHash."""
    impl = Text

    def __init__(self, rounds = 12, **kwds):
        self.rounds = rounds
        super(Password, self).__init__(**kwds)

    def process_bind_param(self, value, dialect):
        """Ensure the value is a PasswordHash and then return its hash."""
        return self._convert(value).hash

    def process_result_value(self, value, dialect):
        """Convert the hash to a PasswordHash, if it's non-NULL."""
        if value is not None:
            return PasswordHash(value, rounds = self.rounds)

    def validator(self, password):
        """Provides a validator/converter for @validates usage."""
        return self._convert(password)

    def _convert(self, value):
        """Returns a PasswordHash from the given string.

        PasswordHash instances or None values will return unchanged.
        Strings will be hashed and the resulting PasswordHash returned.
        Any other input will result in a TypeError.
        """
        if isinstance(value, PasswordHash):
            return value
        elif isinstance(value, str):
            return PasswordHash.new(value, self.rounds)
        elif value is not None:
            raise TypeError(
                'Cannot convert {} to a PasswordHash'.format(type(value)))


class User(Base):
    __tablename__ = 'users'

    id = Column('id', Integer, primary_key = True, autoincrement = True)
    name = Column('name', String(50))
    email = Column('email', String(100), unique = True)
    email_verified = Column('email_verified', Boolean, default = False)
    password = Column(Password(13))
    mobile_number = Column('mobile_number', String(11), nullable = False)
    mobile_verified = Column('mobile_verified', Boolean, default = False)
    profile_image = Column('profile_image', Text)
    user_type = Column('user_type', String)
    created_at = Column('created_at', DateTime, default = func.now())
    updated_at = Column('updated_at', DateTime, nullable = True, onupdate = func.now())
    deleted_at = Column('deleted_at', DateTime, nullable = True)

    @validates('password')
    def _validate_password(self, key, password):
        return getattr(type(self), key).type.validator(password)
