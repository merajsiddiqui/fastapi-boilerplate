from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.database import Base


class Doctor(Base):
    __tablename__ = 'doctors'

    id = Column('id', Integer, primary_key = True)
    registration_number = Column('mci_registration_number', Integer)
    smc_id = Column('smc_id', Integer, nullable = True)
    specialization = Column('specialization', String(20), nullable = True)
    experience_years = Column('experience_years', Integer, nullable = True)
    user_id = Column('user_id', Integer, ForeignKey('users.id'), index = True, nullable = False)
    created_at = Column('created_at', DateTime, default = func.now())
    updated_at = Column('updated_at', DateTime, nullable = True, onupdate = func.now())
    deleted_at = Column('deleted_at', DateTime, nullable = True)

    user = relationship("User", backref = 'doctors')  # class name of the model
