import socket
import paho.mqtt.client as mqtt

# MQTT settings
MQTT_BROKER = '127.0.0.1'  # MQTT broker address
MQTT_PORT = 1883            # MQTT port
MQTT_TOPIC = 'weather/stations/#'  # Topic to subscribe to

# Socket settings
SOCKET_HOST = 'localhost'
SOCKET_PORT = 9999

# Create a socket connection to send data to Spark
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SOCKET_HOST, SOCKET_PORT))
server_socket.listen(1)
print(f"Listening on socket {SOCKET_HOST}:{SOCKET_PORT}")

client_socket, addr = server_socket.accept()
print(f"Socket connection from {addr}")

# Callback when a message is received from the MQTT broker
def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"Received MQTT message: {message}")
    # Send the message to the socket
    client_socket.send(f"{message}\n".encode())

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe(MQTT_TOPIC)

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT broker")

# Set up the MQTT client
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.on_disconnect = on_disconnect

# Connect to the MQTT broker
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Start the MQTT client loop
mqtt_client.loop_forever()
