# A distributed system for collecting humidity and temperature parameters in containers

There are three server applications, a client application for the device for collecting parameters, and a client application for reading data from devices.

## Hardware

1. Raspberry Pi 4
2. TCA9548A multiplexer - Adafruit
3. BME-280 temperature and humidity sensors

Wires were connected to the TCA9548A - Adafruit multiplexer from the Raspberry Pi pins. Thanks to it, you can connect 8 devices with the same I2C address at the same time. The multiplexer operates on 8 addresses from 0x70 to 0x77 depending on the high or low status on A0, A1 and A2 - thanks to them you can set the I2C address.

## Software

1. MagApp – an application that allows you to manage sensors in warehouses,
check the current status of parameters in containers and view charts
related to containers;
2. ServerMagApp – an application that allows devices to communicate
with the server and sending data to the database;
3. ClientMagApp – an application that allows devices to communicate
located in warehouses with the server to which they send data.