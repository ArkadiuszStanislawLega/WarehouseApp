from tkinter import *
from tkinter import ttk

from MagApp.sensor_view import SensorView
from Models.models import Warehouse, Device, Sensor
from datetime import date
from Fragments.sensor_detail_view import SensorDetailView
from Fragments.add_warehouse_view import AddWarehouseView
from Fragments.add_device_view import AddDeviceView
from Fragments.add_sensor_view import AddSensorView
from Fragments.create_graph_view import CreateGraphView
from Fragments.logo_view import LogoView
from Fragments.right_section_view import RightSectionView


class MagAppView:
    # region constans
    SIZE_WINDOW_WIDTH = 1400
    SIZE_WINDOW_HEIGHT = 820
    SIZE_WINDOW = str(SIZE_WINDOW_WIDTH) + "x" + str(SIZE_WINDOW_HEIGHT)
    SIZE_ENTRY_WIDTH = 10
    SIZE_LIST_GRID_WIDTH = 20
    SIZE_LIST_GRID_COLUMN_PADX = 10
    SIZE_LOGO_WIDTH = 250
    SIZE_LOGO_HEIGHT = 150

    STRING_DAY = "Dzień:"
    STRING_MONTH = "Miesiąc:"
    STRING_YEAR = "Rok:"
    STRING_GRAPH_SETTINGS_TITLE = "Wykres czujników:"
    STRING_GRAPH_SELECT_RANGE_DATE = "Wskaż zakres dat:"
    STRING_SETTINGS_FROM = "od"
    STRING_SETTINGS_TO = "do"
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
        self.__f_settings.pack(side=LEFT, fill=BOTH, expand=True)

        self.__c_settings = Canvas(self.__f_settings)
        self.__c_settings.pack(side=LEFT, fill=BOTH, expand=1)

        self.__sb_setting = Scrollbar(self.__f_settings,
                                      orient=VERTICAL,
                                      command=self.__c_settings.yview)
        self.__sb_setting.pack(side=RIGHT, fill=Y)

        self.__c_settings.configure(yscrollcommand=self.__sb_setting.set)
        self.__c_settings.bind('<Configure>', lambda e: self.__c_settings.configure(
            scrollregion=self.__c_settings.bbox(ALL)))

        self.__f_setting_content = Frame(self.__f_settings)
        self.__c_settings.create_window((0, 0),
                                        window=self.__f_setting_content)

        self.__logo_view = LogoView(master=self.__f_setting_content,
                                    file_path=self.__logo_path,
                                    height=self.SIZE_LOGO_HEIGHT,
                                    width=self.SIZE_LOGO_WIDTH)
        self.__sensor_detail_view = SensorDetailView(
            master=self.__f_setting_content)
        self.__add_warehouse_view = AddWarehouseView(self.__f_setting_content)
        self.__add_device_view = AddDeviceView(self.__f_setting_content)
        self.__add_sensor_view = AddSensorView(self.__f_setting_content)
        self.__create_graph_view = CreateGraphView(self.__f_setting_content)
        # endregion LeftSite
        self.__right_section_view = RightSectionView(self.__window)

    def show(self):
        mainloop()

    @property
    def right_section(self):
        return self.__right_section_view

    @property
    def create_graph_view(self):
        return self.__create_graph_view

    @property
    def add_warehouse_view(self):
        return self.__add_warehouse_view

    @property
    def add_device_view(self):
        return self.__add_device_view

    @property
    def add_sensor_view(self):
        return self.__add_sensor_view

    @property
    def sensor_detail_view(self):
        return self.__sensor_detail_view
