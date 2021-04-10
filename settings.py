import values 

class Settings:
    def __init__(self):
        self.__server_ip = values.DEFAULT_IP
        self.__server_port = values.DEFAULT_PORT

        self.__limit_collecting_sensor_data = values.DEFAULT_LIMIT_COLLECTING_DATA_TO_GRAPH

        self.__sending_delay = values.DEFAULT_SENDING_DELAY
        self.__sending_delay_counter = values.DEFAULT_SENDING_DELAY-1

        self.__refresh_graps_delay = values.DEFAULT_GRAPHS_REFRESHING_DELAY
        self.__graphs_refresh_counter = values.DEFAULT_GRAPHS_REFRESHING_DELAY-1

        self.__collect_sensors_data_delay = values.DEFAULT_COLLECT_SENSOR_DATA_DELAY
        self.__collect_sensors_data_counter = values.DEFAULT_COLLECT_SENSOR_DATA_DELAY-1

    @property
    def server_ip(self):
        return self.__server_ip

    @server_ip.setter
    def server_ip(self, value):
        self.__server_ip = value

    @property
    def server_port(self):
        return self.__server_port

    @server_port.setter
    def server_port(self, value):
        self.__server_port = value

    @property
    def limit_collecting_sensor_data(self):
        return self.__limit_collecting_sensor_data

    @limit_collecting_sensor_data.setter
    def limit_collecting_sensor_data(self, value):
        self.__limit_collecting_sensor_data = int(value)

    @property
    def sending_delay(self):
        return self.__sending_delay

    @sending_delay.setter
    def sending_delay(self, value):
        self.__sending_delay = int(value)

    @property
    def sending_delay_counter(self):
        return self.__sending_delay_counter

    @sending_delay_counter.setter
    def sending_delay_counter(self, value):
        self.__sending_delay_counter = int(value)

    @property
    def refresh_graps_delay(self):
        return self.__refresh_graps_delay

    @refresh_graps_delay.setter
    def refresh_graps_delay(self, value):
        self.__refresh_graps_delay = int(value)

    @property
    def graphs_refresh_counter(self):
        return self.__graphs_refresh_counter

    @graphs_refresh_counter.setter
    def graphs_refresh_counter(self, value):
        self.__graphs_refresh_counter = int(value)

    @property
    def collect_sensors_data_delay(self):
        return self.__collect_sensors_data_delay

    @collect_sensors_data_delay.setter
    def collect_sensors_data_delay(self, value):
        self.__collect_sensors_data_delay = int(value)

    @property
    def collect_sensors_data_counter(self):
        return self.__collect_sensors_data_counter

    @collect_sensors_data_counter.setter
    def collect_sensors_data_counter(self, value):
        self.__collect_sensors_data_counter = int(value)
