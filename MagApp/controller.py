from Models.models import Warehouse, DigitalReading, Device, Sensor
from database import db
from sqlalchemy import desc


class MagAppController:
    STRING_LABEL_TEMPERATURE = " temperatura"
    STRING_LABEL_HUMIDITY = " wilgotność"

    def __init__(self, model, view):
        self.__model = model
        self.__view = view
        self.__view.confirm_button['command'] = self.create_graph

        self.__view.show()

    def create_graph(self):
        warehouses = Warehouse.query.all()

        times = []
        labels = {}
        values = {}

        # 4: DigitalReading.query.filter(DigitalReading.sensor_id == 4).limit(100).all()

        sensors = {
            1: DigitalReading.query.filter(DigitalReading.sensor_id == 1).all(),
            2: DigitalReading.query.filter(DigitalReading.sensor_id == 2).all(),
            3: DigitalReading.query.filter(DigitalReading.sensor_id == 3).all(),
            4: DigitalReading.query.filter(DigitalReading.sensor_id == 4).all()
        }

        for i in sensors.get(1):
            times.append(i.time)

        is_temp = self.__view.is_temperature_selected.get()
        is_hum = self.__view.is_humidity_selected.get()

        for i in sensors:

            hum_key = i
            temp_key = i

            if is_hum and not is_temp:
                labels[i] = i
                values[hum_key] = []

            elif is_temp and not is_hum:
                labels[i] = i
                values[temp_key] = []

            elif is_hum and is_temp:
                hum_key = str(i) + self.STRING_LABEL_HUMIDITY
                temp_key = str(i) + self.STRING_LABEL_TEMPERATURE

                labels[hum_key] = hum_key
                labels[temp_key] = temp_key

                values[hum_key] = []
                values[temp_key] = []

            for x in sensors.get(i):
                if self.__view.is_humidity_selected.get() and not self.__view.is_temperature_selected.get():
                    values.get(hum_key).append(x.humidity)

                elif self.__view.is_temperature_selected.get() and not self.__view.is_humidity_selected.get():
                    values.get(temp_key).append(x.temperature)

                elif self.__view.is_humidity_selected.get() and self.__view.is_temperature_selected.get():
                    values.get(hum_key).append(x.humidity)
                    values.get(temp_key).append(x.temperature)

        self.__view.show_graph(times=times, data=values, labels=labels)
