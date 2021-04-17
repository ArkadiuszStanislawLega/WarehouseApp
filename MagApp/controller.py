from Models.models import Warehouse, DigitalReading, Device, Sensor
from database import db
from sqlalchemy import desc
import datetime


class MagAppController:
    STRING_LABEL_TEMPERATURE = " temperatura"
    STRING_LABEL_HUMIDITY = " wilgotność"

    def __init__(self, model, view):
        self.__model = model
        self.__view = view
        self.__view.confirm_button['command'] = self.create_graph
        self.__view.refresh_db['command'] = self.refresh_table
        self.refresh_table()
        self.__view.show()
        self.__labels = {}

    def refresh_table(self):
        warehouses = Warehouse.query.all()
        devices = Device.query.all()
        sensors = Sensor.query.all()
        values = {}
        for w in warehouses:
            for d in devices:
                for s in sensors:
                    dr = DigitalReading.query.filter(DigitalReading.sensor_id == s.id).order_by(
                        desc(DigitalReading.id)).limit(1).all()
                    dr = dr[0]
                    time = dr.time.strftime("%d-%m-%y %H:%M:%S")
                    values[s.id] = (w.name,
                                    d.name,
                                    s.id,
                                    s.name,
                                    round(dr.temperature, 2),
                                    round(dr.humidity, 2),
                                    time)

        self.__view.refresh(values)

    def prepare_data_from_db(self, date=None):
        date_range = {}
        filtered = {}
        curItem = self.__view.table.focus()
        for i in self.__view.table.selection():
            ids = int(self.__view.table.item(i, 'tag')[0])

            date_range[ids] = DigitalReading.query.filter(
                DigitalReading.sensor_id == ids).all()

            if date:
                filtered[ids] = []
                for sensor in date_range[ids]:
                    if sensor.time > date:
                        filtered.get(ids).append(sensor)

        if date:
            return filtered
        else:
            return date_range

    def create_humadity(self, sensors):
        values = {}
        for sensor in sensors:
            hum_key = sensor
            temp_key = sensor
            self.__labels[sensor] = sensor
            values[hum_key] = []

            for digital_read in sensors.get(sensor):
                values.get(hum_key).append(digital_read.humidity)

        return values

    def create_temperatures(self, sensors):
        values = {}
        for sensor in sensors:
            hum_key = sensor
            temp_key = sensor
            self.__labels[sensor] = sensor
            values[temp_key] = []
            for digital_read in sensors.get(sensor):
                values.get(temp_key).append(digital_read.temperature)

        return values

    def create_temp_and_humidity(self, sensors):
        values = {}
        for sensor in sensors:
            hum_key = str(sensor) + self.STRING_LABEL_HUMIDITY
            temp_key = str(sensor) + self.STRING_LABEL_TEMPERATURE

            self.__labels[hum_key] = hum_key
            self.__labels[temp_key] = temp_key

            values[hum_key] = []
            values[temp_key] = []

            for digital_read in sensors.get(sensor):
                values.get(hum_key).append(digital_read.humidity)
                values.get(temp_key).append(digital_read.temperature)

        return values

    def create_graph(self):
        self.__labels = {}
        warehouses = Warehouse.query.all()

        times = []
        sensors = {}
        d = datetime.datetime(2021, 4, 15)
        sensors = self.prepare_data_from_db()

        if len(sensors) > 0:
            for i in sensors.keys():
                # Upewnianie się że mamy jednakowy dystans czasowy.
                # Tworzę tabele z czasami które były zbierane w określonym czasie.
                for digital_read in sensors.get(i):
                    times.append(digital_read.time)

                break

            # Flagi wskazujące czy wykres ma być złożony z temperatury
            # i wilgoci, czy tylko jeden parametrów jest wybrany.
            is_temp = self.__view.is_temperature_selected.get()
            is_hum = self.__view.is_humidity_selected.get()

            if is_hum and not is_temp:
                self.__view.show_graph(times=times,
                                       data=self.create_humadity(sensors),
                                       labels=self.__labels)
            elif is_temp and not is_hum:
                self.__view.show_graph(times=times,
                                       data=self.create_temperatures(sensors),
                                       labels=self.__labels)
            elif is_hum and is_temp:
                self.__view.show_graph(times=times,
                                       data=self.create_temp_and_humidity(
                                           sensors),
                                       labels=self.__labels)
