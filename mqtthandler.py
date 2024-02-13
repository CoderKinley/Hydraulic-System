# import paho.mqtt.client as mqtt
# import time

# class MQTTSubscriber:
#     def __init__(self, topic):
#         self.topic = topic
#         self.received_message = None
#         self.client = mqtt.Client()
#         self.client.on_message = self.on_message

#         try:
#             self.client.connect("202.144.139.110")
#             print("herererer")
#             self.client.subscribe(self.topic)
#             print("herererer")
#             self.client.loop_start()
#         except Exception as e:
#             print(f"Bro MQTT connection or subscription failed: {e}")

#     def on_message(self, client, userdata, message):
#         if message.topic == self.topic:
#             try:
#                 self.received_message = message.payload.decode("utf-8")
#             except UnicodeDecodeError as e:
#                 print(f"Error decoding message payload: {e}")

#     def get_received_message(self):
#         return self.received_message

#     def disconnect(self):
#         try:
#             self.client.loop_stop()
#             self.client.disconnect()
#         except Exception as e:
#             print(f"Error disconnecting MQTT client: {e}")

# def main():
#     MQTTSubscriber("MQTTCommand")

# if __name__ == "__main__":
#     main()


# simulating the mqtt server connection but fake 
class MQTTSubscriber:
    def __init__(self, topic):
        self.topic = topic
        self.received_message = "1"

    def get_received_message(self):
        return self.received_message
