from tkinter import LabelFrame, Label, Widget, Button, Frame, W, BOTH, YES, LEFT, RIGHT


class SensorDetailView (Widget):
    def __init__(self, master=None, cnf={}, **k):
        self.__lf_sensor_details = LabelFrame(master,
                                              text="Szczegóły czujnika")
        self.__lf_sensor_details.pack(anchor=W, expand=YES, fill=BOTH)
        self.__l_warehouse_id_title = Label(self.__lf_sensor_details,
                                            text="Numer identyfikacyjny magazynu:")
        self.__l_warehouse_id_value = Label(self.__lf_sensor_details,
                                            text="999")
        self.__l_warehouse_id_title.grid(row=0, column=0, sticky=W)
        self.__l_warehouse_id_value.grid(row=0, column=1, sticky=W)

        self.__l_warehouse_name_title = Label(self.__lf_sensor_details,
                                              text="Nazwa magazynu:")
        self.__l_warehouse_name_value = Label(self.__lf_sensor_details,
                                              text="ABCDedfs")
        self.__l_warehouse_name_title.grid(row=1, column=0, sticky=W)
        self.__l_warehouse_name_value.grid(row=1, column=1, sticky=W)

        self.__l_device_id_title = Label(self.__lf_sensor_details,
                                         text="Numer identyfikacyjny urządzenia:")
        self.__l_device_id_value = Label(self.__lf_sensor_details,
                                         text="999")
        self.__l_device_id_title.grid(row=2, column=0, sticky=W)
        self.__l_device_id_value.grid(row=2, column=1, sticky=W)

        self.__l_device_name_title = Label(self.__lf_sensor_details,
                                           text="Nazwa urządzenia:")
        self.__l_device_name_value = Label(self.__lf_sensor_details,
                                           text="ABCDedfs")
        self.__l_device_name_title.grid(row=3, column=0, sticky=W)
        self.__l_device_name_value.grid(row=3, column=1, sticky=W)

        self.__l_sensor_id_title = Label(self.__lf_sensor_details,
                                         text="Numer identyfikacyjny czujnika:")
        self.__l_sensor_id_value = Label(self.__lf_sensor_details,
                                         text="999")
        self.__l_sensor_id_title.grid(row=4, column=0, sticky=W)
        self.__l_sensor_id_value.grid(row=4, column=1, sticky=W)

        self.__l_sensor_name_title = Label(self.__lf_sensor_details,
                                           text="Nazwa czujnika:")
        self.__l_sensor_name_value = Label(self.__lf_sensor_details,
                                           text="ABCDEFG")
        self.__l_sensor_name_title.grid(row=5, column=0, sticky=W)
        self.__l_sensor_name_value.grid(row=5, column=1, sticky=W)

        self.__l_sensor_hum_title = Label(self.__lf_sensor_details,
                                          text="Ostatni odczyt wilgotności [%]:")
        self.__l_sensor_hum_value = Label(self.__lf_sensor_details,
                                          text="90")
        self.__l_sensor_hum_title.grid(row=6, column=0, sticky=W)
        self.__l_sensor_hum_value.grid(row=6, column=1, sticky=W)

        self.__l_sensor_temp_title = Label(self.__lf_sensor_details,
                                           text="Ostatni odczyt temperatury [C]:")
        self.__l_sensor_temp_value = Label(self.__lf_sensor_details,
                                           text="12,3")
        self.__l_sensor_temp_title.grid(row=7, column=0, sticky=W)
        self.__l_sensor_temp_value.grid(row=7, column=1, sticky=W)

        self.__f_sensor_detail_buttons = Frame(self.__lf_sensor_details)
        self.__f_sensor_detail_buttons.grid(row=8, column=0, columnspan=2)

        self.__b_sensor_edit = Button(self.__f_sensor_detail_buttons,
                                      text="Edytuj")

        self.__b_sensor_remove = Button(self.__f_sensor_detail_buttons,
                                        text="Usuń")

        self.__b_sensor_edit.pack(side=LEFT, expand=YES, fill=BOTH)
        self.__b_sensor_remove.pack(side=RIGHT, expand=YES, fill=BOTH)
