"""2021 - Autor: Arkadiusz Łęga, email:horemheb@vp.pl"""

import socket
import pickle
import random
import time
from datetime import datetime, date
from models import DigitalReading
from data_reciver import DataReceiver
import strings
import values


class ClientAppModel:
    """
    Model aplikacji odpowiada za łączenie się z serwerem,
    wysyłanie odczytów z czujników.
    """

    def __init__(self, view, ip, port):
        """
        Ustawia podstawowe wartości działania aplikacji.

        Args:
            view ([ClientAppView]): Widok aplikacji
            ip ([str]): Ip serwera
            port ([int]): Port serwera
        """
        self.__view = view
        self.__is_sending_running = False
        self.__is_readings_taken = True
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__data_reciver = DataReceiver()
        self.__counter = 0

        self.__server_ip = str(ip)
        self.__server_port = int(port)

        self.__limit_collecting_sensor_data = values.DEFAULT_LIMIT_COLLECTING_DATA_TO_GRAPH

        self.__time_next_message_send = 0

        self.__server_address = (self.__server_ip, self.__server_port)
        self.__time_values = []
        self.__temperature_values = {
            0: [],
            1: [],
            2: [],
            3: []
        }
        self.__humidity_values = {
            0: [],
            1: [],
            2: [],
            3: []
        }
    # region properties

    @property
    def view(self):
        """
        Widok aplikacji.

        Returns:
            [ClientAppView]: Widok aplikacji tkinter.
        """
        return self.__view

    @property
    def server_ip(self):
        """
        Adres ip serwera

        Returns:
            [str]: Adres ip serwera.
        """
        return self.__server_ip

    @server_ip.setter
    def server_ip(self, value):
        """
        Adres ip serwera

        Args:
            value ([str]): Adres ip serwera
        """
        self.__server_ip = str(value)

    @property
    def server_port(self):
        """
        Numer portu serwera na którym nasłuchuje.

        Returns:
            [int]: Numer portu
        """
        return self.__server_port

    @server_port.setter
    def server_port(self, value):
        """
        Numer portu serwera na którym nasłuchuje.

        Args:
            value ([int]): Numer portu
        """
        self.__server_port = int(value)

    @property
    def server_address(self):
        """
        Pełen adres serwera ip + port.

        Returns:
            [tuple]: Pełen adres serwera.
        """
        return self.__server_address

    @property
    def time_values(self):
        """
        Tablica z czasami w których jest pobierany odczt,
        używany do rysowania wykresów.

        Returns:
            [table]: Tablica z czasami pobieranych odczytów.
        """
        return self.__time_values

    @property
    def temperature_values(self):
        """
        Tablica z wynikami pobranych odczytów temperatur,
        używany do rysowania wykresów.

        Returns:
            [table]: Tablica z tempareaturami pobieranych z czujnika.
        """
        return self.__temperature_values

    @property
    def humidity_values(self):
        """
        Tablica z wynikami pobranych odczytów wilgotności,
        używanych do rysowania wykresów.

        Returns:
            [table]: Tablica z parematrami wilgotności pobieranych z czujnika.
        """
        return self.__humidity_values

    @property
    def is_sending_running(self):
        """
        Flaga wskazująca czy wysyałane są wiadomości.

        Returns:
            [boolean]: Wskazuje czy wiadomości są wysyłane na serwer.
        """
        return self.__is_sending_running

    @property
    def is_readings_taken(self):
        """
        Flaga wskazująca czy są pobierane parametry z czujników.

        Returns:
            [boolean]: Wskazuje czy są pobierane odczyty.
        """
        return self.__is_readings_taken

    @is_readings_taken.setter
    def is_readings_taken(self, value):
        self.__is_sending_running = value

    # endregion properties

    def __time_and_message(self, message):
        current_time = datetime.now().strftime(values.FORMAT_TIME)
        return current_time + message

    def __send(self, digital_read):
        if self.__is_sending_running:
            if digital_read:
                is_temperture_exit_code = digital_read.temperature == values.EXIT_CODE
                is_himidity_exit_code = digital_read.humidity == values.EXIT_CODE
                if is_temperture_exit_code and is_himidity_exit_code:
                    self.__add_to_console(strings.STRING_DISCONNECT)
                else:
                    dr_str = str(digital_read)
                    sending_str = strings.STRING_SENDING_MESSAGE
                    self.__add_to_console(sending_str+dr_str)

                message = pickle.dumps(digital_read)

                send_length = b' ' * values.HEADER

                # self.__debug_mode(message, send_length)

                try:
                    self.__client.send(send_length)
                    self.__client.send(message)
                    self.__add_to_console(strings.STRING_SENT_MESSAGE)
                except socket.error:
                    self.__add_to_console(strings.STRING_SENDING_ERROR)

                    self.__is_sending_running = False
                    self.__client = socket.socket()
                    while not self.__is_sending_running:
                        try:
                            self.__add_to_console(
                                strings.STRING_ATTEMPT_RECONNECT)

                            self.__client.connect(self.__server_address)
                            self.__is_sending_running = True

                            self.__add_to_console(
                                strings.STRING_SUCCESSFUL_RECCONECT)
                        except socket.error:
                            time.sleep(2)

            else:
                self.__view.add_to_console(
                    strings.STRING_SENSOR_IS_NOT_CONNECTED)

    def __add_to_console(self, message, show_time=True):
        if show_time:
            time_and_message = self.__time_and_message(message)
            self.__view.add_to_console(time_and_message)
        else:
            self.__view.add_to_console(message)

    def get_settings_from_GUI(self):
        """
        Pobiera parametry wpisane w widoku.
        Sprawdza czy wartości są poprawne.

        Returns:
            [boolean]: Jeżeli wartości są poprawne to True
        """
        try:
            self.__server_ip = self.__view.get_address()
            self.__server_port = int(self.__view.get_port())
            self.__server_address = (self.__server_ip, self.__server_port)
            self.__limit_collecting_sensor_data = int(
                self.__view.get_limit_collecting_data())
            self.__view.add_to_console(strings.STRING_VALUE_ERROR_MESSAGE)
            return True
        except:
            return False

    def send_data_from_sensors(self):
        """
        Inicializuje zebranie wartości z czujników i wysłanie na serwer.
        """
        for i in range(values.NUMBER_OF_SENSORS):
            self.__send(self.__get_data_recive(i))

    def __debug_mode(self, message, send_length):
        msg_length = len(message)

        print("Długość wiadomości:", msg_length)
        print("Wiadomość:", message)

        print("Wysyłanie - długość wiadomości:",
              self.__client.send(send_length))
        print("Wysyłanie - wiadomość:", self.__client.send(message))

    def __get_data_recive(self, sensor_id):
        self.__data_reciver.change_channel(sensor_id)
        return self.__data_reciver.get_sensor_data(sensor_id)

    def __fake_data(self):
        dr1 = DigitalReading()
        dr1.temperature = random.uniform(-40, 80)
        dr1.humidity = random.uniform(0, 100)
        dr1.sensor_id = 1

        current_time = datetime.now()
        dr1.time = current_time
        dr1.date = date.today()
        return dr1

    def collect_data_from_sensors(self):
        """
        Zbiera dane z czujników i zapisuje do tablic, z których
        tworzone są wykresy.
        """
        size_time_values = len(self.__time_values) 
        if size_time_values >= 0 and size_time_values < self.__limit_collecting_sensor_data :
            self.__save_values_for_graphs()
        else:
            self.__save_values_for_graphs(is_poped=True)

    def __save_values_for_graphs(self, is_poped=False):
        self.__save_arg_in_table(value=datetime.now(), table=self.__time_values, is_poped=True)
        for i in range(values.NUMBER_OF_SENSORS):
            digital_read = self.__get_data_recive(i)

            if digital_read:
                self.__view.update_sensor_view(i, digital_read)
                digital_read.id = i

                table_hum = self.__humidity_values.get(i)
                table_temp = self.__temperature_values.get(i)

                self.__save_arg_in_table(value=digital_read.humidity,table=table_hum, is_poped=True)
                self.__save_arg_in_table(value=digital_read.temperature, table=table_temp, is_poped=True)

        
    def __save_arg_in_table(self, value, table, is_poped=False):
        try:
            if is_poped:
                table.pop(0)

            table.append(value)
        except IndexError:
            for i in range(len(table)-1):
                    print(i, " ", table)

    # def __save_temp_to_table(self, id, digital_read, is_poped=False):
    #     temp_table = self.__temperature_values.get(id)
    #     if is_poped:
    #         temp_table.pop(0)

    #     temp_table.append(digital_read.temperature)

    # def __save_hum_to_table(self, id, digital_read, is_poped=False):
    #     hum_table = self.__humidity_values.get(id)
    #     if is_poped:
    #         hum_table.pop(0)

    #     hum_table.append(digital_read.humidity)

    def connect(self):
        """
        Łączy klienta z serwerem.
        """
        if not self.__is_sending_running:
            ip_str = str(self.__server_ip)
            port_str = str(self.__server_port)
            message = strings.STRING_CONNECTING + ip_str + ":" + port_str + " ..."
            self.__add_to_console(message)
            self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__client.connect(self.__server_address)
            self.__is_sending_running = True

    def disconnect(self):
        """
        Rozłącza klienta z serwerem.
        """
        if self.__is_sending_running:
            disconnect_read = DigitalReading()
            disconnect_read.humidity = values.EXIT_CODE
            disconnect_read.temperature = values.EXIT_CODE
            self.__send(disconnect_read)
            self.__is_sending_running = False
            self.__client.close()
