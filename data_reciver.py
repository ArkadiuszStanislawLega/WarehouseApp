"""2021 - Autor: Arkadiusz Łęga, email:horemheb@vp.pl"""

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
    """

    CONNECTION_ERROR_MESSAGE = "Connection error."

    MAX_NUMBER_OF_CHANNELS = 8
    MB280_ADDRESS = 0x77
    MULTIPLEXER_ADDRESS = 0x70

    def __init__(self, bus=1):
        self.__bus = bus
        self.__i2cbus = SMBus(self.__bus)
        self.__is_receiving = False
        self.__channels_addresses = {
            0: 0b00000001,
            1: 0b00000010,
            2: 0b00000100,
            3: 0b00001000,
            4: 0b00010000,
            5: 0b00100000,
            6: 0b01000000,
            7: 0b10000000
        }

        self.__sensors = {
            0: BME280(self.MB280_ADDRESS),
            1: BME280(self.MB280_ADDRESS),
            2: BME280(self.MB280_ADDRESS),
            3: BME280(self.MB280_ADDRESS),
            4: BME280(self.MB280_ADDRESS),
            5: BME280(self.MB280_ADDRESS),
            6: BME280(self.MB280_ADDRESS),
            7: BME280(self.MB280_ADDRESS)
        }

    def get_sensor_data(self, chanel_id):
        """
        Zwraca odczyt z czujnika z określonego kanału na
        multiplekserze.

        Args:
            chanel_id ([int]): Numer kanału.

        Returns:
            [DigitalRead]: Odczyt z czujnika.
        """
        if chanel_id >= 0 and chanel_id < self.MAX_NUMBER_OF_CHANNELS:
            try:
                sensor = self.__sensors.get(chanel_id)
                digital_read = DigitalReading(time=datetime.now(),
                                              temperature=sensor.get_temperature(),
                                              humidity=sensor.get_humidity())
                return digital_read
            except Exception:
                # print("Nie podłączono kanału ", chanel_id)
                return None

    def change_channel(self, chanel_id):
        """
        Zmienia adress kanału na multiplekserze z którego
        będzie odczytywał dane na adresie 0x77.

        Args:
            chanel_id ([int]): Numer kanału na multiplekserze od 0 do 7.
        """
        if chanel_id >= 0 and chanel_id < self.MAX_NUMBER_OF_CHANNELS:
            chanel_address = self.__channels_addresses.get(chanel_id)
            self.__i2cbus.write_byte(self.MULTIPLEXER_ADDRESS, chanel_address)
