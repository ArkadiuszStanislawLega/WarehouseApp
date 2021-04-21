from tkinter import *
from tkinter import ttk

from MagApp.sensor_view import SensorView
from Models.models import Warehouse, Device, Sensor
from datetime import date

from Fragments.right_section_view import RightSectionView
from Fragments.left_section_view import LeftSectionView

from mag_app_constans import LOGO_PATH, VERSION, SIZE_WINDOW


class MagAppView:
    # region constans
    SIZE_ENTRY_WIDTH = 10
    SIZE_LIST_GRID_WIDTH = 20
    SIZE_LIST_GRID_COLUMN_PADX = 10

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

    def __init__(self):
        self.__window = Tk()
        self.__window.title("MagApp - v" + str(VERSION))
        self.__window.geometry(SIZE_WINDOW)
        self.__window.iconphoto(False, PhotoImage(file=LOGO_PATH))

        self.__left_section_view = LeftSectionView(self.__window)

        self.__right_section_view = RightSectionView(self.__window)

    def show(self):
        mainloop()

    @property
    def right_section(self):
        return self.__right_section_view

    @property
    def left_section(self):
        return self.__left_section_view
