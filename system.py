import keyboard
import pyrebase
import time
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe

from MIV_System.components.Pump import HydraulicPump
from MIV_System.components.DirectionControlValve import DirectionControlValve
from MIV_System.components.DoubleActingCylinder import HydarulicActuator
from MIV_System.bypassValve import BypassValve
from MIV_System.decompressionValve import DecompressionValve
from MIV_System.serviceSealValve import ServiceSealValve
from MIV_System.MIVValve import MIVValve

keypress_val = 0

class MainSystem:
    def __init__(self):
        self.time_counter = 0
        self.event_time = 0
        self.left_solenoid_sig = 0
        self.right_solenoid_sig = 1
        self.stroke_position = 0
        self.last_stroke_position = 0
        self.terminating_flag = False
        self.signal_flag_dac_bp_ext = False
        self.signal_flag_dac_bp_ret = False

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
    # To subscribe to a topic in the mqtt for the receiving of the command from the front end side
    def subscribe_mqtt(self):
        while True:
            # check for the changes in the front end
            commandMqtt = subscribe.simple("MQTTCommand", hostname="202.144.139.110")
            strMQtt = str(commandMqtt.payload)
            splitMqtt = strMQtt[2:-1]
            print(strMQtt)
            return splitMqtt

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
                print("\nTerminating the loop.")
                self.terminating_flag = True

        if e.event_type == keyboard.KEY_DOWN:
            if e.name == '1':
                # print("pressed 1")
                self.event_time = 0
                self.left_solenoid_sig = 1
                self.right_solenoid_sig = 0
                self.last_stroke_position = self.stroke_position
                self.signal_flag_dac_bp_ext = True
                self.signal_flag_dac_bp_ret = False
                
            elif e.name == '0':
                # print("pressed 0") 
                self.event_time = 0  
                self.left_solenoid_sig = 0
                self.right_solenoid_sig = 1
                self.last_stroke_position = self.stroke_position
                self.signal_flag_dac_bp_ret = True
                self.signal_flag_dac_bp_ext = False

            elif e.name.lower() == 'd':
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
    def run(self):
        keyboard.hook(self.on_key_event)
        while not self.terminating_flag:
            # couter_val must support 0.25/2 ........
            # every 1second it will send 64 data
            counter_val = 0.0625
            self.time_counter += counter_val
            self.event_time += counter_val
            print("Time value--> ", self.event_time)
            time.sleep(counter_val)
                        
            # calling the different valves functions
            displacement, q, f_extension, v_extension, power_input, power_output = self.bypass_valves()
            self.miv_valve()
            self.decompression_valve()
            self.service_seal_valve()
            
            dataMqtt = ",".join(map(str,[
                self.bypass_valves()
            ]))
            publish.single("Valve", payload=dataMqtt, qos=0, retain=False, hostname="202.144.139.110",
                           port=1883, client_id="", keepalive=45, will=None, auth=None, tls=None)
            
            # for setting the current postion of the piston stroke
            self.stroke_position = displacement 

            # calling the firebase connection function to upload the data to the firebase
            self.connect_firebase(displacement, v_extension, q, f_extension, power_input, power_output)

    def initialize_valves(self, ValveClass):
        return ValveClass(
            self.event_time, # from global variable at top
            self.stroke_position, # determines the current positon
            self.signal_flag_dac_bp_ext,
            self.signal_flag_dac_bp_ret, 
            self.last_stroke_position,
            self.time_counter,
            self.left_solenoid_sig,
            self.right_solenoid_sig
        ).run()

    # just the bypass logic
    def bypass_valves(self):
        return self.initialize_valves(BypassValve)
    
    def decompression_valve(self):
        return self.initialize_valves(DecompressionValve)
    
    def service_seal_valve(self):
        return self.initialize_valves(ServiceSealValve)
    
    def miv_valve(self):    
        return self.initialize_valves(MIVValve)
    
def main():
    main_system = MainSystem()
    main_system.run()

if __name__ == "__main__":
    main()
