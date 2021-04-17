from tkinter import *
from tkinter import ttk
from MagApp.sensor_view import SensorView
from Models.models import Warehouse, DigitalReading, Device, Sensor
from database import db
# from matplotlib.backends.backend_tkagg import (
#     FigureCanvasTkAgg, NavigationToolbar2Tk)
# from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from sqlalchemy import desc


class MagAppView:
    # region constans
    SIZE_WINDOW_WIDTH = 1510
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
    STRING_TEMPERATURE = "Temperatura [°C]"
    STRING_HUMIDITY = "Wilgotność [%]"
    STRING_LAST_READ = "Ostatni odczyt"
    STRING_SENSOR_ID = "Id czujnika"
    STRING_SHOW_GRAPHS = "Pokaż wykres"
    STRING_REFRESH = "Odśwież"
    # endregion constans

    def __init__(self, version):
        self.__window = Tk()
        self.__window.title("MagApp - v" + str(version))
        self.__window.geometry(self.SIZE_WINDOW)

        # region settingGraps
        self.__is_temperature_selected = BooleanVar()
        self.__is_humidity_selected = BooleanVar()

        self.__f_settings = Frame(self.__window)
        self.__f_settings.pack(side=LEFT)

        self.__f_graph_settings = Frame(self.__f_settings)
        self.__f_graph_settings.pack(side=TOP, fill=BOTH)

        self.__l_title_settings = Label(self.__f_graph_settings,
                                        text=self.STRING_GRAPH_SETTINGS_TITLE)
        self.__l_date_range = Label(self.__f_graph_settings,
                                    text=self.STRING_GRAPH_SELECT_RANGE_DATE)

        self.__l_from = Label(self.__f_graph_settings,
                              text=self.STRING_SETTINGS_FROM)

        self.__cb_temperature = Checkbutton(self.__f_graph_settings,
                                            text=self.STRING_TEMPERATURE,
                                            variable=self.__is_temperature_selected,
                                            onvalue=True,
                                            offvalue=False)

        self.__cb_humidity = Checkbutton(self.__f_graph_settings,
                                         text=self.STRING_HUMIDITY,
                                         variable=self.__is_humidity_selected,
                                         onvalue=True,
                                         offvalue=False)

        self.__l_from_day = Label(self.__f_graph_settings,
                                  text=self.STRING_DAY)

        self.__e_from_day = Entry(self.__f_graph_settings,
                                  width=self.SIZE_ENTRY_WIDTH)

        self.__l_from_month = Label(self.__f_graph_settings,
                                    text=self.STRING_MONTH)

        self.__e_from_month = Entry(self.__f_graph_settings,
                                    width=self.SIZE_ENTRY_WIDTH)

        self.__l_from_year = Label(self.__f_graph_settings,
                                   text=self.STRING_YEAR)

        self.__e_from_year = Entry(self.__f_graph_settings,
                                   width=self.SIZE_ENTRY_WIDTH)

        self.__l_to = Label(self.__f_graph_settings,
                            text=self.STRING_SETTINGS_TO)

        self.__l_to_day = Label(self.__f_graph_settings,
                                text=self.STRING_DAY)

        self.__e_to_day = Entry(self.__f_graph_settings,
                                width=self.SIZE_ENTRY_WIDTH)

        self.__l_to_month = Label(self.__f_graph_settings,
                                  text=self.STRING_MONTH)

        self.__e_to_month = Entry(self.__f_graph_settings,
                                  width=self.SIZE_ENTRY_WIDTH)

        self.__l_to_year = Label(self.__f_graph_settings,
                                 text=self.STRING_YEAR)

        self.__e_to_year = Entry(self.__f_graph_settings,
                                 width=self.SIZE_ENTRY_WIDTH)

        self.__b_confirm = Button(self.__f_graph_settings,
                                  text=self.STRING_SHOW_GRAPHS)

        self.__b_refresh_db = Button(self.__f_graph_settings,
                                     text=self.STRING_REFRESH,
                                     command=self.refresh)

        self.__b_get_selected = Button(self.__f_graph_settings,
                                       text="Zaznaczone",
                                       command=self.selected)

        self.__l_title_settings.grid(row=0, column=0, columnspan=6, sticky=W)
        self.__cb_humidity.grid(row=1, column=0)
        self.__cb_temperature.grid(row=1, column=1)
        self.__l_date_range.grid(row=2, column=0, columnspan=6, sticky=W)

        self.__l_from.grid(row=3, column=0, sticky=E)

        self.__l_from_day.grid(row=3, column=1, sticky=W)
        self.__e_from_day.grid(row=3, column=2, sticky=W)

        self.__l_from_month.grid(row=3, column=3, sticky=W)
        self.__e_from_month.grid(row=3, column=4, sticky=W)

        self.__l_from_year.grid(row=3, column=5, sticky=W)
        self.__e_from_year.grid(row=3, column=6, sticky=W)

        self.__l_to.grid(row=4, column=0, sticky=E)

        self.__l_to_day.grid(row=4, column=1, sticky=W)
        self.__e_to_day.grid(row=4, column=2, sticky=W)

        self.__l_to_month.grid(row=4, column=3, sticky=W)
        self.__e_to_month.grid(row=4, column=4, sticky=W)

        self.__l_to_year.grid(row=4, column=5, sticky=W)
        self.__e_to_year.grid(row=4, column=6, sticky=W)

        self.__b_confirm.grid(row=5, column=0)
        self.__b_refresh_db.grid(row=5, column=1)
        self.__b_get_selected.grid(row=5, column=2)

        # endregion settingGraps
        # region table
        self.__f_sensors_list = Frame(self.__window)
        self.__f_sensors_list.pack(side=BOTTOM, fill=BOTH)

        self.__columns = [self.STRING_WAREHOUSE,
                          self.STRING_DEVICE,
                          self.STRING_SENSOR_ID,
                          self.STRING_SENSOR,
                          self.STRING_TEMPERATURE,
                          self.STRING_HUMIDITY,
                          self.STRING_LAST_READ]
        ac = (1, 2, 3, 4, 5, 6, 7)
        self.__values = {}
        self.__tv_table = ttk.Treeview(self.__f_sensors_list,
                                       columns=ac,
                                       show="headings",
                                       height=100)

        self.__tv_table.column(ac[0], width=200, anchor=CENTER)
        self.__tv_table.column(ac[1], width=200, anchor=CENTER)
        self.__tv_table.column(ac[2], width=75, anchor=CENTER)
        self.__tv_table.column(ac[3], width=200, anchor=CENTER)
        self.__tv_table.column(ac[4], width=100, anchor=CENTER)
        self.__tv_table.column(ac[5], width=100, anchor=CENTER)
        self.__tv_table.column(ac[6], width=200, anchor=CENTER)

        for i in range(len(ac)):
            self.__tv_table.heading(ac[i], text=self.__columns[i])

        self.__tv_table.pack(side=LEFT, fill=Y)

        self.__s_vertical_list = Scrollbar(self.__f_sensors_list,
                                           orient=VERTICAL)
        self.__s_vertical_list.pack(side=RIGHT, fill=Y)

        self.refresh()
        # endregion table
        # mainloop()

    def show(self):
        mainloop()

    @property
    def confirm_button(self):
        return self.__b_confirm

    @property
    def is_temperature_selected(self):
        return self.__is_temperature_selected

    @property
    def is_humidity_selected(self):
        return self.__is_humidity_selected

    @property
    def table(self):
        return self.__tv_table

    def refresh(self):
        warehouses = Warehouse.query.all()
        devices = Device.query.all()
        sensors = Sensor.query.all()

        self.__values.clear()
        self.__tv_table.delete(*self.__tv_table.get_children())

        for w in warehouses:
            for d in devices:
                for s in sensors:
                    dr = DigitalReading.query.filter(DigitalReading.sensor_id == s.id).order_by(
                        desc(DigitalReading.id)).limit(1).all()
                    dr = dr[0]
                    time = dr.time.strftime("%d-%m-%y %H:%M:%S")
                    self.__values[s.id] = (w.name,
                                           d.name,
                                           s.id,
                                           s.name,
                                           round(dr.temperature, 2),
                                           round(dr.humidity, 2),
                                           time)

        for i in self.__values:
            self.__tv_table.insert('', END, values=self.__values[i], tag=i)

    def show_graph(self, times, data, labels):
        """
        Rysuje wykres z podanego czasu, 
        słownika z listami danych i słownikami etykiet.

        Args:
            times ([table[datetime]]): Czasy w których zosatły wykonane pomiary
            data ([dict<float>]): Pobrane pomiary
            labels ([dict<string>]): Nazwy etykiet kolorów wykresów
        """
        for i in data:
            plt.plot(times, data.get(i), label=str(labels.get(i)))

        plt.legend()
        plt.show()

    def test_db(self):
        warehouses = Warehouse.query.all()

        times = []
        labels = {}
        temp = {}

        sensors = {
            1: DigitalReading.query.filter(DigitalReading.sensor_id == 1).limit(100).all(),
            2: DigitalReading.query.filter(DigitalReading.sensor_id == 2).limit(100).all(),
            3: DigitalReading.query.filter(DigitalReading.sensor_id == 3).limit(100).all(),
            4: DigitalReading.query.filter(DigitalReading.sensor_id == 4).limit(100).all()
        }

        for i in sensors.get(1):
            times.append(i.time)

        for i in sensors:
            labels[i] = i
            temp[i] = []
            for x in sensors.get(i):
                temp.get(i).append(x.humidity)

        self.show_graph(times=times, data=temp, labels=labels)

        # plt.plot(times, temp.get(1), label="1")
        # plt.plot(times, temp.get(2), label="2")
        # plt.plot(times, temp.get(3), label="3")
        # plt.plot(times, temp.get(4), label="4")
        # plt.legend()

        # plt.show()

        # print(sensors)
        # print(times)
        # print(temp)

    def selected(self):
        curItem = self.__tv_table.focus()
        for i in self.__tv_table.selection():
            # print(self.__treeview.item(i).get('values')[2])
            print(int(self.__tv_table.item(i, 'tag')[0]))
