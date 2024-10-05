import paho.mqtt.client as mqtt
import json

# Callback when the client receives a CONNACK response from the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected to MQTT broker')
        # Subscribe to the relevant topics
        client.subscribe('weather/stations/#')
        print('Subscribed to weather stations data')
    else:
        print(f'Connection failed with code {rc}')

# Callback when a message is received from the broker
def on_message(client, userdata, msg):
    weather_data = json.loads(msg.payload.decode())
    station_id = weather_data.get('stationId')
    temperature = float(weather_data.get('temperature'))
    wind_speed = float(weather_data.get('windSpeed'))
    pressure = float(weather_data.get('pressure'))

    # print(f'Received data from station {station_id}')
    # print('Temperature:', temperature)
    # print('Wind Speed:', wind_speed)
    # print('Pressure:', pressure)

    # # Example alert conditions
    # if temperature and temperature > 44.9:
    #     print(f'Alert: High temperature detected at station {station_id}')
    #     print('Temperature:', temperature)
    #     print('\n' * 3)

    if wind_speed and (wind_speed) > 99 and pressure and pressure > 999:
        print(f'Alert: High wind speed detected at station {station_id}')
        print('Wind Speed:', wind_speed)
        print('Pressure:', pressure)
        print('\n' * 3)
    


# Callback when a client disconnects
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected disconnection.')

# Callback to handle errors
def on_log(client, userdata, level, buf):
    print(f'Log: {buf}')

# Initialize MQTT client
client = mqtt.Client()

# Assign callback functions
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
# client.on_log = on_log  # Optional, to log MQTT activity

# Connect to the broker
client.connect('127.0.0.1', 1883, 60)  # Replace with your broker address

# Start the MQTT client
client.loop_forever()
