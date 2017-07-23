from datetime import datetime

from sqlalchemy import Boolean, Column, UniqueConstraint, ForeignKey
from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
# from api.api import db
#from flask.ext.sqlalchemy import SQLAlchemy
#from api import config
#from .api import app

Base = declarative_base()


#app.config.from_object(config)
#db = SQLAlchemy(app)

class Data(Base):
    """A recorded entry of a data of a specified type, sent by the equipment of a certain user."""
    __tablename__ = 'Data'
    id = Column(Integer, primary_key= True, autoincrement=True)
    id_device = Column(Integer, ForeignKey("Device.id"), nullable=False)
    type = Column(String(100))
    created = Column(DateTime, default=datetime.now)
    updated = Column(DateTime, default=datetime.now)
    value = Column(String(255))

    def __repr__(self):
        return (u'<{self.__class__.__name__}: id={self.id}, \
        id_device={self.id_device}, type={self.type}, value={self.value}>'
                .format(self=self))

class User(Base):
    """An user account"""
    __tablename__ = 'User'
    id = Column(Integer, primary_key= True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    token = Column(String(100))
    created = Column(DateTime, default=datetime.now)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    devices = relationship('Device', backref='user')

    def __repr__(self):
        return (u'<{self.__class__.__name__}: id={self.id}, \
        name={self.name}, email={self.email}>'.format(self=self))

# class Location(Base):
#     """A recorded entry for a location sent by an equipment of a certain user."""
#     __tablename__ = 'Location'
#     id = Column(Integer, primary_key= True, autoincrement=True)
#     id_device = Column(Integer, ForeignKey("Device.id"), nullable=False)
#     created = Column(DateTime, default=datetime.now)
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
#     registered = Column(DateTime, nullable=False)
#
#     def __repr__(self):
#         return (u'<{self.__class__.__name__}: id={self.id}, \
#                  id_device={self.id_device}>'.format(self=self))

class Device(Base):
    """An entry describing a device belonging to a certain user"""
    __tablename__ = "Device"
    id = Column(Integer, primary_key= True, autoincrement=True)
    id_user = Column(Integer, ForeignKey('User.id'), nullable=False)
    name = Column(String(100), nullable=False)
    serial = Column(String(100), nullable=False, unique=True)
    paired = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.now)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    # locations = relationship('Location', backref='device-location')
    # sensors = relationship('Sensor', backref='device-sensor')
    datas = relationship('Data', backref='device')

    @property
    def token(self):
        return ''.join(e for e in sorted(set(self.serial), reverse=True))

    def __repr__(self):
        return (u'<{self.__class__.__name__}: id={self.id}, \
                serial={self.serial} >'.format(self=self))




if __name__ == '__main__':
    # from datetime import datetime, timedelta
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    # Creates the database
    engine = create_engine('mysql://vss:1!vss@vss.lupu.online/db', echo=True)

    # Creates the database tables if they do not exist.
    Base.metadata.create_all(engine)
    # The engine connects to the database & executes queries.
    Session = sessionmaker(bind=engine)
    session = Session()

    # Add a sample username
    user1 = User(name='Cristian Lupu',
                email='cristianlupu@gmail.com',
                password='secret')
    session.add(user1)
    # session.commit()
    # Add device for user
    device1 = Device(
        user= user1,
        serial='SERIAL_NUMBER',
        description='Raspberry Pi 2'
    )
    session.add(device1)
    # session.commit()
    # Add sample data from a sensor
    # now = datetime.now()
    data1 = Data(
        device = device1,
        type="temperature",
        value="33"
    )
    session.add(data1)
    session.commit()
    #Add a sample location

    # registered_date='210316'
    # registered_day = registered_date[0:2]
    # registered_month = registered_date[2:4]
    # registered_year= '20'+ registered_date[4:6]
    # registered_time= '191016.1'
    # registered_hour = registered_time[0:2]
    # registered_minute = registered_time[2:4]
    # registered_second = int(registered_time[4:6])
    # registered_microsecond = registered_time[7]
    # dt = datetime(
    #     int(registered_year),
    #     int(registered_month),
    #     int(registered_day),
    #     int(registered_hour),
    #     int(registered_minute),
    #     int(registered_second)
    # )
    # print(">>>>>>>>>>"+str(dt))
    # location1 = Location(
    #     device = device1,
    #     latitude = '4426.788279',
    #     north = True,
    #     longitude = '02603.527478',
    #     east = True,
    #     altitude = 13,
    #     registered= dt
    # )
    # session.add(location1)
    # session.commit()

    # Demonstration Queries

    # Get a listing by ID.
    user11 = session.query(User).get(1)
    device11 = session.query(Device).get(1)
    data11 = session.query(Data).get(1)
    # location11 = session.query(Location).get(1)
    print('user:{}, device: {}, data: {}'.format(user11,device11,data11))

    # Get all listings
    # appts = session.query(User).all()
    # appts = session.query(Device).all()
    # appts = session.query(Sensor).all()
    # appts = session.query(Location).all()

    # # Get all appointments before right now, after right now.
    # appts = session.query(Appointment).filter(Appointment.start < datetime.now()).all()
    # appts = session.query(Appointment).filter(Appointment.start >= datetime.now()).all()
    #
    # # Get all appointments before a certain date.
    # appts = session.query(Appointment).filter(Appointment.start <= datetime(2013, 5, 1)).all()
    #
    # # Get the first appointment matching the filter query.
    # appt = session.query(Appointment).filter(Appointment.start <= datetime(2013, 5, 1)).first()
