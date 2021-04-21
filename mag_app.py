from MagApp.controller import MagAppController
from MagApp.model import MagAppModel
from MagApp.view import MagAppView
from mag_app_constans import VERSION


class MagApp:

    def __init__(self):
        self.__model = MagAppModel()
        self.__view = MagAppView()
        self.__controller = MagAppController(model=self.__model,
                                             view=self.__view)


if __name__ == '__main__':
    MagApp()
