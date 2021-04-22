from Models.models import Warehouse, DigitalReading, Device, Sensor
from database import db
from sqlalchemy import desc
import datetime


class MagAppController:

    def __init__(self, model, view):
        self.__model = model
        self.__view = view
        self.__view.left_section.create_graph_view.confirm_button['command'] = self.create_graph
        self.__view.left_section.create_graph_view.refresh_db['command'] = self.refresh_table
        self.__view.left_section.sensor_detail_view.edit_button['command'] = self.edit_sensor
        self.__view.left_section.sensor_detail_view.cancel_button[
            'command'] = self.cancel_edit_sensor
        self.__view.left_section.sensor_detail_view.confirm_button[
            'command'] = self.confirm_edit_sensor
        self.__view.left_section.add_warehouse_view.add_button['command'] = self.add_warehouse
        self.__view.left_section.add_device_view.add_button['command'] = self.add_device
        self.__view.left_section.add_sensor_view.add_button['command'] = self.add_sensor
        self.__view.right_section.table.bind(
            '<<TreeviewSelect>>', self.fill_sensor_profile)

        self.refresh_table()
        self.refresh_warehouses_list()
        self.refresh_devices_list()
        self.__view.show()
        self.__labels = {}

    def refresh_table(self):
        self.__view.right_section.refresh(self.__model.data_for_table())

    def create_graph(self):
        # Flagi wskazujące czy wykres ma być złożony z temperatury
        # i wilgoci, czy tylko jeden parametrów jest wybrany.
        is_temp = self.__view.left_section.create_graph_view.is_temperature_selected.get()
        is_hum = self.__view.left_section.create_graph_view.is_humidity_selected.get()

        from_date = self.__view.left_section.create_graph_view.get_from_date()
        to_date = self.__view.left_section.create_graph_view.get_to_date()

        # Wyświetlenie wilgotności
        if is_hum and not is_temp:
            self.__model.create_graph(from_date=from_date, 
                                      to_date=to_date,
                                      selected=self.__view.right_section.table)
            self.__view.left_section.create_graph_view.show_graph(times=self.__model.times,
                                                                  data=self.__model.graph_values,
                                                                  labels=self.__model.labels)
        # Wyświetlenie temperatury
        elif is_temp and not is_hum:
            self.__model.create_graph(from_date=from_date, 
                                      to_date=to_date, 
                                      selected=self.__view.right_section.table, 
                                      temperature=True)
            self.__view.left_section.create_graph_view.show_graph(times=self.__model.times,
                                                                      data=self.__model.graph_values,
                                                                      labels=self.__model.labels)
        # Wyświetelnie temperatury i wilgotności
        elif is_hum and is_temp:
            self.__model.create_graph(from_date=from_date, 
                                      to_date=to_date, 
                                      selected=self.__view.right_section.table, 
                                      both=True)
            self.__view.left_section.create_graph_view.show_graph(times=self.__model.times,
                                                                  data=self.__model.graph_values,
                                                                  labels=self.__model.labels)

    def edit_sensor(self):
        self.__view.left_section.sensor_detail_view.switch_edit_mode()

    def confirm_edit_sensor(self):
        self.edit_sensor

    def cancel_edit_sensor(self):
        self.__view.left_section.sensor_detail_view.cancel_edit()
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
            self.__view.left_section.sensor_detail_view.set_sensor(
                warehouse=w, device=d, sensor=s, digital_read=dr[0])
        else:
            self.__view.left_section.sensor_detail_view.set_sensor(
                warehouse=w, device=d, sensor=s, digital_read=DigitalReading())

        if self.__view.left_section.sensor_detail_view.is_edit_mode_on:
            self.edit_sensor()

    def add_warehouse(self):
        w = Warehouse()
        w.name = self.__view.left_section.add_warehouse_view.entry_value
        db.session.add(w)
        db.session.commit()
        self.refresh_table()
        self.refresh_warehouses_list()
        self.refresh_devices_list()

    def refresh_warehouses_list(self):
        self.__view.left_section.add_device_view.update_warehouses_list(
            values=Warehouse.query.all())

    def add_device(self):
        d = Device()
        d.warehouse_id = int(
            self.__view.left_section.add_device_view.selected_id())
        d.name = self.__view.left_section.add_device_view.device_name()
        db.session.add(d)
        db.session.commit()
        self.refresh_table()

    def refresh_devices_list(self):

        self.__view.left_section.add_sensor_view.update_device_list(
            values=Device.query.all())

    def add_sensor(self):
        s = Sensor()
        s.device_id = self.__view.left_section.add_sensor_view.selected_id()
        s.name = self.__view.left_section.add_sensor_view.sensor_name()
        db.session.add(s)
        db.session.commit()
        self.refresh_table()
