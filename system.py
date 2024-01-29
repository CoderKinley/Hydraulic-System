from components.Pump import HydraulicPump
from components.DirectionControlValve import DirectionControlValve
from components.DoubleActingCylinder import HydarulicActuator
import keyboard
import pyrebase
import time

class MainSystem:
    def __init__(self):
        self.time_counter = 0
        self.terminating_flag = False

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

    def connect_firebase(self, data, velocity):
        try:
            firebase = pyrebase.initialize_app(self.config)
            database = firebase.database()

            piston_data = {"Piston_extension": data, "velocity": velocity}

            database.push(piston_data)
            print("piston extension: " + str(data) + " Velocity: " + str(velocity))
            print("pushed to firebase...")

        except Exception as e:
            print("An error occurred:", str(e))

    def on_key_event(self, e):
        if e.event_type == keyboard.KEY_DOWN:
            if e.name.lower() == 'esc':
                print("\nTerminating the loop.")
                self.terminating_flag = True

    def run(self):
        keyboard.hook(self.on_key_event)
        
        while not self.terminating_flag:
            self.time_counter += 0.25
            time.sleep(0.25)
            disp = self.bypass_valves()

            self.connect_firebase(disp, self.time_counter)

    def bypass_valves(self):
         #test for hydraulic double acting actuator
        bore_diameter = 0.094 # m
        rod_diameter = 0.016 # mcls
        stroke_length = 0.6 # m maximum length the pistion rod extends
        initial_position = 0 # m initial position of the piston
        simulation_time = 0.25 # s
        discharge = 0.0032 # m^3/s
        packingFriction = 0 # N
        timer = self.time_counter
        motor_speed = 3600 
        oil_type = "skydrol_1"
        operating_pressure = 7845320 # in pascals

    
        efficiency = 0.85
        mass =  50000 # in KG
        pump_ON = True

        left_solenoid = 1
        right_solenoid = 0

        # Calling the pump function
        pump = HydraulicPump(            
            oil_type, 
            motor_speed, 
            operating_pressure, 
            mass, efficiency
            )

        density, viscosity, bulk_modulus = pump.getOil()
        
        flow_rate, pump_pressure = pump.simulate(pump_ON)
        print(flow_rate, pump_pressure)
        
        # calling the direction control valve function
        dcv = DirectionControlValve(
            density, 
            viscosity, 
            pump_pressure, 
            flow_rate
            )
        dcv.simulate(left_solenoid, right_solenoid)
        
        #  calling the hydarulic actuator signal
        hs = HydarulicActuator(
            bore_diameter,
            rod_diameter,
            stroke_length,
            initial_position,
            simulation_time,
            operating_pressure,
            density,
            discharge,
            packingFriction,
            timer

        )
        return hs.displacementExt(self.time_counter)

def main():
    main_system = MainSystem()
    main_system.run()

if __name__ == "__main__":
    main()
