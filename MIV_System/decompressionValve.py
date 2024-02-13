import paho.mqtt.publish as publish
from MIV_System.components.Pump import HydraulicPump
from MIV_System.components.DirectionControlValve import DirectionControlValve
from MIV_System.components.DoubleActingCylinder import HydarulicActuator


class DecompressionValve:
    def  __init__(self, mqtt_subscriber_cmds):
        print("starting decompression valve...")
        self.mqtt_subscriber_cmds = mqtt_subscriber_cmds

        self.left_solenoid_sig = 0
        self.right_solenoid_sig = 1
        self.stroke_position = 0
        self.last_stroke_position = 0
        self.terminating_flag = False
        self.signal_flag_dac_bp_ext = False
        self.signal_flag_dac_bp_ret = False
        self.received_message = 0 
        self.prev_received_message = self.received_message
        self.time_value = 0
    
    # code to define the time instant of the system under functionality 
    def system_time_defination(self):
        self.time_value += 0.0625

    def initialization_values(self, time_counter, event_time):
        self.received_message = self.mqtt_subscriber_cmds.get_received_message()
        
        if self.received_message is not None:
            if self.received_message == '1':
                self.left_solenoid_sig = 1
                self.right_solenoid_sig = 0
                self.last_stroke_position = self.stroke_position
                self.signal_flag_dac_bp_ext = True
                self.signal_flag_dac_bp_ret = False
                if self.prev_received_message != self.received_message:
                    self.time_value = 0
                    self.prev_received_message = self.received_message 


            elif self.received_message == '0':
                self.left_solenoid_sig = 0
                self.right_solenoid_sig = 1
                self.last_stroke_position = self.stroke_position
                self.signal_flag_dac_bp_ret = True
                self.signal_flag_dac_bp_ext = False
                if self.prev_received_message != self.received_message:
                    self.time_value = 0
                    self.prev_received_message = self.received_message   

    def run(self, time_counter, event_time):
         #test for hydraulic double acting actuator
        bore_diameter = 0.15 # m
        rod_diameter = 0.016 # mcls
        stroke_length = 2 # m maximum length the pistion rod extends
        initial_position = 0 # m initial position of the piston
        simulation_time = 0.25 # s
        discharge = 0.0032 # m^3/s
        packingFriction = 0 # N
        timer = time_counter
        motor_speed = 3600 
        oil_type = "skydrol_1"
        operating_pressure = 7845320 # in pascals

        efficiency = 0.85
        mass =  50000 # in KG
        pump_ON = True

        # Calling the pump function
        pump = HydraulicPump(            
            oil_type, 
            motor_speed, 
            operating_pressure, 
            mass, efficiency
            )

        density, viscosity, bulk_modulus = pump.getOil()
        flow_rate, pump_pressure = pump.simulate(pump_ON)
        
        # calling the direction control valve function
        dcv = DirectionControlValve(
            density, 
            viscosity, 
            pump_pressure, 
            flow_rate
        )

        port = dcv.simulate(self.left_solenoid_sig, self.right_solenoid_sig)
        
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
            timer, 
            port,
            self.time_value, # from global variable at top
            self.stroke_position, # determines the current positon
            self.signal_flag_dac_bp_ext,
            self.signal_flag_dac_bp_ret, 
            self.last_stroke_position
        )
        self.initialization_values(time_counter, event_time)

        displacement, q, f_extension, v_extension, power_input, power_output = hs.simulate
                    
        dataMqtt = ",".join(map(str,[
            hs.simulate
        ]))
        print("Dexompression data----> ", dataMqtt)
        # topic, payload, qos, retain, hostname, port, client_id, keepalive, will, authentication, tls
        # publish.single("DecompressionValve", payload=dataMqtt, qos=0, retain=False, hostname="202.144.139.110",
        #         port=1883, client_id="", keepalive=45, will=None, auth=None, tls=None)
        
        self.stroke_position = displacement

        # update the time
        self.system_time_defination()

