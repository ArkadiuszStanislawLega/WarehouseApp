from tkinter import *
from ClientApp.sensor_view import SensorView
import strings
import values


class ClientAppView:
    def __init__(self, ip, port, app_version):
        self.__window = Tk()
        self.__window.title(strings.STRING_WINDOW_TITLE + " v" + str(app_version))
        self.__window.geometry(values.SIZE_WINDOW)

        # region connection
        self.__f_connection = Frame(self.__window)
        self.__f_connection.grid(row=0, column=0, pady=10)

        self.__l_title_entry_address = Label(self.__f_connection,
                                             text=strings.STRING_TITLE_ADRES_INPUT)

        self.__e_address = Entry(self.__f_connection,
                                 width=values.SIZE_FREQUENCYS_ENTRY_WIDTH,
                                 textvariable=StringVar(self.__f_connection, value=str(ip)))

        self.__l_title_entry_port = Label(self.__f_connection,
                                          text=strings.STRING_TITLE_PORT_INPUT)

        self.__e_port = Entry(self.__f_connection,
                              width=values.SIZE_FREQUENCYS_ENTRY_WIDTH,
                              textvariable=StringVar(self.__f_connection, value=str(port)))

        self.__b_connect = Button(self.__f_connection,
                                  text=strings.STRING_CONNECT)

        self.__b_disconnect = Button(self.__f_connection,
                                     text=strings.STRING_DISCONNECT,
                                     state=DISABLED)

        self.__l_title_entry_address.pack(side=LEFT)
        self.__e_address.pack(side=LEFT)
        self.__l_title_entry_port.pack(side=LEFT)
        self.__e_port.pack(side=LEFT)
        self.__b_connect.pack(side=LEFT, padx=5)
        self.__b_disconnect.pack(side=LEFT, padx=5)
        # endregion connection
        # region sensors
        self.__f_sensors = Frame(self.__window)
        self.__f_sensors.grid(row=1, column=0, pady=100)

        self.__sensors_views = {}
        self.__create_sesnsors_views()
        # endregion sensors
        # region settings
        self.__f_settings = Frame(self.__window)
        self.__f_settings.grid(row=2, column=0, pady=2)
        self.__l_sending_delay_title = Label(self.__f_settings,
                                             text=strings.STRING_DELAY_SENDING_TIME,
                                             justify=LEFT)

        self.__e_sending_delay_value = Entry(self.__f_settings,
                                             width=values.SIZE_FREQUENCYS_ENTRY_WIDTH,
                                             textvariable=StringVar(self.__f_settings, value=str(values.DEFAULT_SENDING_DELAY)))
        self.__l_next_send_title = Label(self.__f_settings,
                                         text=strings.STRING_NEXT_SENDING_TIME,
                                         justify=LEFT)
        self.__l_next_send_value = Label(self.__f_settings,
                                         text=strings.STRING_NEXT_SENDING_TIME_UKNOWN,
                                         justify=LEFT)

        self.__l_graphs_refresh_delay_title = Label(self.__f_settings,
                                                    text=strings.STRING_GRAPHS_REFRESHING_DELAY,
                                                    justify=LEFT)
        self.__e_graphs_refreshing_delay_value = Entry(self.__f_settings,
                                                       width=values.SIZE_FREQUENCYS_ENTRY_WIDTH,
                                                       textvariable=StringVar(self.__f_settings, value=str(values.DEFAULT_GRAPHS_REFRESHING_DELAY)))

        self.__l_limit_sensor_data_title = Label(self.__f_settings,
                                                 text=strings.STRING_TITLE_LIMIT_SENSOR_DATA,
                                                 justify=LEFT)
        self.__e_limit_sensor_data_value = Entry(self.__f_settings,
                                                 width=values.SIZE_FREQUENCYS_ENTRY_WIDTH,
                                                 textvariable=StringVar(self.__f_settings, value=str(values.DEFAULT_LIMIT_COLLECTING_DATA_TO_GRAPH)))

        self.__l_title_collect_sensors_data_delay = Label(self.__f_settings,
                                                          text=strings.STRING_TITLE_COLLECT_SENSORS_DATA_DELAY,
                                                          justify=LEFT)
        self.__e_collect_sensors_data_delay = Entry(self.__f_settings,
                                                    width=values.SIZE_FREQUENCYS_ENTRY_WIDTH,
                                                    textvariable=StringVar(self.__f_settings, value=str(values.DEFAULT_COLLECT_SENSOR_DATA_DELAY)))

        self.__l_sending_delay_title.grid(row=0, column=0, sticky=W)
        self.__e_sending_delay_value.grid(row=0, column=1, sticky=W)
        self.__l_graphs_refresh_delay_title.grid(row=1, column=0, sticky=W)
        self.__e_graphs_refreshing_delay_value.grid(row=1, column=1, sticky=W)
        self.__l_title_collect_sensors_data_delay.grid(
            row=0, column=2, sticky=W)
        self.__e_collect_sensors_data_delay.grid(row=0, column=3, sticky=W)
        self.__l_limit_sensor_data_title.grid(row=1, column=2, sticky=W)
        self.__e_limit_sensor_data_value.grid(row=1, column=3, sticky=W)
        self.__l_next_send_title.grid(row=2, column=0)
        self.__l_next_send_value.grid(row=2, column=1)
        # endregion settings
        # region console
        self.__f_console = Frame(self.__window)
        self.__f_console.grid(row=3, column=0, columnspan=4)

        self.__l_console_title = Label(self.__f_console,
                                       text=strings.STRING_EVENTS_LIST)
        self.__l_console_title.pack()

        self.__sb_console = Scrollbar(self.__f_console, orient=VERTICAL)
        self.__lb_console = Listbox(self.__f_console,
                                    width=values.SIZE_CONSOLE_WIDTH,
                                    yscrollcommand=self.__sb_console.set,
                                    selectmode=MULTIPLE)
        self.__lb_console.pack(side=LEFT, fill=Y, )

        self.__sb_console.config(command=self.__lb_console.yview)
        self.__sb_console.pack(side=RIGHT, fill=Y)
        # endregion console

    def __create_sesnsors_views(self):
        column = 0
        for i in range(values.NUMBER_OF_SENSORS):
            self.__sensors_views[i] = SensorView(self.__f_sensors,
                                                 row=0, column=column,
                                                 title=strings.STRING_SENSOR_NAME_UNKNOWN)
            column += 2

    def updateGraphs(self, timesValues, humidityValues, temperatureValues):
        for i in range(values.NUMBER_OF_SENSORS):
            if len(timesValues) == len(humidityValues[i]) == len(temperatureValues[i]) > 0 :
                    self.__sensors_views.get(i).show_graph(time_values=timesValues,
                                                        humidity_values=humidityValues.get(i),
                                                        temperature_values=temperatureValues.get(i))

    def update_sensor_view(self, sensor_id, digital_read):
        self.__sensors_views.get(sensor_id).update_values(title=str(sensor_id+1)+". " + strings.STRING_SENSOR_NAME,
                                                          temperature=digital_read.temperature,
                                                          humidity=digital_read.humidity)

    def updateSendingTime(self, time):
        formated = time.strftime(values.FORMAT_TIME)
        self.__l_next_send_value.config(text=formated)

    def get_limit_collecting_data(self):
        return self.__e_limit_sensor_data_value.get()

    def get_sending_delay(self):
        return self.__e_sending_delay_value.get()

    def get_graphs_refresh_delay(self):
        return self.__e_graphs_refreshing_delay_value.get()

    def get_address(self):
        return self.__e_address.get()

    def get_port(self):
        return self.__e_port.get()

    def get_collect_sensor_data_delay(self):
        return self.__e_collect_sensors_data_delay.get()

    def set_address(self, value):
        self.__e_address.insert(0, str(value))

    def set_port(self, value):
        self.__e_port.insert(0, str(value))

    @property
    def buttonConnect(self):
        return self.__b_connect

    @property
    def buttonDisconnect(self):
        return self.__b_disconnect

    @property
    def window(self):
        return self.__window

    def show(self):
        mainloop()

    def disableOrEnableFields(self):
        self.__connect_button_enable_switch()

    def add_to_console(self, text):
        self.__lb_console.insert(END, text)

    def __connect_button_enable_switch(self):
        if self.__b_connect['state'] == DISABLED:
            self.__b_connect.config(state=NORMAL)
            self.__b_disconnect.config(state=DISABLED)
            self.__e_address.config(state=NORMAL)
            self.__e_port.config(state=NORMAL)
            self.__e_sending_delay_value.config(state=NORMAL)
            self.__e_graphs_refreshing_delay_value.config(state=NORMAL)
            self.__e_collect_sensors_data_delay.config(state=NORMAL)
            self.__e_limit_sensor_data_value.config(state=NORMAL)
        else:
            self.__b_connect.config(state=DISABLED)
            self.__b_disconnect.config(state=NORMAL)
            self.__e_address.config(state=DISABLED)
            self.__e_port.config(state=DISABLED)
            self.__e_sending_delay_value.config(state=DISABLED)
            self.__e_graphs_refreshing_delay_value.config(state=DISABLED)
            self.__e_collect_sensors_data_delay.config(state=DISABLED)
            self.__e_limit_sensor_data_value.config(state=DISABLED)
