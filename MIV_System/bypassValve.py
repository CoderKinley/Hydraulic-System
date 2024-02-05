from MIV_System.components.Pump import HydraulicPump
from MIV_System.components.DirectionControlValve import DirectionControlValve
from MIV_System.components.DoubleActingCylinder import HydarulicActuator

class BypassValve:
    def  __init__(
        self, 
        event_time,
        stroke_position,
        signal_flag_dac_bp_ext,
        signal_flag_dac_bp_ret, 
        last_stroke_position,
        time_counter,
        left_solenoid_sig,
        right_solenoid_sig
    ):
        self.event_time = event_time
        self.stroke_position =  stroke_position
        self.signal_flag_dac_bp_ext = signal_flag_dac_bp_ext
        self.signal_flag_dac_bp_ret = signal_flag_dac_bp_ret
        self.last_stroke_position = last_stroke_position
        self.time_counter = time_counter
        self.left_solenoid_sig = left_solenoid_sig
        self.right_solenoid_sig = right_solenoid_sig
        
    def run(self):
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
            self.event_time, # from global variable at top
            self.stroke_position, # determines the current positon
            self.signal_flag_dac_bp_ext,
            self.signal_flag_dac_bp_ret, 
            self.last_stroke_position
        )
        return hs.simulate
    