from Models.models import Warehouse


class MagAppModel:
    def __init__(self):
        self.__warehouse = Warehouse()
        self.__warehouse.id = 1
        self.__warehouse.name = "elo"
        print(self.__warehouse)
