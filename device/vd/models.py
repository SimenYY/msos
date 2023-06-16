"""
1. 建立orm模型
"""

from peewee import *
import datetime

db_msos = MySQLDatabase("msos.db")


class BaseModel(Model):
    class Meta:
        database = db_msos


class Vehicle(BaseModel):
    pass
