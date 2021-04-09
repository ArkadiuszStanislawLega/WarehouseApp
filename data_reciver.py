import time
from datetime import datetime
from smbus import SMBus
from bme280 import BME280
from models import DigitalReading

class DataReceiver:
    """
    Klasa ktora pracuje z multiplexerem TCA9548A - Adafruit.
    Obsuguje 8 czujnikow na raz zmieniajac kanaly. Multiplexer uzywa do komunikacji 
    I2C na adresie 0x70 - 0x77.
    Czujniki to BM280 - Waveshare. Adres do komunikacji to 0x77 lub 0x78 w zaleznosci 
    od polaczenia 
    Arguments.
        BasicModel {BasicModel} -- opsi
    """

    CONNECTION_ERROR_MESSAGE = "Connection error."

    MAX_NUMBER_OF_CHANNELS = 8
    MB280_ADDRESS  = 0x77
    MULTIPLEXER_ADDRESS = 0x70

    def __init__(self, bus = 1, delay = 1):
        self.__bus = bus
        self.__i2cbus = SMBus(self.__bus)
        self.__delay = delay
        self.__is_receiving = False
        self.__channels_addresses = {
                0 : 0b00000001,
                1 : 0b00000010,
                2 : 0b00000100,
                3 : 0b00001000,
                4 : 0b00010000,
                5 : 0b00100000,
                6 : 0b01000000,
                7 : 0b10000000
        }

        self.__sensors = {
            0 : BME280(self.MB280_ADDRESS),
            1 : BME280(self.MB280_ADDRESS),
            2 : BME280(self.MB280_ADDRESS),
            3 : BME280(self.MB280_ADDRESS),
            4 : BME280(self.MB280_ADDRESS),
            5 : BME280(self.MB280_ADDRESS),
            6 : BME280(self.MB280_ADDRESS),
            7 : BME280(self.MB280_ADDRESS)
        }

    @property
    def delay(self):
        self.__delay

    @delay.setter
    def delay(self, value):
        self.__delay = value

    @property
    def sensors(self):
        self.__sensors

    def get_sensor_data(self, chanel_id):
        if chanel_id >= 0 and chanel_id < self.MAX_NUMBER_OF_CHANNELS:
            try:
                dr = DigitalReading(time=datetime.now(),
                                    temperature=self.__sensors.get(chanel_id).get_temperature(), 
                                    humidity=self.__sensors.get(chanel_id).get_humidity())
                return dr
            except Exception:
                # print("Nie podłączono kanału ", chanel_id)
                pass

    def change_channel(self, chanel_id):
        if chanel_id >= 0 and chanel_id < self.MAX_NUMBER_OF_CHANNELS:
            self.__i2cbus.write_byte(self.MULTIPLEXER_ADDRESS, self.__channels_addresses.get(chanel_id))



    def __change_and_print(self,  chanel_id):
        self.__change_channel(chanel_id)
        self.__print_values(chanel_id)


    def start_receiving(self):
        self.__is_receiving = True
        while (self.__is_receiving):
            for i in range(len(self.__sensors)):
                self.__change_and_print(i)


            time.sleep(self.__delay)  
            print(40*"=")
