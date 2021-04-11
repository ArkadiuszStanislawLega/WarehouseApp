from MagApp.controller import MagAppController
from MagApp.model import MagAppModel
from MagApp.view import MagAppView


class MagApp:
    def __init__(self):
        self.__model = MagAppModel()
        self.__view = MagAppView()
        self.__controller = MagAppController()
        print("done")


if __name__ == '__main__':
    MagApp()
