from tkinter import Checkbutton, Label, Widget
from Models.models import Warehouse


class SensorView(Widget):
    def __init__(self, warehouse, device, sensor, temperature, humidity, master=None, cnf={}, **k):
        Widget.__init__(self, master, 'label', cnf)
        self.__column_width = 10
        if master:
            self.__check = Checkbutton(master=master,
                                       width=5,
                                       padx=1,
                                       pady=1)

            self.__l_warehouse = Label(master=master,
                                       width=self.__column_width,
                                       text=str(warehouse))

            self.__l_device = Label(master=master,
                                    width=self.__column_width,
                                    text=str(device))
            self.__l_sensor = Label(master=master,
                                    width=self.__column_width,
                                    text=str(sensor))
            self.__l_temperature = Label(master=master,
                                         bg="white",
                                         width=self.__column_width,
                                         text=str(temperature))
            self.__l_humidity = Label(master=master,
                                      bg="white",
                                      width=self.__column_width,
                                      text=str(humidity))

            self.__check.grid(column=0, row=0)
            self.__l_warehouse.grid(column=1, row=0)
            self.__l_device.grid(column=2, row=0)
            self.__l_sensor.grid(column=3, row=0)
            self.__l_temperature.grid(column=4, row=0)
            self.__l_humidity.grid(column=5, row=0)

    def set_device(self, value):
        self.__l_device.config(text=str(value))

    def set_sensor(self, value):
        self.__l_sensor.config(text=str(value))

    def set_temperature(self, value):
        self.__l_temperature.config(text=str(value))

    def set_humidity(self, value):
        self.__l_humidity.config(text=str(value))

    def temperature_warning(self):
        self.__l_temperature.config(bg="red")

    def temperature_normal(self):
        self.__l_temperature.config(bg="white")

    def humidity_warning(self):
        self.__l_humidity.config(bg="red")

    def humidity_normal(self):
        self.__l_humidity.config(bg="white")
