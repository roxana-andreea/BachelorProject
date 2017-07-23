"""
    SQL tables.
    This is a typical declarative usage of sqlalchemy,
    It has no dependency on flask or eve iself. Pure sqlalchemy.
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import column_property, relationship
from sqlalchemy import func
from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    ForeignKey,
    DateTime)
from sqlalchemy.orm import synonym
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash


Base = declarative_base()


# class CommonColumns(Base):
#     __abstract__ = True
    # _created = Column(DateTime, default=func.now())
    # _updated = Column(DateTime, default=func.now(), onupdate=func.now())
    # created = Column(DateTime, default=datetime.now)
    # updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    # _etag = Column(String(40))

    # @hybrid_property
    # def _id(self):
    #     """
    #     Eve backward compatibility
    #     """
    #     return self.id


class User(Base):
    """An user account"""
    __tablename__ = 'User'
    id_user = Column(Integer, primary_key= True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    token = Column(String(100))
#    token = column_property(firstname + " " + lastname)
    devices = relationship('Device', backref='user')
    datas = relationship('Data', backref='user')
    _password = Column('password', String(100))

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        if password:
            password = password.strip()
        self._password = generate_password_hash(password)

    password_descriptor = property(_get_password,
                                   _set_password)
    password = synonym('_password',
                       descriptor=password_descriptor)

    def check_password(self, password):
        if self.password is None:
            return False
        password = password.strip()
        if not password:
            return False
        return check_password_hash(self.password, password)

    @classmethod
    def authenticate(cls, query, email, password):
        email = email.strip().lower()
        user = query(cls).filter(cls.email == email).first()
        if user is None:
            return None, False
        if not user.active:
            return user, False
        return user, user.check_password(password)

    def __repr__(self):
        return (u'<{self.__class__.__name__}: id={self.id}, \
        name={self.name}, email={self.email}>'.format(self=self))



class Device(Base):
    """An entry describing a device belonging to a certain user"""
    __tablename__ = "Device"
    id_device = Column(Integer, primary_key= True, autoincrement=True)
    id_user = Column(Integer, ForeignKey('User.id_user'), nullable=False)
    # people = relationship(People, uselist=False)
    name = Column(String(100), nullable=False)
    serial = Column(String(100), nullable=False, unique=True)
    paired = Column(Boolean, default=False)
    datas = relationship('Data', backref='device')

    @property
    def token(self):
        return ''.join(e for e in sorted(set(self.serial), reverse=True))

    def __repr__(self):
        return (u'<{self.__class__.__name__}: id={self.id}, \
                serial={self.serial} >'.format(self=self))

class Data(Base):
    """A recorded entry of a data of a specified type, sent by the equipment of a certain user."""
    __tablename__ = 'Data'
    id_data = Column(Integer, primary_key= True, autoincrement=True)
    id_device = Column(Integer, ForeignKey("Device.id_device"), nullable=False)
    id_user = Column(Integer, ForeignKey('User.id_user'), nullable=False)
    type = Column(String(100),nullable=False)
    value = Column(String(255),nullable=False)

    def __repr__(self):
        return (u'<{self.__class__.__name__}: id={self.id}, \
        id_device={self.id_device}, type={self.type}, value={self.value}>'
                .format(self=self))

