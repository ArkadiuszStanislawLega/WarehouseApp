import socket
import threading
import json
import pickle
from database import db
from datetime import datetime, date
from Models.models import DigitalReading
import values


class ServerApp:
    # region Constans
    VERSION = 1.0
    HEADER = values.HEADER  # ilosc bajtow ktore beda pobrane
    PORT = values.DEFAULT_PORT
    # pobieram ip localhosta
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDRESS = (SERVER, PORT)
    MESSAGE_START_INFORMATION = "\nMagApp - serwer, wersja: " + str(VERSION) + "\nuwagi i błędy można zgłaszać na arkadiusz.stanislaw.lega@gmail.com\n" + (80*"_") + "\n"
    MESSAGE_CLIENT_DISCONNECTED = " [KLIENT POŁĄCZONY] "
    MESSAGE_NEW_CONNECTION = " [NOWE POŁĄCZENIE] "
    MESSAGE_ACTIVE_CONNECTION = " [POŁĄCZENIE AKTYWNE] "
    MESSAGE_STARTING = " [ROZPOCZYNAM] uruchamianie serwera.."
    MESSAGE_LISTENNING = " [NASŁUCHIWANIE] Serwer nasłuchuje na "
    # endregion Constans

    def __init__(self):
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.bind(self.ADDRESS)
        self.start()

    def __handle_client(self, connection, address):
        self.__print_message(self.MESSAGE_NEW_CONNECTION +
                             str(address) + " connected.")

        connected = True

        while connected:
            if not isinstance(connection, bool):
                msg_length = connection.recv(self.HEADER)
                if msg_length:
                    msg_length = int(len(msg_length))
                    msg = pickle.loads(connection.recv(self.HEADER))
                    if isinstance(msg, DigitalReading):
                        if msg.humidity == 666 and msg.temperature == 666:
                            print(self.MESSAGE_CLIENT_DISCONNECTED + str(address))
                            connection.close()
                            break
                        else:
                            self.__print_message(
                                " [" + str(address) + "] " + str(msg))
                            self.__add_digital_read_to_db(msg)
                else:
                    break
            else:
                connection = False

        connection.close()

    def __add_digital_read_to_db(self, digital_read):
        db.session.add(digital_read)
        db.session.commit()

    def __print_message(self, message):
        time = datetime.now().strftime(values.FORMAT_TIME)
        print(time + message)

    def start(self):
        print(self.MESSAGE_START_INFORMATION)
        self.__print_message(self.MESSAGE_STARTING)
        db.create_all()
        # war = Warehouse()
        # war.name = "Bydgoszcz"
        # sen = Sensor()
        # sen.name = "280-1"
        # sen.warehouse_id = 1
        # db.session.add(war)
        # db.session.add(sen)
        # db.session.commit()

        self.__server.listen()
        self.__print_message(self.MESSAGE_LISTENNING + self.SERVER)
        while True:
            connection, address = self.__server.accept()
            thread = threading.Thread(target=self.__handle_client,
                                      args=(connection, address))
            thread.start()
            self.__print_message(self.MESSAGE_ACTIVE_CONNECTION +
                                 str(threading.active_count()-1))


if __name__ == '__main__':
    ServerApp()
