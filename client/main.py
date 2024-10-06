import mqtt_to_socket
import client
import threading

# Create 2 threads to run the forward mqtt stream to socket service and the PySpark client

# MQTT to socket service
t1 = threading.Thread(target=mqtt_to_socket)
# PySpark client
t2 = threading.Thread(target=client)

# Start the threads
t1.start()
t2.start()