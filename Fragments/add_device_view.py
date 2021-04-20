from tkinter import LabelFrame, Label, Widget, Button, Frame, W, BOTH, YES, LEFT, RIGHT, Entry, OptionMenu, StringVar


class AddDeviceView (Widget):
    def __init__(self, master=None, cnf={}, **k):
        self.__lf_add_device = LabelFrame(master,
                                          text="Dodaj urządzenie",
                                          padx=10,
                                          pady=10)
        self.__lf_add_device.pack(anchor=W, expand=YES, fill=BOTH)

        self.__l_add_device_set_name = Label(self.__lf_add_device,
                                             text="Nazwa urządzenia:")
        self.__l_add_device_set_name.grid(row=0, column=0)
        self.__e_add_device = Entry(self.__lf_add_device)
        self.__e_add_device.grid(row=0, column=1)
        self.__choices_warehouses = []
        self.__warehouses_dict_id = {}
        self.__selcted_warehouse = StringVar(self.__lf_add_device)
        self.__om_select_warehouse = None

        self.__l_add_device_select_warehouse = Label(self.__lf_add_device,
                                                     text="Wybierz magazyn:")
        self.__l_add_device_select_warehouse.grid(row=0, column=2)

        self.__b_add_device = Button(self.__lf_add_device,
                                     text="Dodaj urządzenie")
        self.__b_add_device.grid(row=1, column=0)

    @property
    def warehouses_list(self):
        return self.__choices_warehouses

    @warehouses_list.setter
    def warehouses_list(self, value):
        self.__choices_warehouses = value

    @property
    def add_button(self):
        return self.__b_add_device

    def update_warehouses_list(self, values):
        self.__choices_warehouses.clear()
        for w in values:
            self.__choices_warehouses.append(w.name)
            self.__warehouses_dict_id[w.id] = w.name

        if len(self.__choices_warehouses) > 0:
            self.__selcted_warehouse.set(self.__choices_warehouses[0])

            if self.__om_select_warehouse:
                self.__om_select_warehouse.grid_remove()

            self.__om_select_warehouse = OptionMenu(self.__lf_add_device,
                                                    self.__selcted_warehouse,
                                                    *self.__choices_warehouses)
            self.__om_select_warehouse.grid(row=0, column=3)

    def selected_id(self):
        for i in self.__warehouses_dict_id:
            if self.__warehouses_dict_id[i] == self.__selcted_warehouse.get():
                return i

        return None

    def device_name(self):
        return self.__e_add_device.get()
