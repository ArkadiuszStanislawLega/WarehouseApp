from tkinter import Widget, Frame, Scrollbar, RIGHT, LEFT, VERTICAL, BOTH, CENTER, Y, END
from tkinter import ttk


class RightSectionView(Widget):
    STRING_WAREHOUSE = "Magazyn"
    STRING_DEVICE = "Urządzenie"
    STRING_SENSOR = "Czujnik"
    STRING_TEMPERATURE = "Temperatura [°C]"
    STRING_HUMIDITY = "Wilgotność [%]"
    STRING_LAST_READ = "Ostatni odczyt"

    def __init__(self, master=None, cnf={}, **k):
        self.__f_sensors_list = Frame(master)
        self.__f_sensors_list.pack(side=RIGHT, fill=BOTH, expand=True)

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

        self.__tv_table.column(ac[0], width=150, anchor=CENTER)
        self.__tv_table.column(ac[1], width=100, anchor=CENTER)
        self.__tv_table.column(ac[2], width=150, anchor=CENTER)
        self.__tv_table.column(ac[3], width=100, anchor=CENTER)
        self.__tv_table.column(ac[4], width=100, anchor=CENTER)
        self.__tv_table.column(ac[5], width=150, anchor=CENTER)

        for i in range(len(ac)):
            self.__tv_table.heading(ac[i], text=self.__columns[i])

        self.__tv_table.pack(side=LEFT, fill=Y)

        self.__s_vertical_list = Scrollbar(self.__f_sensors_list,
                                           orient=VERTICAL)
        self.__s_vertical_list.pack(side=RIGHT, fill=Y)

    @ property
    def table(self):
        return self.__tv_table

    def refresh(self, values):
        if values and len(values) > 0:
            self.__tv_table.delete(*self.__tv_table.get_children())

            for i in values:
                self.__tv_table.insert('', END, values=values[i], tag=i)
