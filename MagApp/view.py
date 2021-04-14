from tkinter import *
from tkinter import ttk
from MagApp.sensor_view import SensorView
from Models.models import Warehouse, DigitalReading
from database import db
# from matplotlib.backends.backend_tkagg import (
#     FigureCanvasTkAgg, NavigationToolbar2Tk)
# from matplotlib.figure import Figure
from matplotlib import pyplot as plt


class MagAppView:
    # region constans
    SIZE_WINDOW_WIDTH = 1200
    SIZE_WINDOW_HEIGHT = 800
    SIZE_WINDOW = str(SIZE_WINDOW_WIDTH) + "x" + str(SIZE_WINDOW_HEIGHT)
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
    STRING_WAREHOUSE = "Magazyn"
    STRING_DEVICE = "Urządzenie"
    STRING_SENSOR = "Czujnik"
    STRING_TEMPERATURE = "Temperatura"
    STRING_HUMIDITY = "Wilgotność"
    # endregion constans

    def __init__(self, version):
        self.__window = Tk()
        self.__window.title("MagApp - v" + str(version))
        self.__window.geometry(self.SIZE_WINDOW)

        # region settingGraps

        self.__f_settings = Frame(self.__window)
        self.__f_settings.grid(row=0,
                               column=0,
                               columnspan=7,
                               sticky=W)

        self.__l_title_settings = Label(self.__f_settings,
                                        text=self.STRING_GRAPH_SETTINGS_TITLE)
        self.__l_date_range = Label(self.__f_settings,
                                    text=self.STRING_GRAPH_SELECT_RANGE_DATE)

        self.__l_from = Label(self.__f_settings,
                              text=self.STRING_SETTINGS_FROM)

        self.__l_from_day = Label(self.__f_settings,
                                  text=self.STRING_DAY)

        self.__e_from_day = Entry(self.__f_settings,
                                  width=self.SIZE_ENTRY_WIDTH)

        self.__l_from_month = Label(self.__f_settings,
                                    text=self.STRING_MONTH)

        self.__e_from_month = Entry(self.__f_settings,
                                    width=self.SIZE_ENTRY_WIDTH)

        self.__l_from_year = Label(self.__f_settings,
                                   text=self.STRING_YEAR)

        self.__e_from_year = Entry(self.__f_settings,
                                   width=self.SIZE_ENTRY_WIDTH)

        self.__l_to = Label(self.__f_settings,
                            text=self.STRING_SETTINGS_TO)

        self.__l_to_day = Label(self.__f_settings,
                                text=self.STRING_DAY)

        self.__e_to_day = Entry(self.__f_settings,
                                width=self.SIZE_ENTRY_WIDTH)

        self.__l_to_month = Label(self.__f_settings,
                                  text=self.STRING_MONTH)

        self.__e_to_month = Entry(self.__f_settings,
                                  width=self.SIZE_ENTRY_WIDTH)

        self.__l_to_year = Label(self.__f_settings,
                                 text=self.STRING_YEAR)

        self.__e_to_year = Entry(self.__f_settings,
                                 width=self.SIZE_ENTRY_WIDTH)

        self.__b_confirm = Button(self.__f_settings,
                                  text="Pokaż wykres",
                                  command=self.test_db)

        self.__l_title_settings.grid(row=0, column=0, columnspan=6, sticky=W)
        self.__l_date_range.grid(row=1, column=0, columnspan=6, sticky=W)

        self.__l_from.grid(row=2, column=0, sticky=E)

        self.__l_from_day.grid(row=2, column=1, sticky=W)
        self.__e_from_day.grid(row=2, column=2, sticky=W)

        self.__l_from_month.grid(row=2, column=3, sticky=W)
        self.__e_from_month.grid(row=2, column=4, sticky=W)

        self.__l_from_year.grid(row=2, column=5, sticky=W)
        self.__e_from_year.grid(row=2, column=6, sticky=W)

        self.__l_to.grid(row=3, column=0, sticky=E)

        self.__l_to_day.grid(row=3, column=1, sticky=W)
        self.__e_to_day.grid(row=3, column=2, sticky=W)

        self.__l_to_month.grid(row=3, column=3, sticky=W)
        self.__e_to_month.grid(row=3, column=4, sticky=W)

        self.__l_to_year.grid(row=3, column=5, sticky=W)
        self.__e_to_year.grid(row=3, column=6, sticky=W)

        self.__b_confirm.grid(row=4, column=0)

        # endregion settingGraps
        # region table
        self.__f_sensors_list = Frame(self.__window, bg="black")
        self.__f_sensors_list.grid(row=2,
                                   column=0,
                                   columnspan=5,
                                   rowspan=4,
                                   sticky=W)

        self.__columns = [self.STRING_WAREHOUSE, self.STRING_DEVICE,
                          self.STRING_SENSOR, self.STRING_TEMPERATURE, self.STRING_HUMIDITY]
        ac = ('all', 'n', 'e', 's', 'ne')
        self.__treeview = ttk.Treeview(self.__f_sensors_list,
                                       columns=ac,
                                       show="headings",
                                       height=7)

        self.__treeview.column(ac[0], width=200)
        self.__treeview.column(ac[1], width=200)
        self.__treeview.column(ac[2], width=200)
        self.__treeview.column(ac[3], width=50)
        self.__treeview.column(ac[4], width=50)

        for i in range(len(ac)):
            self.__treeview.heading(ac[i], text=self.__columns[i])

        self.__treeview.grid()
        self.__values = [("Bydgoszcz", "rspi-1", "BME280 - CNU4801/E", 21.23, 50.3),
                         ("Bydgoszcz", "rspi-1", "BME280 - CNU4801/E", 21.23, 50.3),
                         ("Bydgoszcz", "rspi-1", "BME280 - CNU4801/E", 21.23, 50.3),
                         ("Bydgoszcz", "rspi-1", "BME280 - CNU4801/E", 21.23, 50.3),
                         ("Bydgoszcz", "rspi-1", "BME280 - CNU4801/E", 21.23, 50.3),
                         ("Bydgoszcz", "rspi-1", "BME280 - CNU4801/E", 21.23, 50.3), ]
        for i in range(len(self.__values)):
            self.__treeview.insert('', END, values=self.__values[i])
        # endregion table
        mainloop()

    def show(self):
        mainloop()

    @property
    def confirm_button(self):
        return self.__b_confirm

    def test_db(self):
        warehouses = Warehouse.query.all()
        sensors = {
            1: DigitalReading.query.filter(DigitalReading.sensor_id == 1).limit(6).all(),
            2: DigitalReading.query.filter(DigitalReading.sensor_id == 2).limit(6).all(),
            3: DigitalReading.query.filter(DigitalReading.sensor_id == 3).limit(6).all(),
            4: DigitalReading.query.filter(DigitalReading.sensor_id == 4).limit(6).all()
        }

        times = []

        for i in sensors.get(1):
            times.append(i.time)

        temp = {
            1: [],
            2: [],
            3: [],
            4: []
        }

        for i in sensors:
            for x in sensors.get(i):
                temp.get(i).append(x.temperature)

        # fig = Figure(figsize=(1, 1), dpi=100)
        # plot = fig.add_subplot(111)
        plt.plot(times, temp.get(1), label="1")
        plt.plot(times, temp.get(2), label="2")
        plt.plot(times, temp.get(3), label="3")
        plt.plot(times, temp.get(4), label="4")
        plt.legend()
        # plt.ion()
        # plt.xlim(0, 100)
        # plt.ylim(-40, 80)
        plt.show()

        # canvas = FigureCanvasTkAgg(fig, master=self.__window)
        # canvas.draw()
        # fig.canvas.flush_events()
        # canvas.get_tk_widget().grid(row=4,
        #                             column=0, columnspan=6)

        # print(sensors)
        # print(times)
        # print(temp)
