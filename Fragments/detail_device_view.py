from tkinter import LabelFrame, Label, Widget, Button, Frame, W, E, BOTH, YES, NO, LEFT, RIGHT, Entry, END, Checkbutton, BooleanVar

class DetailDeviceView (Widget):
    STRING_DEVICE = "Urządzenie"
    STRING_DEVICE_ID = "Numer identyfikacyjny urządzenia:"
    STRING_DEVICE_NAME = "Nazwa urządzenia:"

    def __init__(self, size_width, master=None, cnf={}, **k):
        self.__is_device_removing = BooleanVar()
        self.__is_device_removing = False

        self.__lf_device_detail = LabelFrame(master,
                                             text=self.STRING_DEVICE)
        self.__lf_device_detail.grid(row=1, column=0)

        self.__l_device_id_title = Label(self.__lf_device_detail,
                                         text=self.STRING_DEVICE_ID)
        self.__l_device_id_value = Label(self.__lf_device_detail,
                                         width=size_width)

        self.__cb_device_delete = Checkbutton(self.__lf_device_detail,
                                              variable=self.__is_device_removing)
                                              
        self.__l_device_name_title = Label(self.__lf_device_detail,
                                           text=self.STRING_DEVICE_NAME)
        self.__l_device_name_value = Label(self.__lf_device_detail,
                                           width=size_width)
        self.__e_device_name_value = Entry(self.__lf_device_detail,
                                           width=size_width)

        self.__l_device_id_title.grid(row=0, column=0, sticky=W)
        self.__l_device_id_value.grid(row=0, column=1, sticky=W)
        self.__cb_device_delete.grid(row=0, column=2)
        self.__l_device_name_title.grid(row=1, column=0, sticky=W)
        self.__l_device_name_value.grid(row=1, column=1, sticky=W)

    def switch_edit_mode(self, is_edit_mode_on):
        if not is_edit_mode_on:
            self.__l_device_name_value.grid_remove()
            self.__e_device_name_value.grid(row=1, column=1, sticky=W)
        else:
            self.__e_device_name_value.grid_remove()
            self.__l_device_name_value.grid(row=1, column=1, sticky=W)
    
    def cancel_edit(self):
        device_name = str(self.__l_device_name_value['text'])
        self.__e_device_name_value.delete(0, END)
        self.__e_device_name_value.insert(0, device_name)

    def set_values(self, device):
        self.__l_device_id_value.config(text=str(device.id))
        self.__l_device_name_value.config(text=str(device.name))

        self.__e_device_name_value.delete(0, END)
        self.__e_device_name_value.insert(0, str(device.name))