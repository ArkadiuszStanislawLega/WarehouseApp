from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from tkinter import Label, Widget
import matplotlib
matplotlib.use('Agg')


class SensorView(Widget):
    STRING_TEMPERATURE = "Temperatura:"
    STRING_HUMIDITY = "Wilgotność:"
    STRING_READ_UNKNOWN = "---"

    def __init__(self, master=None, row=0, column=0, title="", cnf={}, **k):
        Widget.__init__(self, master, 'label', cnf)
        self.__parent = master
        self.__widget_row = row
        self.__widget_column = column
        self.__l_name = Label(master, text=title, padx=30)

        self.__l_temperature_title = Label(master,
                                           text=self.STRING_TEMPERATURE)
        self.__l_temperature_value = Label(
            master, text=self.STRING_READ_UNKNOWN)

        self.__l_humidity_title = Label(master, text=self.STRING_HUMIDITY)
        self.__l_humidity_value = Label(master, text=self.STRING_READ_UNKNOWN)

        self.__l_name.grid(row=self.__widget_row,
                           column=self.__widget_column, columnspan=2)
        self.__l_temperature_title.grid(
            row=self.__widget_row+1, column=self.__widget_column)
        self.__l_temperature_value.grid(
            row=self.__widget_row+1, column=self.__widget_column + 1)
        self.__l_humidity_title.grid(
            row=self.__widget_row+2, column=self.__widget_column)
        self.__l_humidity_value.grid(
            row=self.__widget_row+2, column=self.__widget_column + 1)
        self.show_graph()

    def show_graph(self, temperature_values=[], humidity_values=[], time_values=[]):
        fig = Figure(figsize=(3, 3), dpi=100)
        plot = fig.add_subplot(111)
        plot.plot(time_values, temperature_values, label="temp")
        plot.plot(time_values, humidity_values, label="wilg")
        plot.legend()
        # plt.ion()
        plt.xlim(0, 100)
        plt.ylim(-10, 100)

        canvas = FigureCanvasTkAgg(fig, master=self.__parent)
        canvas.draw()
        fig.canvas.flush_events()
        canvas.get_tk_widget().grid(row=self.__widget_row+4,
                                    column=self.__widget_column, columnspan=2)

    def update_values(self, title, temperature, humidity):
        self.__l_name.config(text=title)
        self.__l_humidity_value.config(text=str(round(humidity, 2))+"%")
        self.__l_temperature_value.config(text=str(round(temperature, 2))+"C")
