from tkinter import (LabelFrame, Label, Widget, Button, Frame, W,
                     BOTH, YES, LEFT, RIGHT, StringVar, BooleanVar,
                     OptionMenu, Entry, Checkbutton, END)
from datetime import date, timedelta, datetime
from matplotlib import pyplot as plt


class CreateGraphView (Widget):
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

    def __init__(self, master=None, cnf={}, **k):
        self.__current_date = date.today()
        self.__month_earlier = self.__current_date - \
            timedelta(self.NUMBER_OF_DAYS_EARLIER)
        self.__is_temperature_selected = BooleanVar()
        self.__is_humidity_selected = BooleanVar()

        self.__f_graph_settings = LabelFrame(master,
                                             text=self.STRING_GRAPH_SETTINGS_TITLE,
                                             padx=10,
                                             pady=10)
        self.__f_graph_settings.pack(anchor=W, expand=YES, fill=BOTH)

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

        self.__cb_humidity.select()

        self.__f_input_from_date = Frame(self.__f_graph_settings)
        self.__l_date_range = Label(self.__f_input_from_date,
                                    text=self.STRING_GRAPH_SELECT_RANGE_DATE)

        self.__l_from = Label(self.__f_input_from_date,
                              text=self.STRING_SETTINGS_FROM)

        self.__l_from_day = Label(self.__f_input_from_date,
                                  text=self.STRING_DAY)

        self.__e_from_day = Entry(self.__f_input_from_date,
                                  width=self.SIZE_ENTRY_WIDTH,
                                  textvariable=StringVar(self.__f_graph_settings,
                                                         value=str(self.__month_earlier.day)))

        self.__l_from_month = Label(self.__f_input_from_date,
                                    text=self.STRING_MONTH)

        self.__e_from_month = Entry(self.__f_input_from_date,
                                    width=self.SIZE_ENTRY_WIDTH,
                                    textvariable=StringVar(self.__f_graph_settings,
                                                           value=str(self.__month_earlier.month)))

        self.__l_from_year = Label(self.__f_input_from_date,
                                   text=self.STRING_YEAR)

        self.__e_from_year = Entry(self.__f_input_from_date,
                                   width=self.SIZE_ENTRY_WIDTH,
                                   textvariable=StringVar(self.__f_graph_settings,
                                                          value=str(self.__month_earlier.year)))

        self.__f_input_to_date = Frame(self.__f_graph_settings)

        self.__l_to = Label(self.__f_input_to_date,
                            text=self.STRING_SETTINGS_TO)

        self.__l_to_day = Label(self.__f_input_to_date,
                                text=self.STRING_DAY)

        self.__e_to_day = Entry(self.__f_input_to_date,
                                width=self.SIZE_ENTRY_WIDTH,
                                textvariable=StringVar(self.__f_graph_settings,
                                                       value=str(self.__current_date.day)))

        self.__l_to_month = Label(self.__f_input_to_date,
                                  text=self.STRING_MONTH)

        self.__e_to_month = Entry(self.__f_input_to_date,
                                  width=self.SIZE_ENTRY_WIDTH,
                                  textvariable=StringVar(self.__f_graph_settings,
                                                         value=str(self.__current_date.month)))

        self.__l_to_year = Label(self.__f_input_to_date,
                                 text=self.STRING_YEAR)

        self.__e_to_year = Entry(self.__f_input_to_date,
                                 width=self.SIZE_ENTRY_WIDTH,
                                 textvariable=StringVar(self.__f_graph_settings,
                                                        value=str(self.__current_date.year)))

        self.__b_confirm = Button(self.__f_graph_settings,
                                  text=self.STRING_SHOW_GRAPHS)

        self.__b_refresh_db = Button(self.__f_graph_settings,
                                     text=self.STRING_REFRESH)

        self.__cb_humidity.grid(row=0, column=0, sticky=W)
        self.__cb_temperature.grid(row=0, column=1, sticky=W)

        self.__f_input_from_date.grid(row=2, column=0)

        self.__l_date_range.pack(anchor=W)
        self.__l_from.pack(side=LEFT, anchor=W)

        self.__l_from_day.pack(side=LEFT, anchor=W)
        self.__e_from_day.pack(side=LEFT, anchor=W)

        self.__l_from_month.pack(side=LEFT, anchor=W)
        self.__e_from_month.pack(side=LEFT, anchor=W)

        self.__l_from_year.pack(side=LEFT, anchor=W)
        self.__e_from_year.pack(side=LEFT, anchor=W)

        self.__f_input_to_date.grid(row=3, column=0)
        self.__l_to.pack(side=LEFT, anchor=W)

        self.__l_to_day.pack(side=LEFT, anchor=W)
        self.__e_to_day.pack(side=LEFT, anchor=W)

        self.__l_to_month.pack(side=LEFT, anchor=W)
        self.__e_to_month.pack(side=LEFT, anchor=W)

        self.__l_to_year.pack(side=LEFT, anchor=W)
        self.__e_to_year.pack(side=LEFT, anchor=W)

        self.__b_confirm.grid(row=5, column=0)
        self.__b_refresh_db.grid(row=5, column=1)

    @ property
    def confirm_button(self):
        return self.__b_confirm

    @ property
    def refresh_db(self):
        return self.__b_refresh_db

    @ property
    def is_temperature_selected(self):
        return self.__is_temperature_selected

    @ property
    def is_humidity_selected(self):
        return self.__is_humidity_selected

    def get_from_date(self):
        try:
            day = int(self.__e_from_day.get())
            month = int(self.__e_from_month.get())
            year = int(self.__e_from_year.get())

            if len(self.__e_from_year.get()) == 4:
                return datetime(year, month, day)

            return None

        except ValueError:
            return None

    def get_to_date(self):
        try:
            day = int(self.__e_to_day.get())
            month = int(self.__e_to_month.get())
            year = int(self.__e_to_year.get())

            if len(self.__e_to_year.get()) == 4:
                return datetime(year, month, day)
        except ValueError:
            return None

    def show_graph(self, times, data, labels):
        """
        Rysuje wykres z podanego czasu,
        słownika z listami danych i słownikami etykiet.

        Args:
            times ([table[datetime]]): Czasy w których zostały wykonane pomiary
            data ([dict<float>]): Pobrane pomiary
            labels ([dict<string>]): Nazwy etykiet kolorów wykresów
        """
        for i in data:
            plt.plot(times, data.get(i), label=str(labels.get(i)))

        plt.legend()
        plt.show()
