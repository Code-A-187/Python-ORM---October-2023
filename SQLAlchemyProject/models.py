from sqlalchemy import create_engine
from settings import DATABASE_URL
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
Session = sessionmaker(binf=engine)
Base = declarative_base()

class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)


# Many-to-one relationship
class Order(Base):

    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    is_completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User')

# Base.metadata.create_all(engine)