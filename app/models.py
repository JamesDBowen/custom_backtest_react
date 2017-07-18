import warnings
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Boolean, UnicodeText, create_engine, func
from sqlalchemy.orm import relationship, sessionmaker
from app import app, db, manager


class Series(db.Model):
    __tablename__ = 'series'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    custom = Column(Boolean,default=False)
    symbol = Column(String(20))
    data = Column(UnicodeText)
    profile_id = Column(ForeignKey("profile.id"))
    profile = db.relationship("Profile")

    #profiles = db.relationship('Profile', secondary=SeriesProfile, backref='series' )
    
class Profile(db.Model):
    __tablename__ = 'profile'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    start_amount = Column(Integer)
    monthly_addition = Column(Integer)
    start_date = Column(Date)
    end_date = Column(Date)
    series = db.relationship("Series")
    start_y = Column(Integer)

    
manager.create_api(Series, methods=['GET'])
manager.create_api(Profile, methods=['GET'])
