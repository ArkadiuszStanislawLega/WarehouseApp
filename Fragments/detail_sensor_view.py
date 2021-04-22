from tkinter import LabelFrame, Label, Widget, Button, Frame, W, E, BOTH, YES, NO, LEFT, RIGHT, Entry, END, Checkbutton, BooleanVar

class DetailSensorView (Widget):
    STRING_SENSOR = "Czujnik"
    STRING_SENSOR_ID = "Numer identyfikacyjny czujnika:"
    STRING_SENSOR_NAME = "Nazwa czujnika:"
    STRING_LAST_READ_HUMIDITY = "Ostatni odczyt wilgotności [%]:"
    STRING_LAST_READ_TEMPERATURE = "Ostatni odczyt temperatury [C]:"
    STRING_SENSOR_PORT = "Port na urządzeniu:"
    STRING_LAST_READ_DATE = "Data ostatniego odczytu:"
    STRING_EMPY_PROPERTY = "--"

    def __init__(self, size_width, master=None, cnf={}, **k):
        self.__is_sensor_removing = BooleanVar()
        self.__is_sensor_removing = False

        self.__lf_dg_and_sensor_detail = LabelFrame(master,
                                                    text=self.STRING_SENSOR)
        self.__lf_dg_and_sensor_detail.grid(row=2, column=0)

        self.__l_sensor_id_title = Label(self.__lf_dg_and_sensor_detail,
                                         text=self.STRING_SENSOR_ID)
        self.__l_sensor_id_value = Label(self.__lf_dg_and_sensor_detail,
                                         width=size_width+2)

        self.__cb_sensor_delete = Checkbutton(self.__lf_dg_and_sensor_detail,
                                              offvalue=False,
                                              onvalue=True,
                                              variable=self.__is_sensor_removing)

        self.__l_sensor_name_title = Label(self.__lf_dg_and_sensor_detail,
                                           text=self.STRING_SENSOR_NAME)
        self.__l_sensor_name_value = Label(self.__lf_dg_and_sensor_detail,
                                           width=size_width)
        self.__e_sensor_name_value = Entry(self.__lf_dg_and_sensor_detail,
                                           width=size_width)

        self.__l_sensor_hum_title = Label(self.__lf_dg_and_sensor_detail,
                                          text=self.STRING_LAST_READ_HUMIDITY)
        self.__l_sensor_hum_value = Label(self.__lf_dg_and_sensor_detail,
                                          width=size_width)

        self.__l_sensor_temp_title = Label(self.__lf_dg_and_sensor_detail,
                                           text=self.STRING_LAST_READ_TEMPERATURE)
        self.__l_sensor_temp_value = Label(self.__lf_dg_and_sensor_detail,
                                           width=size_width)

        self.__l_sensor_port_title = Label(self.__lf_dg_and_sensor_detail,
                                           text=self.STRING_SENSOR_PORT)
        self.__l_sensor_port_value = Label(self.__lf_dg_and_sensor_detail,
                                           width=size_width)
        self.__e_sensor_port_value = Entry(self.__lf_dg_and_sensor_detail,
                                           width=size_width)

        self.__l_last_read_title = Label(self.__lf_dg_and_sensor_detail,
                                         text=self.STRING_LAST_READ_DATE)
        self.__l_last_read_value = Label(self.__lf_dg_and_sensor_detail,
                                         width=size_width)

        self.__l_sensor_id_title.grid(row=0, column=0, sticky=W)
        self.__l_sensor_id_value.grid(row=0, column=1, sticky=W)
        self.__cb_sensor_delete.grid(row=0, column=2)

        self.__l_sensor_name_title.grid(row=1, column=0, sticky=W)
        self.__l_sensor_name_value.grid(row=1, column=1, sticky=W)

        self.__l_sensor_hum_title.grid(row=2, column=0, sticky=W)
        self.__l_sensor_hum_value.grid(row=2, column=1, sticky=W)

        self.__l_sensor_temp_title.grid(row=3, column=0, sticky=W)
        self.__l_sensor_temp_value.grid(row=3, column=1, sticky=W)

        self.__l_sensor_port_title.grid(row=4, column=0, sticky=W)
        self.__l_sensor_port_value.grid(row=4, column=1, sticky=W)

        self.__l_last_read_title.grid(row=5, column=0, sticky=W)
        self.__l_last_read_value.grid(row=5, column=1, sticky=W)


    def switch_edit_mode(self, is_edit_mode_on):
        if not is_edit_mode_on:
            self.__l_sensor_name_value.grid_remove()
            self.__e_sensor_name_value.grid(row=1, column=1, sticky=W)

            self.__l_sensor_port_value.grid_remove()
            self.__e_sensor_port_value.grid(row=4, column=1, sticky=W)
        else:
            self.__e_sensor_name_value.grid_remove()
            self.__l_sensor_name_value.grid(row=1, column=1, sticky=W)

            self.__e_sensor_port_value.grid_remove()
            self.__l_sensor_port_value.grid(row=4, column=1, sticky=W)

    def cancel_edit(self):
        sensor_name = str(self.__l_sensor_name_value['text'])
        self.__e_sensor_name_value.delete(0, END)
        self.__e_sensor_name_value.insert(0, sensor_name)

    def set_values(self, sensor, digital_read):
        self.__l_sensor_id_value.config(text=str(sensor.id))
        self.__l_sensor_name_value.config(text=str(sensor.name))

        self.__e_sensor_name_value.delete(0, END)
        self.__e_sensor_name_value.insert(0, str(sensor.name))

        if digital_read.id:
            hum = str(round(digital_read.humidity, 2))
            temp = str(round(digital_read.temperature, 2))
            time = digital_read.time.strftime("%d-%m-%y %H:%M:%S")

            self.__l_sensor_hum_value.config(text=hum)
            self.__l_sensor_temp_value.config(text=temp)
            self.__l_last_read_value.config(text=time)
            # self.__l_sensor_port_value.config(text=str(sensor.port))
            # self.__e_sensor_port_value.set(str(sensor.port))
        else:
            self.__l_sensor_hum_value.config(text=self.STRING_EMPY_PROPERTY)
            self.__l_sensor_temp_value.config(text=self.STRING_EMPY_PROPERTY)
            # self.__l_sensor_port_value.config(text=self.STRING_EMPY_PROPERTY)
            self.__l_last_read_value.config(text=self.STRING_EMPY_PROPERTY)