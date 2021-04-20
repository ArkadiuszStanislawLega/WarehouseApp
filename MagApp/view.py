from tkinter import *
from tkinter import ttk

from MagApp.sensor_view import SensorView
from Models.models import Warehouse, DigitalReading, Device, Sensor
from matplotlib import pyplot as plt
from datetime import date, timedelta, datetime
from Fragments.sensor_detail_view import SensorDetailView
from Fragments.add_warehouse_view import AddWarehouseView
from Fragments.add_device_view import AddDeviceView
from Fragments.add_sensor_view import AddSensorView
from Fragments.create_graph_view import CreateGraphView
from Fragments.logo_view import LogoView


class MagAppView:
    # region constans
    SIZE_WINDOW_WIDTH = 1510
    SIZE_WINDOW_HEIGHT = 800
    SIZE_WINDOW = str(SIZE_WINDOW_WIDTH) + "x" + str(SIZE_WINDOW_HEIGHT)
    SIZE_ENTRY_WIDTH = 10
    SIZE_LIST_GRID_WIDTH = 20
    SIZE_LIST_GRID_COLUMN_PADX = 10
    SIZE_LOGO_WIDTH = 100
    SIZE_LOGO_HEIGHT = 100

    STRING_DAY = "Dzień:"
    STRING_MONTH = "Miesiąc:"
    STRING_YEAR = "Rok:"
    STRING_GRAPH_SETTINGS_TITLE = "Wykres czujników:"
    STRING_GRAPH_SELECT_RANGE_DATE = "Wskaż zakres dat:"
    STRING_SETTINGS_FROM = "od"
    STRING_SETTINGS_TO = "do"
    STRING_WAREHOUSE = "Magazyn"
    STRING_DEVICE = "Urządzenie"
    STRING_SENSOR = "Czujnik"
    STRING_TEMPERATURE = "Temperatura [°C]"
    STRING_HUMIDITY = "Wilgotność [%]"
    STRING_LAST_READ = "Ostatni odczyt"
    STRING_SENSOR_ID = "Id czujnika"
    STRING_SHOW_GRAPHS = "Pokaż wykres"
    STRING_REFRESH = "Odśwież"
    # endregion constans
    NUMBER_OF_DAYS_EARLIER = 31

    def __init__(self, version, logo_path):
        self.__logo_path = logo_path
        self.__window = Tk()
        self.__window.title("MagApp - v" + str(version))
        self.__window.geometry(self.SIZE_WINDOW)
        self.__window.iconphoto(False, PhotoImage(file=self.__logo_path))

        # region LeftSite
        self.__f_settings = Frame(self.__window)
        self.__f_settings.pack(side=LEFT)
        self.__logo_view = LogoView(master=self.__f_settings,
                                    file_path=self.__logo_path,
                                    height=self.SIZE_LOGO_HEIGHT,
                                    width=self.SIZE_LOGO_WIDTH)
        self.__sensor_detail_view = SensorDetailView(master=self.__f_settings)
        self.__add_warehouse_view = AddWarehouseView(self.__f_settings)
        self.__add_device_view = AddDeviceView(self.__f_settings)
        self.__add_sensor_view = AddSensorView(self.__f_settings)
        self.__create_graph_view = CreateGraphView(self.__f_settings)
        # endregion LeftSite
        # region RightSite
        self.__f_sensors_list = Frame(self.__window)
        self.__f_sensors_list.pack(side=RIGHT)

        self.__columns = [self.STRING_WAREHOUSE,
                          self.STRING_DEVICE,
                          self.STRING_SENSOR,
                          self.STRING_TEMPERATURE,
                          self.STRING_HUMIDITY,
                          self.STRING_LAST_READ]
        ac = (1, 2, 3, 4, 5, 6)
        self.__values = {}
        self.__tv_table = ttk.Treeview(self.__f_sensors_list,
                                       columns=ac,
                                       show="headings",
                                       height=100)

        self.__tv_table.column(ac[0], width=200, anchor=CENTER)
        self.__tv_table.column(ac[1], width=100, anchor=CENTER)
        self.__tv_table.column(ac[2], width=200, anchor=CENTER)
        self.__tv_table.column(ac[3], width=100, anchor=CENTER)
        self.__tv_table.column(ac[4], width=100, anchor=CENTER)
        self.__tv_table.column(ac[5], width=200, anchor=CENTER)

        # self.__tv_table.tag_bind('cb', '<<TreeviewSelect>>', cb)

        for i in range(len(ac)):
            self.__tv_table.heading(ac[i], text=self.__columns[i])

        self.__tv_table.pack(side=LEFT, fill=Y)

        self.__s_vertical_list = Scrollbar(self.__f_sensors_list,
                                           orient=VERTICAL)
        self.__s_vertical_list.pack(side=RIGHT, fill=Y)

        # endregion RightSite

    def show(self):
        mainloop()

    @property
    def create_graph_view(self):
        return self.__create_graph_view

    @ property
    def table(self):
        return self.__tv_table

    @property
    def add_warehouse_view(self):
        return self.__add_warehouse_view

    @property
    def sensor_detail_view(self):
        return self.__sensor_detail_view

    def refresh(self, values):
        if values and len(values) > 0:
            self.__tv_table.delete(*self.__tv_table.get_children())

            for i in values:
                self.__tv_table.insert('', END, values=values[i], tag=i)
