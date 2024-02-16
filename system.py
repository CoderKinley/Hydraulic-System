from keyboard import *
import pyrebase
import time
from threading import *

from MIV_System.bypassValve import BypassValve
from MIV_System.decompressionValve import DecompressionValve
from MIV_System.serviceSealValve import ServiceSealValve
from MIV_System.MIVValve import MIVValve
from mqtthandler import MQTTSubscriber
from firebase import FirebaseConnectivity

keypress_val = 0

class MainSystem:
    def __init__(self):
        self.terminating_flag = False
        self.time_counter = 0
        self.event_time = 0

        # <-------------- temporary test logic will be removed later ----------------->
        self.bpv_flag = 0
        self.dv_flag = 0
        self.miv_flag = 0
        self.ssv_flag = 0
        # <-------------- temporary test logic will be removed later ----------------->

        self.mqtt_sub_bypass = MQTTSubscriber("MQTTCommand")
        self.mqtt_sub_dv = MQTTSubscriber("MQTTCommandDV")
        self.mqtt_sub_miv = MQTTSubscriber("MQTTCommandMIV")
        self.mqtt_sub_ssv = MQTTSubscriber("MQTTCommandSSV")

    # handles the firebase request
    def connect_firebase(self):
       firebaseConnect = FirebaseConnectivity()
       firebaseConnect.connect_firebase(1,2,3,4,5,6)

    # just a keyboard functionality which will be replaced by the input data form the frontend
    def on_key_event(self, e):
        if e.event_type == KEY_DOWN:
            if e.name.lower() == 'esc':
                print("\nSimulation Stopped successfully...")
                self.terminating_flag = True
                
        if e.event_type == KEY_DOWN:
            if e.name.lower() == 'd':
                pass
                # self.remove_all_data()

            # <-------------- temporary test logic will be removed later ----------------->
            # bypass
            if e.name.lower() == '1':
                self.bpv_flag = '1'

            if e.name.lower() == '2':
                self.bpv_flag = '0'

            # decompression valve
            if e.name.lower() == '3':
                self.dv_flag = '1'

            if e.name.lower() == '4':
                self.dv_flag = '0'

            #  MIV valve
            if e.name.lower() == '5':
                self.miv_flag = '1'

            if e.name.lower() == '6':
                self.miv_flag = '0'

            #  Service seal valve
            if e.name.lower() == '7':
                self.ssv_flag = '1'

            if e.name.lower() == '8':
                self.ssv_flag = '0'

            # <-------------- temporary test logic will be removed later ----------------->
                
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
        hook(self.on_key_event)
        while not self.terminating_flag:
            # couter_val must support 0.25/2 ........
            # every 1second it will send 64 data
            counter_val = 0.0625
            self.time_counter += counter_val
            self.event_time += counter_val
            
            bypass_thread = Thread(target=bpv.run, args=(self.time_counter, self.event_time, self.bpv_flag))
            decompression_thread = Thread(target=dv.run, args=(self.time_counter, self.event_time, self.dv_flag))
            service_seal_thread = Thread(target=ssv.run, args=(self.time_counter, self.event_time, self.ssv_flag))
            miv_thread = Thread(target=miv.run, args=(self.time_counter, self.event_time, self.miv_flag))

            bypass_thread.start()
            decompression_thread.start()
            service_seal_thread.start()
            miv_thread.start()

            # calling the 4 main valves
            time.sleep(counter_val)
            
    def initialize_valves(self, ValveClass):
        if(str(ValveClass) == "<class 'MIV_System.bypassValve.BypassValve'>"):
            mqtt = self.mqtt_sub_bypass

        elif(str(ValveClass) == "<class 'MIV_System.decompressionValve.DecompressionValve'>"):
            mqtt = self.mqtt_sub_dv

        elif(str(ValveClass) == "<class 'MIV_System.MIVValve.MIVValve'>"):
            mqtt = self.mqtt_sub_miv

        elif(str(ValveClass)=="<class 'MIV_System.serviceSealValve.ServiceSealValve'>"):
            mqtt = self.mqtt_sub_ssv

        return ValveClass(
            mqtt,
        )
    
def main():
    print("Simulation started successfully...")
    main_system = MainSystem()
    bpv = main_system.initialize_valves(BypassValve)
    dv = main_system.initialize_valves(DecompressionValve)
    ssv = main_system.initialize_valves(ServiceSealValve)
    miv = main_system.initialize_valves(MIVValve)

    main_system.run_sys(bpv,dv,ssv,miv)

if __name__ == "__main__":
    main()
