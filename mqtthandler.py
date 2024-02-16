import paho.mqtt.client as mqtt
import threading

class MQTTSubscriber:
    def __init__(self, topic):
        self.topic = topic
        self.received_message = None
        self.client = mqtt.Client()
        self.client.on_message = self.on_message

        # Create a reentrant lock to protect the received_message attribute
        self.lock = threading.RLock()

        try:
            self.client.connect("202.144.139.110")
            self.client.subscribe(self.topic)
            self.client.loop_start()
        except Exception as e:
            print(f"MQTT Subscribe failed: {e}")

    def on_message(self, client, userdata, message):
        if message.topic == self.topic:
            # Acquire the lock before accessing received_message
            with self.lock:
                try:
                    self.received_message = message.payload.decode("utf-8")
                    print("Received Message____from__TOpic--->", self.topic, " With message---->", self.received_message)
                except UnicodeDecodeError as e:
                    print(f"Error decoding message payload: {e}")

    def get_received_message(self):
        # Acquire the lock before reading received_message
        with self.lock:
            return self.received_message

    def disconnect(self):
        try:
            # Acquire the lock before stopping the loop and disconnecting
            with self.lock:
                self.client.loop_stop()
            self.client.disconnect()
        except Exception as e:
            print(f"Error disconnecting MQTT client: {e}")


# def main():
#     MQTTSubscriber("MQTTCommand")

# if __name__ == "__main__":
#     main()


# simulating the mqtt server connection but fake 
# class MQTTSubscriber:
#     def __init__(self, topic):
#         self.topic = topic
#         self.received_message = "1"

#     def get_received_message(self):
#         return self.received_message
