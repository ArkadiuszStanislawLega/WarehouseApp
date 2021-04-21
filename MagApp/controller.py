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
        self.__view.sensor_detail_view.cancel_button['command'] = self.cancel_edit_sensor
        self.__view.sensor_detail_view.confirm_button['command'] = self.confirm_edit_sensor
        self.__view.add_warehouse_view.add_button['command'] = self.add_warehouse
        self.__view.add_device_view.add_button['command'] = self.add_device
        self.__view.add_sensor_view.add_button['command'] = self.add_sensor
        self.__view.right_section.table.bind(
            '<<TreeviewSelect>>', self.fill_sensor_profile)

        self.refresh_table()
        self.refresh_warehouses_list()
        self.refresh_devices_list()
        self.__view.show()
        self.__labels = {}

    def refresh_table(self):
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
                        time = dr.time.strftime("%d-%m-%y %H:%M:%S")
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
                                        "--",
                                        "--",
                                        "--")

        self.__view.right_section.refresh(values)

    def __prepare_data_from_db(self, from_date=None, to_date=None):
        full_data = {}
        filtered = {}
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

    def confirm_edit_sensor(self):
        self.edit_sensor

    def cancel_edit_sensor(self):
        self.__view.sensor_detail_view.cancel_edit()
        self.edit_sensor()

    def fill_sensor_profile(self, event):
        curItem = self.__view.right_section.table.focus()

        id = int(self.__view.right_section.table.item(curItem,  'tags')[0])

        dr = DigitalReading.query.filter(DigitalReading.sensor_id == id).order_by(
            desc(DigitalReading.id)).limit(1).all()
        s = Sensor.query.filter(Sensor.id == id).first()
        d = Device.query.filter(Device.id == s.device_id).first()
        w = Warehouse.query.filter(Warehouse.id == d.warehouse_id).first()

        if len(dr) > 0:
            self.__view.sensor_detail_view.set_sensor(
                warehouse=w, device=d, sensor=s, digital_read=dr[0])
        else:
            self.__view.sensor_detail_view.set_sensor(
                warehouse=w, device=d, sensor=s, digital_read=DigitalReading())

        if self.__view.sensor_detail_view.is_edit_mode_on:
            self.edit_sensor()

    def add_warehouse(self):
        w = Warehouse()
        w.name = self.__view.add_warehouse_view.entry_value
        db.session.add(w)
        db.session.commit()
        self.refresh_table()
        self.refresh_warehouses_list()
        self.refresh_devices_list()

    def refresh_warehouses_list(self):
        self.__view.add_device_view.update_warehouses_list(
            values=Warehouse.query.all())

    def add_device(self):
        d = Device()
        d.warehouse_id = int(self.__view.add_device_view.selected_id())
        d.name = self.__view.add_device_view.device_name()
        db.session.add(d)
        db.session.commit()
        self.refresh_table()

    def refresh_devices_list(self):

        self.__view.add_sensor_view.update_device_list(
            values=Device.query.all())

    def add_sensor(self):
        s = Sensor()
        s.device_id = self.__view.add_sensor_view.selected_id()
        s.name = self.__view.add_sensor_view.sensor_name()
        db.session.add(s)
        db.session.commit()
        self.refresh_table()
