from Models.models import Warehouse, DigitalReading, Device, Sensor
from database import db
from sqlalchemy import desc


class MagAppController:
    def __init__(self, model, view):
        self.__model = model
        self.__view = view
        self.__view.confirm_button['command'] = self.create_graph

        self.__view.show()

    def create_graph(self):
        warehouses = Warehouse.query.all()

        times = []
        labels = {}
        temp = {}

        # 4: DigitalReading.query.filter(DigitalReading.sensor_id == 4).limit(100).all()

        sensors = {
            1: DigitalReading.query.filter(DigitalReading.sensor_id == 1).all(),
            2: DigitalReading.query.filter(DigitalReading.sensor_id == 2).all(),
            3: DigitalReading.query.filter(DigitalReading.sensor_id == 3).all(),
            4: DigitalReading.query.filter(DigitalReading.sensor_id == 4).all()
        }

        for i in sensors.get(1):
            times.append(i.time)

        for i in sensors:
            labels[i] = i
            temp[i] = []
            for x in sensors.get(i):
                if self.__view.is_humidity_selected.get():
                    temp.get(i).append(x.humidity)
                elif self.__view.is_temperature_selected.get():
                    temp.get(i).append(x.temperature)

        self.__view.show_graph(times=times, data=temp, labels=labels)
