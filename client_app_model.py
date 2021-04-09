import socket
import pickle
import random
from datetime import datetime, date
from models import DigitalReading
from data_reciver import DataReceiver
import time
import strings
import values


class ClientAppModel:
    def __init__(self, view, ip, port):
        self.__view = view
        self.__is_sending_running = False
        self.__is_readings_taken = True
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__data_reciver = DataReceiver()
        self.__counter = 0

        self.__server_ip = str(ip)
        self.__server_port = int(port)

        self.__limit_collecting_sensor_data = 5

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
        # self.run()
    # region properties
    @property
    def view(self):
        return self.__view

    @property
    def server_ip(self):
        return self.__server_ip

    @server_ip.setter
    def server_ip(self, value):
        self.__server_ip = str(values)

    @property
    def server_port(self):
        return self.__server_port

    @server_port.setter
    def server_port(self, value):
        self.__server_port = int(values)

    @property
    def server_address(self):
        return self.__server_address

    @property
    def time_values(self):
        return self.__time_values

    @property
    def temperature_values(self):
        return self.__temperature_values

    @property
    def humidity_values(self):
        return self.__humidity_values

    @property
    def is_sending_running(self):
        return self.__is_sending_running

    @property
    def is_readings_taken(self):
        return self.__is_readings_taken

    @is_readings_taken.setter
    def is_readings_taken(self, value):
        self.__is_sending_running = value

    # endregion properties

    def __timeAndMessage(self, message):
        time = datetime.now().strftime(values.FORMAT_TIME)
        return time + message

    def __send(self, digital_read):
        if self.__is_sending_running:
            if digital_read:
                if digital_read.temperature == values.EXIT_CODE and digital_read.humidity == values.EXIT_CODE:
                    self.__view.add_to_console(self.__timeAndMessage(strings.STRING_DISCONNECT))
                else:
                    self.__view.add_to_console(self.__timeAndMessage(strings.STRING_SENDING_MESSAGE + str(digital_read)))

                message = pickle.dumps(digital_read)

                send_length = b' ' * values.HEADER

                # self.__debug_mode(message, send_length)

                try:
                    self.__client.send(send_length)
                    self.__client.send(message)
                    self.__view.add_to_console(self.__timeAndMessage(strings.STRING_SENT_MESSAGE))
                except socket.error:
                    self.__view.add_to_console(self.__timeAndMessage(self.__timeAndMessage(strings.STRING_SENDING_ERROR)))
                    self.__is_sending_running = False
                    self.__client = socket.socket()
                    while not self.__is_sending_running:
                        try:
                            self.__view.add_to_console(self.__timeAndMessage(strings.STRING_ATTEMPT_RECONNECT))
                            self.__client.connect(self.__server_address)
                            self.__is_sending_running = True
                            self.__view.add_to_console(self.__timeAndMessage(strings.STRING_SUCCESSFUL_RECCONECT))
                        except socket.error:
                            time.sleep(2)

            else:
                self.__view.add_to_console(strings.STRING_SENSOR_IS_NOT_CONNECTED)

    def getSettingsFromGUI(self):
        try:
            self.__server_ip = self.__view.get_address()
            self.__server_port = int(self.__view.get_port())
            self.__server_address = (self.__server_ip, self.__server_port)
            self.__limit_collecting_sensor_data = int(self.__view.get_limit_collecting_data())
            self.__view.add_to_console(strings.STRING_VALUE_ERROR_MESSAGE)
            return True
        except:
            return False

    def sendDataFromSensors(self):
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

    def collectDataFromSensors(self):
        if len(self.__time_values) < self.__limit_collecting_sensor_data:
            self.__time_values.append(datetime.now())
            for i in range(values.NUMBER_OF_SENSORS):
                digital_read = self.__get_data_recive(i)
                if digital_read:
                    digital_read.id = i

                    self.__view.update_sensor_view(i, digital_read)
                    self.__temperature_values.get(i).append(digital_read.temperature)
                    self.__humidity_values.get(i).append(digital_read.humidity)
        else:
            self.__time_values.pop(0)
            self.__time_values.append(datetime.now())
            for i in range(values.NUMBER_OF_SENSORS):
                digital_read = self.__get_data_recive(i)
                if digital_read:
                    digital_read.id = i

                    self.__view.update_sensor_view(i, digital_read)
                    self.__temperature_values.get(i).pop(0)
                    self.__temperature_values.get(
                        i).append(digital_read.temperature)
                    self.__humidity_values.get(i).pop(0)
                    self.__humidity_values.get(i).append(digital_read.humidity)


    def connect(self):
        if not self.__is_sending_running:
            self.__view.add_to_console(self.__timeAndMessage(strings.STRING_CONNECTING + str(self.__server_ip) + ":" + str(self.__server_port) + " ..."))
            self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__client.connect(self.__server_address)
            self.__is_sending_running = True

    def disconnect(self):
        if self.__is_sending_running:
            disconnect_read = DigitalReading()
            disconnect_read.humidity = values.EXIT_CODE
            disconnect_read.temperature = values.EXIT_CODE
            self.__send(disconnect_read)
            self.__is_sending_running = False
            self.__client.close()
