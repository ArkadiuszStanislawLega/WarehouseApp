from datetime import datetime, date
from database import db


class Warehouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    sensor = db.relationship('Sensor', backref='warehouse')

    def __repr__(self):
        return str(id) + " " + self.name


class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'))
    digital_reading_id = db.relationship('DigitalReading', backref='sensor')

    def __repr__(self):
        return str(self.id) + " " + self.name + " " + str(self.warehouse_id)


class DigitalReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=date.today())
    time = db.Column(db.DateTime, default=datetime.now())
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    sensor_id = db.Column(db.Integer(), db.ForeignKey('sensor.id'))

    def __repr__(self):
        time = self.time.strftime("%H:%M:%S")
        return str(self.sensor_id) + ". Godzina: " + str(time) + ", temp: " + str(round(self.temperature, 2)) + "C, wilg: " + str(round(self.humidity, 2)) + "%"

    def Printing(self):
        time = self.time.strftime("%H:%M:%S")
        print(". Godzina: " + str(time) + ", temp: " + str(round(self.temperature, 2)
                                                           ) + "C, wilg: " + str(round(self.humidity, 2)) + "%")
