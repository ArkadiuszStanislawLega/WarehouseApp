from tkinter import LabelFrame, Label, Widget, Button, Frame, W, BOTH, YES, LEFT, RIGHT, StringVar, OptionMenu, Entry


class AddSensorView (Widget):
    def __init__(self, master=None, cnf={}, **k):
        self.__lf_add_sensor = LabelFrame(master,
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
