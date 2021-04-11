from tkinter import Checkbutton, Label, Widget
from Models.models import Warehouse


class SensorView(Widget):
    def __init__(self,  sensor, master=None, cnf={}, **k):
        Widget.__init__(self, master, 'label', cnf)
        if master:
            self.__check = Checkbutton(master=master)
            self.__l_warehouse = Label(master=master,
                                       text=sensor.warehouse.name)

            self.__l_device = Label(master=master,
                                    text=master.)
