from peewee import *
import datetime

db_msos = MySQLDatabase("msos.db")


class BaseModel(Model):
    class Meta:
        database = db_msos


class Vehicle(BaseModel):
    # 因为我们没有指定主键，Peewee将自动添加一个名为 id.
    passing_time = IntegerField()
    line = IntegerField()
    sum = IntegerField()
    num_motor = IntegerField()
    num_small_car = IntegerField()
    num_big_car = IntegerField()
    num_truck = IntegerField()
    num_trailer = IntegerField()
    average_speed = IntegerField()
    speed_motor = IntegerField()
    speed_small_car = IntegerField()
    speed_big_car = IntegerField()
    speed_truck = IntegerField()
    speed_trailer = IntegerField()
    average_car_spacing = IntegerField()
    average_car_length = IntegerField()
    average_occupancy = IntegerField()
    created_data = DateTimeField(default=datetime.datetime.now())
