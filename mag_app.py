from MagApp.controller import MagAppController
from MagApp.model import MagAppModel
from MagApp.view import MagAppView


class MagApp:

    VERSION = 0.2
    LOGO_PATH = 'logo.png'

    def __init__(self):
        self.__model = MagAppModel()
        self.__view = MagAppView(version=self.VERSION,
                                 path=self.LOGO_PATH)
        self.__controller = MagAppController(model=self.__model,
                                             view=self.__view)


if __name__ == '__main__':
    MagApp()
