from tkinter import LabelFrame, Label, Widget, Button, Frame, W, E, BOTH, YES, NO, LEFT, RIGHT, Entry, END, Checkbutton, BooleanVar
from Fragments.detail_warehouse_view import DetailWarehouseView
from Fragments.detail_device_view import DetailDeviceView
from Fragments.detail_sensor_view import DetailSensorView

class SensorDetailView (Widget):
    STRING_EMPY_PROPERTY = "--"
    STRING_TITLE = "Szczegóły czujnika"
    STRING_CONFIRM = "Zapisz"
    STRING_EDIT = "Edytuj"
    STRING_REMOVE = "Usuń"
    STRING_CANCEL = "Anuluj"

    SIZE_WIDTH_CENTER_GRID = 36

    def __init__(self, master=None, cnf={}, **k):
        self.__is_edit_mode_on = False
        self.__lf_sensor_details = LabelFrame(master,
                                              text=self.STRING_TITLE)
        self.__lf_sensor_details.pack(anchor=W, expand=YES, fill=BOTH)

        self.__detail_warehouse_view = DetailWarehouseView(master=self.__lf_sensor_details, 
                                                           size_width=self.SIZE_WIDTH_CENTER_GRID)
        self.__detial_device_view = DetailDeviceView(master=self.__lf_sensor_details,
                                                     size_width=self.SIZE_WIDTH_CENTER_GRID)
        self.__detail_sensor_view = DetailSensorView(master=self.__lf_sensor_details,
                                                     size_width=self.SIZE_WIDTH_CENTER_GRID)
        # region Buttons
        self.__f_sensor_detail_buttons = Frame(self.__lf_sensor_details)
        self.__f_sensor_detail_buttons.grid(row=3, column=0)
        
        self.__b_edit = Button(self.__f_sensor_detail_buttons,
                               text=self.STRING_EDIT)

        self.__b_cancel = Button(self.__f_sensor_detail_buttons,
                                 text=self.STRING_CANCEL)

        self.__b_confirm = Button(self.__f_sensor_detail_buttons,
                                  text=self.STRING_CONFIRM)

        self.__b_remove = Button(self.__f_sensor_detail_buttons,
                                 text=self.STRING_REMOVE)

        self.__b_edit.pack(side=LEFT)
        self.__b_remove.pack(side=RIGHT)
        # endregion Buttons

    @property
    def is_warehouse_removing(self):
        return self.__is_warehouse_removing

    @property
    def is_device_removing(self):
        return self.__is_device_removing

    @property
    def is_sensor_removing(self):
        return self.__is_sensor_removing

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
        self.__detail_warehouse_view.switch_edit_mode(self.__is_edit_mode_on)
        self.__detial_device_view.switch_edit_mode(self.__is_edit_mode_on)
        self.__detail_sensor_view.switch_edit_mode(self.__is_edit_mode_on)

        if not self.__is_edit_mode_on:
            self.__b_edit.pack_forget()
            self.__b_confirm.pack(side=LEFT)
            self.__b_cancel.pack(side=RIGHT)

            self.__is_edit_mode_on = True

        else:
            self.__b_confirm.pack_forget()
            self.__b_cancel.pack_forget()
            self.__b_edit.pack(side=LEFT)

            self.__is_edit_mode_on = False

    def cancel_edit(self):
        self.__detail_warehouse_view.cancel_edit()
        self.__detial_device_view.cancel_edit()
        self.__detail_sensor_view.cancel_edit()

    def set_sensor(self, warehouse, device, sensor, digital_read):
        self.__detail_warehouse_view.set_values(warehouse)
        self.__detial_device_view.set_values(device)
        self.__detail_sensor_view.set_values(sensor, digital_read)



