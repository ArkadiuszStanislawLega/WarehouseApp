from tkinter import *


class MagAppView:
    SIZE_WINDOW_WIDTH = 1200
    SIZE_WINDOW_HEIGHT = 800
    SIZE_WINDOW = str(SIZE_WINDOW_WIDTH) + "x" + str(SIZE_WINDOW_HEIGHT)
    SIZE_ENTRY_WIDTH = 10

    STRING_DAY = "Dzień:"
    STRING_MONTH = "Miesiąc:"
    STRING_YEAR = "Rok:"
    STRING_GRAPH_SETTINGS_TITLE = "Wykres czujników:"
    STRING_GRAPH_SELECT_RANGE_DATE = "Wskaż zakres dat:"
    STRING_SETTINGS_FROM = "od"
    STRING_SETTINGS_TO = "do"

    def __init__(self, version):
        self.__window = Tk()
        self.__window.title("MagApp - v" + str(version))
        self.__window.geometry(self.SIZE_WINDOW)

        # region settingGraps
        self.__f_settings = Frame(self.__window, bg="red")
        self.__f_settings.grid(row=0,
                               column=0,
                               columnspan=7,
                               sticky=W)

        self.__l_title_settings = Label(self.__f_settings,
                                        text=self.STRING_GRAPH_SETTINGS_TITLE)
        self.__l_date_range = Label(self.__f_settings,
                                    text=self.STRING_GRAPH_SELECT_RANGE_DATE)

        self.__l_from = Label(self.__f_settings,
                              text=self.STRING_SETTINGS_FROM)

        self.__l_from_day = Label(self.__f_settings,
                                  text=self.STRING_DAY)

        self.__e_from_day = Entry(self.__f_settings,
                                  width=self.SIZE_ENTRY_WIDTH)

        self.__l_from_month = Label(self.__f_settings,
                                    text=self.STRING_MONTH)

        self.__e_from_month = Entry(self.__f_settings,
                                    width=self.SIZE_ENTRY_WIDTH)

        self.__l_from_year = Label(self.__f_settings,
                                   text=self.STRING_YEAR)

        self.__e_from_year = Entry(self.__f_settings,
                                   width=self.SIZE_ENTRY_WIDTH)

        self.__l_to = Label(self.__f_settings,
                            text=self.STRING_SETTINGS_TO)

        self.__l_to_day = Label(self.__f_settings,
                                text=self.STRING_DAY)

        self.__e_to_day = Entry(self.__f_settings,
                                width=self.SIZE_ENTRY_WIDTH)

        self.__l_to_month = Label(self.__f_settings,
                                  text=self.STRING_MONTH)

        self.__e_to_month = Entry(self.__f_settings,
                                  width=self.SIZE_ENTRY_WIDTH)

        self.__l_to_year = Label(self.__f_settings,
                                 text=self.STRING_YEAR)

        self.__e_to_year = Entry(self.__f_settings,
                                 width=self.SIZE_ENTRY_WIDTH)

        self.__b_confirm = Button(self.__f_settings,
                                  text="Pokaż wykres")

        self.__l_title_settings.grid(row=0, column=0, columnspan=6, sticky=W)
        self.__l_date_range.grid(row=1, column=0, columnspan=6, sticky=W)

        self.__l_from.grid(row=2, column=0, sticky=E)

        self.__l_from_day.grid(row=2, column=1, sticky=W)
        self.__e_from_day.grid(row=2, column=2, sticky=W)

        self.__l_from_month.grid(row=2, column=3, sticky=W)
        self.__e_from_month.grid(row=2, column=4, sticky=W)

        self.__l_from_year.grid(row=2, column=5, sticky=W)
        self.__e_from_year.grid(row=2, column=6, sticky=W)

        self.__l_to.grid(row=3, column=0, sticky=E)

        self.__l_to_day.grid(row=3, column=1, sticky=W)
        self.__e_to_day.grid(row=3, column=2, sticky=W)

        self.__l_to_month.grid(row=3, column=3, sticky=W)
        self.__e_to_month.grid(row=3, column=4, sticky=W)

        self.__l_to_year.grid(row=3, column=5, sticky=W)
        self.__e_to_year.grid(row=3, column=6, sticky=W)

        self.__b_confirm.grid(row=4, column=0)

        # endregion settingGraps
        mainloop()

    def show(self):
        mainloop()

    @property
    def confirm_button(self):
        return self.__b_confirm
