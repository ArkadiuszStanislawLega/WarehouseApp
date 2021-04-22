from Models.models import Warehouse, DigitalReading, Device, Sensor
from database import db
from sqlalchemy import desc


class MagAppModel:
    STRING_EMPTY_VALUE = "--"
    FORMAT_DATE = "%d-%m-%y %H:%M:%S"

    def __init__(self):
        pass
    
    def data_for_table(self):
        w = Warehouse()
        d = Device()
        s = Sensor()

        values = {}
        war = Warehouse.query.all()
        dev = {}
        sen = {}

        for w in war:
            dev[w.id] = Device.query.filter(
                Device.warehouse_id == w.id).all()
            for d in dev[w.id]:
                sen[d.id] = Sensor.query.filter(Sensor.device_id == d.id).all()
                for s in sen[d.id]:
                    dr = DigitalReading.query.filter(DigitalReading.sensor_id == s.id).order_by(
                        desc(DigitalReading.id)).limit(1).all()
                    if len(dr) > 0:
                        dr = dr[0]
                        time = dr.time.strftime(self.FORMAT_DATE)
                        values[s.id] = (w.name,
                                        d.name,
                                        s.name,
                                        round(dr.temperature, 2),
                                        round(dr.humidity, 2),
                                        time)
                    else:
                        values[s.id] = (w.name,
                                        d.name,
                                        s.name,
                                        self.STRING_EMPTY_VALUE,
                                        self.STRING_EMPTY_VALUE,
                                        self.STRING_EMPTY_VALUE)

        return values