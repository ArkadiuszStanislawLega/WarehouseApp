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
        self.__view.create_graph_view.confirm_button['command'] = self.create_graph
        self.__view.create_graph_view.refresh_db['command'] = self.refresh_table
        self.__view.sensor_detail_view.edit_button['command'] = self.edit_sensor
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
                                    s.name,
                                    round(dr.temperature, 2),
                                    round(dr.humidity, 2),
                                    time)

        self.__view.refresh(values)

    def __prepare_data_from_db(self, from_date=None, to_date=None):
        full_data = {}
        filtered = {}
        curItem = self.__view.table.focus()
        for i in self.__view.table.selection():
            ids = int(self.__view.table.item(i, 'tag')[0])

            full_data[ids] = DigitalReading.query.filter(
                DigitalReading.sensor_id == ids).all()

            if from_date:
                filtered[ids] = []
                for sensor in full_data[ids]:
                    if sensor.time >= from_date and sensor.time <= to_date:
                        filtered.get(ids).append(sensor)

        if from_date:
            return filtered
        else:
            return full_data

    def __create_readings(self, sensors, temperature=False):
        values = {}
        for sensor in sensors:
            hum_key = sensor
            temp_key = sensor
            self.__labels[sensor] = sensor
            values[temp_key] = []
            for digital_read in sensors.get(sensor):
                if temperature:
                    values.get(temp_key).append(digital_read.temperature)
                else:
                    values.get(temp_key).append(digital_read.humidity)

        return values

    def __create_temp_and_humidity(self, sensors):
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
        sensors = {}
        times = []

        from_date = self.__view.create_graph_view.get_from_date()
        to_date = self.__view.create_graph_view.get_to_date()

        if from_date and to_date:
            sensors = self.__prepare_data_from_db(from_date=from_date,
                                                  to_date=to_date)
        else:
            sensors = self.__prepare_data_from_db()

        # d = datetime.datetime(2021, 4, 15)

        if len(sensors) > 0:
            for i in sensors.keys():
                # Upewnianie się że mamy jednakowy dystans czasowy.
                # Tworzę tabele z czasami które były zbierane w określonym czasie.
                for digital_read in sensors.get(i):
                    times.append(digital_read.time)

                break

            # Flagi wskazujące czy wykres ma być złożony z temperatury
            # i wilgoci, czy tylko jeden parametrów jest wybrany.
            is_temp = self.__view.create_graph_view.is_temperature_selected.get()
            is_hum = self.__view.create_graph_view.is_humidity_selected.get()

            # Wyświetlenie wilgotności
            if is_hum and not is_temp:
                self.__view.create_graph_view.show_graph(times=times,
                                                         data=self.__create_readings(
                                                             sensors),
                                                         labels=self.__labels)
            # Wyświetlenie temperatury
            elif is_temp and not is_hum:
                self.__view.create_graph_view.show_graph(times=times,
                                                         data=self.__create_readings(sensors,
                                                                                     temperature=True),
                                                         labels=self.__labels)
            # Wyświetelnie temperatury i wilgotności
            elif is_hum and is_temp:
                data = self.__create_temp_and_humidity(sensors)
                self.__view.create_graph_view.show_graph(times=times,
                                                         data=data,
                                                         labels=self.__labels)

    def edit_sensor(self):
        self.__view.sensor_detail_view.switch_edit_mode()
