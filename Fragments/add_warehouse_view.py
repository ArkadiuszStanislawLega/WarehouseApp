from tkinter import LabelFrame, Label, Widget, Button, BOTH, YES, LEFT, Entry, W


class AddWarehouseView (Widget):
    def __init__(self, master=None, cnf={}, **k):
        self.__lf_add_warehouse = LabelFrame(master,
                                             text="Dodaj magazyn",
                                             padx=10,
                                             pady=10)
        self.__lf_add_warehouse.pack(anchor=W, expand=YES, fill=BOTH)
        self.__l_add_warehouse_set_name = Label(self.__lf_add_warehouse,
                                                text="Nazwa magazynu:")
        self.__l_add_warehouse_set_name.pack(side=LEFT)
        self.__e_add_warehouse = Entry(self.__lf_add_warehouse)
        self.__e_add_warehouse.pack(side=LEFT)

        self.__b_add_warehouse = Button(self.__lf_add_warehouse,
                                        text="Dodaj magazyn")
        self.__b_add_warehouse.pack(expand=YES, fill=BOTH)
