import keyboard
import pyrebase
import time
# import paho.mqtt.publish as publish
# import paho.mqtt.subscribe as subscribe
from threading import *

from MIV_System.bypassValve import BypassValve
from MIV_System.decompressionValve import DecompressionValve
from MIV_System.serviceSealValve import ServiceSealValve
from MIV_System.MIVValve import MIVValve
from mqtthandler import MQTTSubscriber

keypress_val = 0

class MainSystem:
    def __init__(self):
        self.terminating_flag = False
        self.time_counter = 0
        self.event_time = 0

        self.mqtt_sub_bypass = MQTTSubscriber("MQTTCommand")
        self.mqtt_sub_dv = MQTTSubscriber("MQTTCommandDV")
        self.mqtt_sub_miv = MQTTSubscriber("MQTTCommandMIV")
        self.mqtt_sub_ssv = MQTTSubscriber("MQTTCommandSSV")


        # initilising the required data for uploading the data
        self.config = {
            "apiKey": "AIzaSyARhmKyZm_BcsEioLHWCK7XP2Gg6RMavN0",
            "authDomain": "pyto-db701.firebaseapp.com",
            "projectId": "pyto-db701",
            "databaseURL": "https://pyto-db701-default-rtdb.firebaseio.com/",
            "storageBucket": "pyto-db701.appspot.com",
            "messagingSenderId": "229412264516",
            "appId": "1:229412264516:web:f2fdafadec99efeef23a11",
            "measurementId": "G-PYES5CSJQ7"
        }

    # handles the firebase request
    def connect_firebase(
            self, 
            p_extension, 
            velocity,
            flow_rate, 
            f_extension, 
            power_input, 
            power_output
        ):
        
        try:
            firebase = pyrebase.initialize_app(self.config)
            database = firebase.database()

            piston_data = {
                "Piston_extension": p_extension, 
                "velocity": velocity, 
                "flow_rate" : flow_rate, 
                "force_extension": f_extension, 
                "power_input" : power_input, 
                "power_output" : power_output 
            }

            database.push(piston_data)
            # print("piston extension: " + str(data) + " Velocity: " + str(velocity))
            print("pushed to firebase...")

        except Exception as e:
            print("error! ", str(e))

    # just a keyboard functionality which will be replaced by the input data form the frontend
    def on_key_event(self, e):
        if e.event_type == keyboard.KEY_DOWN:
            if e.name.lower() == 'esc':
                print("\nSimulation Stopped successfully...")
                self.terminating_flag = True
        if e.event_type == keyboard.KEY_DOWN:
            if e.name.lower() == 'd':
                self.remove_all_data()        

    # remove the data from firebase
    def remove_all_data(self):
        try:
            firebase = pyrebase.initialize_app(self.config)
            database= firebase.database()
            database.remove()
            print("All data removed from Firebase")
        except Exception as e:
            print("Error while removing data from Firebase: ", str(e))

    # Function to start calling the individual components and start running
    def run_sys(self, bpv, dv,ssv,miv):
        keyboard.hook(self.on_key_event)
        while not self.terminating_flag:
            # couter_val must support 0.25/2 ........
            # every 1second it will send 64 data
            counter_val = 0.0625
            self.time_counter += counter_val
            self.event_time += counter_val
            
            bypass_thread = Thread(target=bpv.run, args=(self.time_counter, self.event_time))
            bypass_thread.start()

            # calling the 4 main valves
            time.sleep(counter_val)
            
    def initialize_valves(self, ValveClass):
        return ValveClass(
            self.mqtt_sub_bypass,
        )
    
def main():
    print("Simulation started successfully...")
    main_system = MainSystem()
    bpv = main_system.initialize_valves(BypassValve)
    # dv = main_system.initialize_valves(DecompressionValve)
    # ssv = main_system.initialize_valves(ServiceSealValve)
    # miv = main_system.initialize_valves(MIVValve)

    main_system.run_sys(bpv,1,2,3)

if __name__ == "__main__":
    main()
