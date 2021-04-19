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
        choices_warehouses = ["Bydgoszcz", "Szczecin", "Poznań"]

        tkvar_warehouses = StringVar(self.__lf_add_device)
        tkvar_warehouses.set("Bydgoszcz")
        self.__l_add_device_select_warehouse = Label(self.__lf_add_device,
                                                     text="Wybierz magazyn:")
        self.__l_add_device_select_warehouse.grid(row=0, column=2)
        self.__om_select_warehouse = OptionMenu(self.__lf_add_device,
                                                tkvar_warehouses,
                                                *choices_warehouses)
        self.__om_select_warehouse.grid(row=0, column=3)
        self.__b_add_device = Button(self.__lf_add_device,
                                     text="Dodaj urządzenie")
        self.__b_add_device.grid(row=1, column=0, columnspan=4)
