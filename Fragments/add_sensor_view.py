from tkinter import LabelFrame, Label, Widget, Button, Frame, W, BOTH, YES, LEFT, RIGHT, StringVar, OptionMenu, Entry


class AddSensorView (Widget):
    STRING_ADD_SENSOR = "Dodaj czujnik"
    STRING_SENSOR_NAME = "Nazwa czujnika:"
    STRING_CHOSE_DEVICE = "Wybierz urządzenie:"
    def __init__(self, master=None, cnf={}, **k):
        self.__lf_add_sensor = LabelFrame(master,
                                          text=self.STRING_ADD_SENSOR,
                                          padx=10,
                                          pady=10)
        self.__lf_add_sensor.pack(anchor=W, expand=YES, fill=BOTH)

        self.__l_add_sensor_get_name = Label(self.__lf_add_sensor,
                                             text=self.STRING_SENSOR_NAME)
        self.__l_add_sensor_get_name.grid(row=0, column=0)
        self.__e_add_sensor = Entry(self.__lf_add_sensor)
        self.__e_add_sensor.grid(row=0, column=1)
        self.__l_add_sensor_get_device = Label(self.__lf_add_sensor,
                                               text=self.STRING_ADD_SENSOR)
        self.__l_add_sensor_get_device.grid(row=0, column=2)
        self.__om_select_device = None
        self.__choices_device = []
        self.__devices_dict_id = {}
        self.__selected_device = StringVar(self.__lf_add_sensor)

        self.__b_add_sensor = Button(self.__lf_add_sensor,
                                     text="Dodaj czujnik")
        self.__b_add_sensor.grid(row=1, column=0)

    @property
    def add_button(self):
        return self.__b_add_sensor

    def update_device_list(self, values):
        self.__choices_device.clear()
        for d in values:
            self.__choices_device.append(d.name)
            self.__devices_dict_id[d.id] = d.name

        if len(self.__choices_device) > 0:
            self.__selected_device.set(self.__choices_device[0])

            if self.__om_select_device:
                self.__om_select_device.grid_remove()

            self.__om_select_device = OptionMenu(self.__lf_add_sensor,
                                                 self.__selected_device,
                                                 *self.__choices_device)
            self.__om_select_device.grid(row=0, column=3)

    def selected_id(self):
        for i in self.__devices_dict_id:
            if self.__devices_dict_id[i] == self.__selected_device.get():
                return int(i)

        return None

    def sensor_name(self):
        return self.__e_add_sensor.get()
