from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from MagApp.sensor_view import SensorView
from Models.models import Warehouse, DigitalReading, Device, Sensor
from matplotlib import pyplot as plt
from datetime import date, timedelta, datetime


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

        self.__current_date = date.today()
        self.__month_earlier = self.__current_date - \
            timedelta(self.NUMBER_OF_DAYS_EARLIER)

        # region LeftSite
        self.__f_settings = Frame(self.__window, width=100)
        self.__f_settings.pack(side=LEFT)
        # region Logo
        image = Image.open(self.__logo_path)
        resiz_image = image.resize((self.SIZE_LOGO_WIDTH,
                                    self.SIZE_LOGO_HEIGHT))
        img = ImageTk.PhotoImage(resiz_image)

        self.__l_logo = Label(self.__f_settings,
                              image=img,
                              width=self.SIZE_LOGO_WIDTH,
                              height=self.SIZE_LOGO_HEIGHT)
        self.__l_logo.image = img
        self.__l_logo.pack()
        # endregion Logo
        # region AddWarehouse
        self.__lf_add_warehouse = LabelFrame(self.__f_settings,
                                             text="Dodaj magazyn",
                                             padx=10,
                                             pady=10)
        self.__lf_add_warehouse.pack(anchor=W, expand=YES, fill=BOTH)
        self.__l_add_warehouse_set_name = Label(self.__lf_add_warehouse,
                                                text="Nazwa magazynu:")
        self.__l_add_warehouse_set_name.pack(side=LEFT)
        self.__e_add_warehouse = Entry(self.__lf_add_warehouse)
        self.__e_add_warehouse.pack(side=LEFT)

        self.__b_add_warehouse = Button(self.__lf_add_warehouse,
                                        text="Dodaj magazyn")
        self.__b_add_warehouse.pack(expand=YES, fill=BOTH)
        # endregion AddWarehouse
        # region AddDevice
        self.__lf_add_device = LabelFrame(self.__f_settings,
                                          text="Dodaj urządzenie",
                                          padx=10,
                                          pady=10)
        self.__lf_add_device.pack(anchor=W, expand=YES, fill=BOTH)

        self.__l_add_device_set_name = Label(self.__lf_add_device,
                                             text="Nazwa urządzenia:")
        self.__l_add_device_set_name.grid(row=0, column=0)
        self.__e_add_device = Entry(self.__lf_add_device)
        self.__e_add_device.grid(row=0, column=1)
        choices_warehouses = ["Bydgoszcz", "Szczecin", "Poznań"]

        tkvar_warehouses = StringVar(self.__lf_add_device)
        tkvar_warehouses.set("Bydgoszcz")
        self.__l_add_device_select_warehouse = Label(self.__lf_add_device,
                                                     text="Wybierz magazyn:")
        self.__l_add_device_select_warehouse.grid(row=0, column=2)
        self.__om_select_warehouse = OptionMenu(self.__lf_add_device,
                                                tkvar_warehouses,
                                                *choices_warehouses)
        self.__om_select_warehouse.grid(row=0, column=3)
        self.__b_add_device = Button(self.__lf_add_device,
                                     text="Dodaj urządzenie")
        self.__b_add_device.grid(row=1, column=0, columnspan=4)
        # endregion AddDevice
        # region AddSensor
        self.__lf_add_sensor = LabelFrame(self.__f_settings,
                                          text="Dodaj czujnik",
                                          padx=10,
                                          pady=10)
        self.__lf_add_sensor.pack(anchor=W, expand=YES, fill=BOTH)

        self.__l_add_sensor_get_name = Label(self.__lf_add_sensor,
                                             text="Nazwa czujnika:")
        self.__l_add_sensor_get_name.grid(row=0, column=0)
        self.__e_add_sensor = Entry(self.__lf_add_sensor)
        self.__e_add_sensor.grid(row=0, column=1)
        self.__l_add_sensor_get_device = Label(self.__lf_add_sensor,
                                               text="Wybierz urządzenie:")
        self.__l_add_sensor_get_device.grid(row=0, column=2)
        choices_device = ["rspi-1", "rspi-2", "rspi-3"]

        tkvar_device = StringVar(self.__lf_add_sensor)
        tkvar_device.set("rspi-1")

        self.__om_select_device = OptionMenu(self.__lf_add_sensor,
                                             tkvar_device,
                                             *choices_device)
        self.__om_select_device.grid(row=0, column=3)
        self.__b_add_sensor = Button(self.__lf_add_sensor,
                                     text="Dodaj czujnik")
        self.__b_add_sensor.grid(row=1, column=0, columnspan=4)
        # endregion AddSensor
        # region Graps
        self.__is_temperature_selected = BooleanVar()
        self.__is_humidity_selected = BooleanVar()

        self.__f_graph_settings = LabelFrame(self.__f_settings,
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

        self.__cb_humidity.grid(row=0, column=0)
        self.__cb_temperature.grid(row=0, column=1)

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
        # endregion Graps
        # endregion LeftSite
        # region table
        self.__f_sensors_list = Frame(self.__window)
        self.__f_sensors_list.pack(side=RIGHT)

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

        # endregion table

    def show(self):
        mainloop()

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

    @ property
    def table(self):
        return self.__tv_table

    def refresh(self, values):
        if values and len(values) > 0:
            self.__tv_table.delete(*self.__tv_table.get_children())

            for i in values:
                self.__tv_table.insert('', END, values=values[i], tag=i)

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
