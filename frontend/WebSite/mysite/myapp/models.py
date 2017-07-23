from __future__ import unicode_literals

from django.contrib.auth.models import update_last_login, user_logged_in
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
import hashlib
import random
import string
from django.contrib.auth.models import UserManager, BaseUserManager

user_logged_in.disconnect(update_last_login)

from datetime import datetime
#import sqlalchemy, sqlalchemy.orm


class MyUserManager(BaseUserManager):
    def create_user(self, login, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not login:
            raise ValueError('Users must have an email address')

        user = self.model(
            login=self.normalize_email(login),
            name=name,
        )

        user.field_created = datetime.now()
        user.field_updated = user.field_created
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            login,
        )
        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(models.Model):
    USERNAME_FIELD = 'login'
    field_created = models.DateTimeField(db_column='_created', blank=True, null=True)  # Field renamed because it started with '_'.
    field_updated = models.DateTimeField(db_column='_updated', blank=True, null=True)  # Field renamed because it started with '_'.
    field_etag = models.CharField(db_column='_etag', max_length=40, blank=True, null=True)  # Field renamed because it started with '_'.
    name = models.CharField(max_length=100)
    login = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=100)
    token = models.CharField(max_length=100, blank=True, null=True)
    salt = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    # id = models.IntegerField(primary_key= True, autoincrement=True)

    objects = MyUserManager()

    class Meta:
        #managed = False
        db_table = 'User'


    def __str__(self):
        return (u'<{self.__class__.__name__}: id={self.id}, \
        name={self.name}, login={self.login}>'.format(self=self))


    def check_password(self, password):
        if not self.password:
            return False
        return self.encrypt(password) == self.password

    def encrypt(self, password):
        """Encrypt password using hashlib and current salt.
        """
        return str(hashlib.sha1(password.encode('utf-8') + str(self.salt).encode('utf-8')).hexdigest())

    def set_password(self, value):
        self.salt = self.generate_salt()
        self.password = self.encrypt(value)

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def generate_salt(self):
        return ''.join(random.sample(string.ascii_letters, 12))


class Device(models.Model):
    field_created = models.DateTimeField(db_column='_created', blank=True, null=True)  # Field renamed because it started with '_'.
    field_updated = models.DateTimeField(db_column='_updated', blank=True, null=True)  # Field renamed because it started with '_'.
    field_etag = models.CharField(db_column='_etag', max_length=40, blank=True, null=True)  # Field renamed because it started with '_'.
    id_user = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user')
    name = models.CharField(max_length=100)
    serial = models.CharField(unique=True, max_length=100)
    paired = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Device'


class Input(models.Model):
    field_created = models.DateTimeField(db_column='_created', blank=True, null=True)  # Field renamed because it started with '_'.
    field_updated = models.DateTimeField(db_column='_updated', blank=True, null=True)  # Field renamed because it started with '_'.
    field_etag = models.CharField(db_column='_etag', max_length=40, blank=True, null=True)  # Field renamed because it started with '_'.
    id_device = models.ForeignKey(Device, models.DO_NOTHING, db_column='id_device')
    id_user = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user')
    pid = models.CharField(max_length=10)
    value = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'Input'



"""
    SQL tables.
    This is a typical declarative usage of sqlalchemy,
    It has no dependency on flask or eve iself. Pure sqlalchemy.
"""

'''
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
#from werkzeug.security import generate_password_hash
import hashlib
import string
import random
#from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
#from itsdangerous import SignatureExpired, BadSignature
from sqlalchemy.orm import validates
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime



SECRET_KEY = 'this-is-my-super-secret-key'
Base = declarative_base()


engine = sqlalchemy.create_engine('mysql://vss:1!vss@vss.lupu.online/db')
Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()

class CommonColumns(Base):
    __abstract__ = True
    _created = Column(DateTime, default=datetime.now)
    _updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    _etag = Column(String(40))

    # @hybrid_property
    # def _id(self):
    #     """
    #     Eve backward compatibility
    #     """
    #     return self.id

class User(CommonColumns):
    """An user account"""
    __tablename__ = 'User'
    id = Column(Integer, primary_key= True, autoincrement=True)
    name = Column(String(100), nullable=False)
    login = Column(String(100), nullable=False, unique=True)
    password = Column('password', String(100),nullable=False)
    token = Column(String(100))
    salt = Column(String(100))
    phone = Column(String(15))
    devices = relationship('Device', backref='user')
    inputs = relationship('Input', backref='user')
    # locations = relationship('Location', backref='user')
    #    token = column_property(firstname + " " + lastname)
    #
    def _get_password(self):
        return self._password
    
    def _set_password(self, password):
        if password:
            password = password.strip()
        self._password = encrypt(password)

    password_descriptor = property(_get_password,
                                   _set_password)
    # password = synonym('_password',
    #                    descriptor=password_descriptor)
    #
    #def check_password(self, password):
    #    if self.password is None:
    #        return False
    #    password = password.strip()
    #    if not password:
    #        return False
    #    return check_password_hash(self.password, password)
    #
    # @classmethod
    # def authenticate(cls, query, email, password):
    #     email = email.strip().lower()
    #     user = query(cls).filter(cls.email == email).first()
    #     if user is None:
    #         return None, False
    #     if not user.active:
    #         return user, False
    #     return user, user.check_password(password)

    #def generate_auth_token(self, expiration=24*60*60):
    #    """Generates token for given expiration
    #    and user login."""
    #    s = Serializer(SECRET_KEY, expires_in=expiration)
    #    return s.dumps({'login': self.login })

    #@staticmethod
    #def verify_auth_token(token):
    #    """Verifies token and eventually returns
    #   user login.
    #   """
    #    s = Serializer(SECRET_KEY)
    #    try:
    #        data = s.loads(token)
    #    except SignatureExpired:
    #       return None # valid token, but expired
    #    except BadSignature:
    #        return None # invalid token
    #    return data['login']

    # def isAuthorized(self, role_names):
    #     """Checks if user is related to given role_names.
    #     """
    #     allowed_roles = set([r.id for r in self.roles]) \
    #         .intersection(set(role_names))
    #     return len(allowed_roles) > 0

    #def generate_salt(self):
    #    return ''.join(random.sample(string.ascii_letters, 12))

    def encrypt(self, password):
        """Encrypt password using hashlib and current salt.
        """
        return str(hashlib.sha1(password.encode('utf-8') + str(self.salt).encode('utf-8')).hexdigest())

    #@validates('password')
    #def _set_password(self, key, value):
    #    """Using SQLAlchemy validation makes sure each
    #    time password is changed it will get encrypted
    #    before flushing to db.
    #    """
    #    self.salt = self.generate_salt()
    #    return self.encrypt(value)

    def check_password(self, password):
        if not self.password:
            return False
        return self.encrypt(password) == self.password


    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    #@hybrid_property
    #def id_user(self):
    #    """
    #    Eve backward compatibility
    #    """
    #    return self.id
    # @hybrid_property
    # def user_id(self):
    #     """
    #     Eve backward compatibility
    #     """
    #     return self.id

    def __repr__(self):
        return (u'<{self.__class__.__name__}: id={self.id}, \
        name={self.name}, login={self.login}>'.format(self=self))



class Device(CommonColumns):
    """An entry describing a device belonging to a certain user"""
    __tablename__ = "Device"
    id = Column(Integer, primary_key= True, autoincrement=True)
    id_user = Column(Integer, ForeignKey('User.id'), nullable=False)
    # people = relationship(People, uselist=False)
    name = Column(String(100), nullable=False)
    serial = Column(String(100), nullable=False, unique=True)
    paired = Column(Boolean, default=True)
    inputs = relationship('Input', backref='device')
    # locations = relationship('Location', backref='device')

    # @property
    # def token(self):
    #     return ''.join(e for e in sorted(set(self.serial), reverse=True))

    def __repr__(self):
        return (u'<{self.__class__.__name__}: id={self.id}, \
                serial={self.serial} >'.format(self=self))

class Input(CommonColumns):
    """A recorded entry of a data of a specified type, sent by the equipment of a certain user."""
    __tablename__ = 'Input'
    id = Column(Integer, primary_key= True, autoincrement=True)
    id_device = Column(Integer, ForeignKey("Device.id"), nullable=False)
    id_user = Column(Integer, ForeignKey('User.id'), nullable=False)
    pid = Column(String(10), nullable=False)
    value = Column(String(255),nullable=False)

    def __repr__(self):
        return (u'<{self.__class__.__name__}: id={self.id}, id_device={self.id}, value={self.value}>'\
                .format(self=self))

# class Output(CommonColumns):

# class Location(Base):
#     """A recorded entry for a location sent by an equipment of a certain user."""
#     __tablename__ = 'Location'
#     id = Column(Integer, primary_key= True, autoincrement=True)
#     id_device = Column(Integer, ForeignKey("Device.id"), nullable=False)
#     id_user = Column(Integer, ForeignKey('User.id'), nullable=False)
#     #format:    ddmm.mmmmmm d: degree; m: minute
#     #example:   4140.831527 [E/W]
#     latitude = Column(String(11),nullable=False)
#     #True = North, False = South
#     north = Column(Boolean, default=True)
#     #format:    dddmm.mmmmmm d: degree; m: minute
#     #example:   00053.173495
#     longitude = Column(String(12),nullable=False)
#     #True = East, False = West
#     east = Column(Boolean, default=True)
#     #format:    meters
#     #example:   293
#     altitude = Column(Integer)
#     #format: yyyy-mm-dd hh:mm:ss
#     #example: 2016-05-13 16:20:20
#     #registered = Column(DateTime, nullable=False)

    def __repr__(self):
        return (u'<{self.__class__.__name__}: id={self.id}, \
                 id_device={self.id}>'.format(self=self))

'''