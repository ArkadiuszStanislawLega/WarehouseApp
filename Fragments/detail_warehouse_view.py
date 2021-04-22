from tkinter import LabelFrame, Label, Widget, Button, Frame, W, E, BOTH, YES, NO, LEFT, RIGHT, Entry, END, Checkbutton, BooleanVar

class DetailWarehouseView (Widget):
    STRING_WAREHOUSE = "Magazyn"
    STRING_WAREHOUSE_ID = "Numer identyfikacyjny magazynu:"
    STRING_WAREHOUSE_NAME = "Nazwa magazynu:"
    
    def __init__(self, size_width, master=None, cnf={}, **k):
        self.__is_warehouse_removing = BooleanVar()
        self.__is_warehouse_removing = False
        
        self.__lf_warehouse_detail = LabelFrame(master,
                                                text=self.STRING_WAREHOUSE)
        self.__lf_warehouse_detail.grid(row=0, column=0)

        self.__l_warehouse_id_title = Label(self.__lf_warehouse_detail,
                                            text=self.STRING_WAREHOUSE_ID)

        self.__l_warehouse_id_value = Label(self.__lf_warehouse_detail,
                                            width=size_width)
        self.__l_warehouse_id_value.grid(row=0, column=1, sticky=E)

        self.__cb_warehouse_delete = Checkbutton(self.__lf_warehouse_detail,
                                                 offvalue=False,
                                                 onvalue=True,
                                                 variable=self.__is_warehouse_removing)
        self.__cb_warehouse_delete.grid(row=0, column=2)

        self.__l_warehouse_id_title.grid(row=0, column=0, sticky=W)
        self.__cb_warehouse_delete.grid(row=0, column=2, sticky=W)

        self.__l_warehouse_name_title = Label(self.__lf_warehouse_detail,
                                              text=self.STRING_WAREHOUSE_NAME)
        self.__l_warehouse_name_value = Label(self.__lf_warehouse_detail,
                                              width=size_width)
        self.__e_warehouse_name_value = Entry(self.__lf_warehouse_detail,
                                              width=size_width)

        self.__l_warehouse_name_title.grid(row=1, column=0, sticky=W)
        self.__l_warehouse_name_value.grid(row=1, column=1, sticky=W)

    def warehouse_name(self):
        return str(self.__l_warehouse_name_value['text'])


    def switch_edit_mode(self, is_edit_mode_on):
        if not is_edit_mode_on:
            self.__l_warehouse_name_value.grid_remove()
            self.__e_warehouse_name_value.grid(row=1, column=1, sticky=W)
        else:
            self.__e_warehouse_name_value.grid_remove()
            self.__l_warehouse_name_value.grid(row=1, column=1, sticky=W)

    def cancel_edit(self):
        warehouse_name =  str(self.__l_warehouse_name_value['text'])
        self.__e_warehouse_name_value.delete(0, END)
        self.__e_warehouse_name_value.insert(0, warehouse_name)

    def set_values(self, warehouse):
        self.__l_warehouse_id_value.config(text=str(warehouse.id))
        self.__l_warehouse_name_value.config(text=str(warehouse.name))

        self.__e_warehouse_name_value.delete(0, END)
        self.__e_warehouse_name_value.insert(0, str(warehouse.name))