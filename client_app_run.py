"""2021 - Autor: Arkadiusz Łęga, email:horemheb@vp.pl"""

import threading
import time
from datetime import datetime, timedelta
from ClientApp.client_app_controller import ClientAppController
from ClientApp.client_app_model import ClientAppModel
from ClientApp.client_app_view import ClientAppView
from settings import Settings
import strings
import paths
import values


class MainLoop:
    """
    Klasa odpowiadająca za zarządzanie wszystkimi wątkami aplikacji.
    Łączy model, widok i kontroler.
    """

    APP_VERSION = 1.1

    def __init__(self):
        """
        Inicjuje podstawowe wartości dla własności klasy.
        Pobiera wartości z plików i inicjuje model, widok i kontroller
        aplikacji.
        """
        self.__is_loop_working = True
        self.__time_next_message_send = 0

        self.__settings = Settings()
        self.__read_user_settings()

        self.__view = ClientAppView(ip=self.__settings.server_ip,
                                    port=self.__settings.server_port,
                                    app_version=self.APP_VERSION)

        self.__model = ClientAppModel(view=self.__view,
                                      ip=self.__settings.server_ip,
                                      port=self.__settings.server_port)

        self.__controller = ClientAppController(model=self.__model,
                                                view=self.__view,
                                                parent=self)

        self.__view.buttonConnect['command'] = self.__controller.connect
        self.__view.buttonDisconnect['command'] = self.__controller.disconnect
        self.__view.window.protocol('WM_DELETE_WINDOW', self.__controller.exit)

        main_loop = threading.Thread(target=self.__loop)
        main_loop.daemon = True
        main_loop.start()

        self.__view.show()

    @property
    def is_loop_working(self):
        """
        Flaga wskazująca działanie głównej pętli aplikacji.
        """
        return self.__is_loop_working

    @is_loop_working.setter
    def is_loop_working(self, value):
        self.__is_loop_working = value

    def __read_from_file_server_ip(self):
        try:
            with open(paths.PATH_ADDRESS) as reader:
                self.__settings.server_ip = reader.readline()
        finally:
            reader.close()

    def __read_from_file_server_port(self):
        try:
            with open(paths.PATH_PORT) as reader:
                self.__settings.server_port = int(reader.readline())

        except ValueError:
            self.__settings.server_port = values.DEFAULT_PORT
            print(strings.STRING_PORT_READING_ERROR)
        finally:
            reader.close()

    def __write_new_address(self):
        with open(paths.PATH_ADDRESS, 'w') as file:
            file.write(self.__view.get_address())
            file.close()

    def __write_new_port(self):
        with open(paths.PATH_PORT, 'w') as file:
            file.write(self.__view.get_port())
            file.close()

    def __read_user_settings(self):
        self.__read_from_file_server_ip()
        self.__read_from_file_server_port()

    def __increment_counters(self):
        self.__settings.sending_delay_counter += 1
        self.__settings.graphs_refresh_counter += 1
        self.__settings.collect_sensors_data_counter += 1

    def __refres_graphs(self):
        self.__view.updateGraphs(temperatureValues=self.__model.temperature_values,
                                 humidityValues=self.__model.humidity_values,
                                 timesValues=self.__model.time_values)
        self.__settings.graphs_refresh_counter = 0

    def __loop(self):
        while self.__is_loop_working:
            self.__increment_counters()
            if self.__settings.collect_sensors_data_counter == self.__settings.collect_sensors_data_delay:
                self.__settings.collect_sensors_data_counter = 0
                self.__model.collect_data_from_sensors()

            if self.__settings.graphs_refresh_counter == self.__settings.refresh_graps_delay:
                self.__settings.graphs_refresh_counter = 0
                self.__refres_graphs()

            if self.__settings.sending_delay_counter >= self.__settings.sending_delay:
                self.__settings.sending_delay_counter = 0
                self.__model.send_data_from_sensors()
                next_update = datetime.now()+timedelta(seconds=self.__settings.sending_delay)
                self.__view.updateSendingTime(next_update)

            time.sleep(1)

    def collect_settings_from_GUI(self):
        """
        Pobiera wartości wpisane w polach formatki aplikacji.
        Zapisuje wprowadzone wartości do plików z których są pobierane
        ostatnie ustawienia użytkownika.
        """
        try:
            v_sending_delay = int(self.__view.get_sending_delay())
            v_graphs_refresh_delay = int(
                self.__view.get_graphs_refresh_delay())
            v_collect_sensors_data_delay = int(
                self.__view.get_collect_sensor_data_delay())
            v_limit_collecting_data = int(
                self.__view.get_limit_collecting_data())

            self.__settings.sending_delay = v_sending_delay
            self.__settings.refresh_graps_delay = v_graphs_refresh_delay
            self.__settings.collect_sensors_data_delay = v_collect_sensors_data_delay
            self.__settings.limit_collecting_sensor_data = v_limit_collecting_data

            self.__write_new_address()
            self.__write_new_port()

            self.__model.get_settings_from_GUI()
            return True
        except ValueError:
            self.__view.add_to_console(strings.STRING_VALUE_ERROR_MESSAGE)
            return False


if __name__ == '__main__':
    MainLoop()
