from tkinter import Widget, Frame, Scrollbar, RIGHT, LEFT, VERTICAL, BOTH, CENTER, Y, END, Canvas, ALL
from tkinter import ttk

from Fragments.sensor_detail_view import SensorDetailView
from Fragments.add_warehouse_view import AddWarehouseView
from Fragments.add_device_view import AddDeviceView
from Fragments.add_sensor_view import AddSensorView
from Fragments.create_graph_view import CreateGraphView
from Fragments.logo_view import LogoView


class LeftSectionView(Widget):
    LOGO_PATH = 'logo.png'
    SIZE_LOGO_WIDTH = 250
    SIZE_LOGO_HEIGHT = 150

    def __init__(self, master=None, cnf={}, **k):
        self.__f_settings = Frame(master)
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
                                    file_path=self.LOGO_PATH,
                                    height=self.SIZE_LOGO_HEIGHT,
                                    width=self.SIZE_LOGO_WIDTH)
        self.__sensor_detail_view = SensorDetailView(
            master=self.__f_setting_content)
        self.__add_warehouse_view = AddWarehouseView(self.__f_setting_content)
        self.__add_device_view = AddDeviceView(self.__f_setting_content)
        self.__add_sensor_view = AddSensorView(self.__f_setting_content)
        self.__create_graph_view = CreateGraphView(self.__f_setting_content)

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
