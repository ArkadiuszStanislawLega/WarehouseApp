from tkinter import LabelFrame, Label, Widget, Button, Frame, W, BOTH, YES, LEFT, RIGHT, Entry, END


class SensorDetailView (Widget):
    def __init__(self, master=None, cnf={}, **k):
        self.__is_edit_mode_on = False
        self.__lf_sensor_details = LabelFrame(master,
                                              text="Szczegóły czujnika")
        self.__lf_sensor_details.pack(anchor=W, expand=YES, fill=BOTH)
        self.__l_warehouse_id_title = Label(self.__lf_sensor_details,
                                            text="Numer identyfikacyjny magazynu:")
        self.__l_warehouse_id_value = Label(self.__lf_sensor_details,)
        self.__l_warehouse_id_title.grid(row=0, column=0, sticky=W)
        self.__l_warehouse_id_value.grid(row=0, column=1, sticky=W)

        self.__l_warehouse_name_title = Label(self.__lf_sensor_details,
                                              text="Nazwa magazynu:")
        self.__l_warehouse_name_value = Label(self.__lf_sensor_details)
        self.__e_warehouse_name_value = Entry(self.__lf_sensor_details)
        self.__l_warehouse_name_title.grid(row=1, column=0, sticky=W)
        self.__l_warehouse_name_value.grid(row=1, column=1, sticky=W)

        self.__l_device_id_title = Label(self.__lf_sensor_details,
                                         text="Numer identyfikacyjny urządzenia:")
        self.__l_device_id_value = Label(self.__lf_sensor_details)
        self.__l_device_id_title.grid(row=2, column=0, sticky=W)
        self.__l_device_id_value.grid(row=2, column=1, sticky=W)

        self.__l_device_name_title = Label(self.__lf_sensor_details,
                                           text="Nazwa urządzenia:")
        self.__l_device_name_value = Label(self.__lf_sensor_details)
        self.__e_device_name_value = Entry(self.__lf_sensor_details)

        self.__l_device_name_title.grid(row=3, column=0, sticky=W)
        self.__l_device_name_value.grid(row=3, column=1, sticky=W)

        self.__l_sensor_id_title = Label(self.__lf_sensor_details,
                                         text="Numer identyfikacyjny czujnika:")
        self.__l_sensor_id_value = Label(self.__lf_sensor_details)
        self.__l_sensor_id_title.grid(row=4, column=0, sticky=W)
        self.__l_sensor_id_value.grid(row=4, column=1, sticky=W)

        self.__l_sensor_name_title = Label(self.__lf_sensor_details,
                                           text="Nazwa czujnika:")
        self.__l_sensor_name_value = Label(self.__lf_sensor_details)
        self.__e_sensor_name_value = Entry(self.__lf_sensor_details)

        self.__l_sensor_name_title.grid(row=5, column=0, sticky=W)
        self.__l_sensor_name_value.grid(row=5, column=1, sticky=W)

        self.__l_sensor_hum_title = Label(self.__lf_sensor_details,
                                          text="Ostatni odczyt wilgotności [%]:")
        self.__l_sensor_hum_value = Label(self.__lf_sensor_details)
        self.__l_sensor_hum_title.grid(row=6, column=0, sticky=W)
        self.__l_sensor_hum_value.grid(row=6, column=1, sticky=W)

        self.__l_sensor_temp_title = Label(self.__lf_sensor_details,
                                           text="Ostatni odczyt temperatury [C]:")
        self.__l_sensor_temp_value = Label(self.__lf_sensor_details)
        self.__l_sensor_temp_title.grid(row=7, column=0, sticky=W)
        self.__l_sensor_temp_value.grid(row=7, column=1, sticky=W)

        self.__l_sensor_port_title = Label(self.__lf_sensor_details,
                                           text="Port na urządzeniu:")
        self.__l_sensor_port_value = Label(self.__lf_sensor_details)
        self.__e_sensor_port_value = Entry(self.__lf_sensor_details)

        self.__l_sensor_port_title.grid(row=8, column=0, sticky=W)
        self.__l_sensor_port_value.grid(row=8, column=1, sticky=W)

        self.__f_sensor_detail_buttons = Frame(self.__lf_sensor_details)
        self.__f_sensor_detail_buttons.grid(row=9, column=0, columnspan=2)

        self.__b_edit = Button(self.__f_sensor_detail_buttons,
                               text="Edytuj")

        self.__b_cancel = Button(self.__f_sensor_detail_buttons,
                                 text="Anuluj")

        self.__b_confirm = Button(self.__f_sensor_detail_buttons,
                                  text="Zapisz")

        self.__b_remove = Button(self.__f_sensor_detail_buttons,
                                 text="Usuń")

        self.__b_edit.pack(side=LEFT, expand=YES, fill=BOTH)
        self.__b_remove.pack(side=RIGHT, expand=YES, fill=BOTH)

    @property
    def edit_button(self):
        return self.__b_edit

    @property
    def cancel_button(self):
        return self.__b_cancel

    @property
    def confirm_button(self):
        return self.__b_confirm

    @property
    def remove_button(self):
        return self.__b_remove

    @property
    def is_edit_mode_on(self):
        return self.__is_edit_mode_on

    def switch_edit_mode(self):
        if not self.__is_edit_mode_on:
            self.__is_edit_mode_on = True

            self.__l_sensor_port_value.grid_remove()
            self.__l_sensor_name_value.grid_remove()
            self.__l_device_name_value.grid_remove()
            self.__l_warehouse_name_value.grid_remove()
            self.__b_edit.pack_forget()

            self.__e_warehouse_name_value.grid(row=1, column=1, sticky=W)
            self.__e_device_name_value.grid(row=3, column=1, sticky=W)
            self.__e_sensor_name_value.grid(row=5, column=1, sticky=W)
            self.__e_sensor_port_value.grid(row=8, column=1, sticky=W)

            self.__b_confirm.pack(side=LEFT, expand=YES, fill=BOTH)
            self.__b_cancel.pack(side=LEFT, expand=YES, fill=BOTH)

        else:
            self.__is_edit_mode_on = False
            self.__e_warehouse_name_value.grid_remove()
            self.__e_device_name_value.grid_remove()
            self.__e_sensor_name_value.grid_remove()
            self.__e_sensor_port_value.grid_remove()

            self.__b_confirm.pack_forget()
            self.__b_cancel.pack_forget()

            self.__l_warehouse_name_value.grid(row=1, column=1, sticky=W)
            self.__l_device_name_value.grid(row=3, column=1, sticky=W)
            self.__l_sensor_name_value.grid(row=5, column=1, sticky=W)
            self.__l_sensor_port_value.grid(row=8, column=1, sticky=W)
            self.__b_edit.pack(side=LEFT, expand=YES, fill=BOTH)

    def cancel_edit(self):
        self.__e_warehouse_name_value.delete(0, END)
        self.__e_warehouse_name_value.insert(
            0, str(self.__l_warehouse_name_value['text']))

        self.__e_device_name_value.delete(0, END)
        self.__e_device_name_value.insert(
            0, str(self.__l_device_name_value['text']))

        self.__e_sensor_name_value.delete(0, END)
        self.__e_sensor_name_value.insert(
            0, str(self.__l_sensor_name_value['text']))

    def set_sensor(self, warehouse, device, sensor, digital_read):
        self.__l_warehouse_id_value.config(text=str(warehouse.id))
        self.__l_warehouse_name_value.config(text=str(warehouse.name))
        self.__e_warehouse_name_value.delete(0, END)
        self.__e_warehouse_name_value.insert(0, str(warehouse.name))

        self.__l_device_id_value.config(text=str(device.id))
        self.__l_device_name_value.config(text=str(device.name))
        self.__e_device_name_value.delete(0, END)
        self.__e_device_name_value.insert(0, str(device.name))

        self.__l_sensor_id_value.config(text=str(sensor.id))
        self.__l_sensor_name_value.config(text=str(sensor.name))
        self.__e_sensor_name_value.delete(0, END)
        self.__e_sensor_name_value.insert(0, str(sensor.name))
        self.__l_sensor_hum_value.config(
            text=str(round(digital_read.humidity, 2)))
        self.__l_sensor_temp_value.config(
            text=str(round(digital_read.temperature, 2)))

        # self.__l_sensor_port_value.config(text=str(sensor.port))
        # self.__e_sensor_port_value.set(str(sensor.port))
