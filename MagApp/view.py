from tkinter import *
from tkinter import ttk

from MagApp.sensor_view import SensorView
from Models.models import Warehouse, Device, Sensor
from datetime import date

from Fragments.right_section_view import RightSectionView
from Fragments.left_section_view import LeftSectionView


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

    def __init__(self, version, path):
        self.__logo_path = path
        self.__window = Tk()
        self.__window.title("MagApp - v" + str(version))
        self.__window.geometry(self.SIZE_WINDOW)
        self.__window.iconphoto(False, PhotoImage(file=self.__logo_path))

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
