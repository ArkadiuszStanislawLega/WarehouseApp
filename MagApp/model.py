from Models.models import Warehouse, DigitalReading, Device, Sensor
from database import db
from sqlalchemy import desc


class MagAppModel:
    STRING_EMPTY_VALUE = "--"
    FORMAT_DATE = "%d-%m-%y %H:%M:%S"
    STRING_LABEL_TEMPERATURE = " temperatura"
    STRING_LABEL_HUMIDITY = " wilgotność"

    def __init__(self):
        self.__labels = {}
        self.__times = []
        self.__graph_values = {}

    @property
    def labels(self):
        return self.__labels

    @property
    def times(self):
        return self.__times

    @property
    def graph_values(self):
        return self.__graph_values
    
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

    def __prepare_data_from_db(self, selected, from_date=None, to_date=None):
        full_data = {}
        filtered = {}
        for i in selected.selection():
            ids = int(selected.item(i, 'tag')[0])

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
        self.__graph_values.clear()
        self.__labels.clear()
        for sensor in sensors:
            temp_key = sensor
            self.__labels[sensor] = sensor
            self.__graph_values[temp_key] = []
            for digital_read in sensors.get(sensor):
                if temperature:
                    self.__graph_values.get(temp_key).append(digital_read.temperature)
                else:
                    self.__graph_values.get(temp_key).append(digital_read.humidity)

        return self.__graph_values

    def __create_temp_and_humidity(self, sensors):
        self.__graph_values.clear()
        self.__labels.clear()
        for sensor in sensors:
            hum_key = str(sensor) + self.STRING_LABEL_HUMIDITY
            temp_key = str(sensor) + self.STRING_LABEL_TEMPERATURE

            self.__labels[hum_key] = hum_key
            self.__labels[temp_key] = temp_key

            self.__graph_values[hum_key] = []
            self.__graph_values[temp_key] = []

            for digital_read in sensors.get(sensor):
                self.__graph_values.get(hum_key).append(digital_read.humidity)
                self.__graph_values.get(temp_key).append(digital_read.temperature)

        return self.__graph_values

    def create_graph(self, from_date, to_date, selected, temperature= False, both=False):
 
        values = {}
        self.__times.clear()

        if from_date and to_date:
            values = self.__prepare_data_from_db(from_date=from_date, 
                                                 to_date=to_date,
                                                 selected=selected)
        else:
            values = self.__prepare_data_from_db(selected=selected)

        if len(values) > 0:
            for i in values.keys():
                # Upewnianie się że mamy jednakowy dystans czasowy.
                # Tworzę tabele z czasami które były zbierane w określonym czasie.
                for digital_read in values.get(i):
                    self.__times.append(digital_read.time)

                break

        if not both:
            self.__create_readings(values, temperature)
        else:
            self.__create_temp_and_humidity(values)