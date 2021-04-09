"""2021 - Autor: Arkadiusz Łęga, email:horemheb@vp.pl
Klasa - odpowiada za reakcje na przyciski w GUI"""


class ClientAppController:
    """
    Odpowiada za reakcje na przyciski w GUI aplikacji.
    """

    def __init__(self, model, view, parent):
        self.__model = model
        self.__view = view
        self.__parent = parent

    def disconnect(self):
        """
        Przełącza status przycisków w GUI i
        rozłącza clienta z serwerem.
        """
        self.__view.disableOrEnableFields()
        self.__model.disconnect()

    def connect(self):
        """
        Pobiera wartości z GUI - sprawdza czy są poprawne,
        przełącza status przycisków oraz pól do wpisywania,
        a następnie łączy z serwerem.
        """
        if self.__parent.collect_settings_from_GUI() and self.__model.getSettingsFromGUI():
            self.__view.disableOrEnableFields()
            self.__model.connect()

    def exit(self):
        """
        Wykonuje wszystkie czynności do poprawnego zamknięcia aplikacji.
        Rozłącza się z serverem. Przełącza flagi wskazujące na zaknięcie wątków.
        Wyłącza aplikacje.
        """
        self.__model.disconnect()
        self.__model.is_readings_taken = False
        self.__parent.is_loop_working = False
        self.__view.window.destroy()
