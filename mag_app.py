from MagApp.controller import MagAppController
from MagApp.model import MagAppModel
from MagApp.view import MagAppView


class MagApp:

    VERSION = 0.1

    def __init__(self):
        self.__model = MagAppModel()
        self.__view = MagAppView(version=self.VERSION)
        self.__controller = MagAppController()
        


if __name__ == '__main__':
    MagApp()