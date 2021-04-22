from tkinter import LabelFrame, Label, Widget, Button, BOTH, YES, LEFT, Entry, W


class AddWarehouseView (Widget):
    STRING_ADD_WAREHOUSE = "Dodaj magazyn"
    STRING_WAREHOUSE_NAME = "Nazwa magazynu:"

    def __init__(self, master=None, cnf={}, **k):
        self.__lf_add_warehouse = LabelFrame(master,
                                             text=self.STRING_ADD_WAREHOUSE,
                                             padx=10,
                                             pady=10)
        self.__lf_add_warehouse.pack(anchor=W, expand=YES, fill=BOTH)
        self.__l_add_warehouse_set_name = Label(self.__lf_add_warehouse,
                                                text=self.STRING_WAREHOUSE_NAME)
        self.__l_add_warehouse_set_name.pack(side=LEFT)
        self.__e_add_warehouse = Entry(self.__lf_add_warehouse)
        self.__e_add_warehouse.pack(side=LEFT)

        self.__b_add_warehouse = Button(self.__lf_add_warehouse,
                                        text=self.STRING_ADD_WAREHOUSE)
        self.__b_add_warehouse.pack(expand=YES, fill=BOTH)

    @property
    def add_button(self):
        return self.__b_add_warehouse

    @property
    def entry_value(self):
        return self.__e_add_warehouse.get()
