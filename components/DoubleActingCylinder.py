import numpy as np

class HydarulicActuator:
    def __init__(
            self, 
            bore_diameter, 
            rod_diameter,
            stroke_length,
            initial_position,
            simulation_time,
            operating_pressure,
            oil_flow_pressure,
            flow_rate,
            packingFriction,
            time_instant,
            port,
            event_time_instant,
            current_stroke_position,
            signal_flag_ext,
            signal_flag_ret,
            last_stroke_position
            ):
        
        self.bore_diameter = bore_diameter
        self.rod_diameter = rod_diameter
        self.stroke_length = stroke_length
        self.initial_position = initial_position
        self.simulation_time = simulation_time
        self.operating_pressure = operating_pressure
        self.oil_flow_pressure = oil_flow_pressure
        self.flow_rate = flow_rate
        self.packingFriction = packingFriction
        self.time_instant = time_instant
        self.event_time_instant = event_time_instant
        self.current_stroke_position = current_stroke_position
        self.signal_flag_ext = signal_flag_ext
        self.last_stroke_position = last_stroke_position
        self.signal_flag_ret = signal_flag_ret
        self.position_data = {}
        self.simulate = self.simulate(port)

    def simulate(self, port):
        # deconstruct and logic for the working of the double acting cylidner
        port_a_flow = port[0].get("flow_rate")
        port_a_pressure = port[0].get("pressure")
        port_b_flow = port[1].get("flow_rate")
        port_b_pressure = port[1].get("pressure")

        if(port_a_flow > port_b_flow and port_a_pressure > port_b_pressure):
            q = self.massFlowRateExt()
            f_extension = self.extensionForce()
            v_extension = self.pistonVelocityExt()
            power_input = self.powerInputExt()
            power_output= self.powerOutputExt()
            displacement = self.displacementExt(self.event_time_instant)

            if (displacement > self.stroke_length):
                displacement = self.stroke_length
            return displacement, q, f_extension, v_extension, power_input, power_output
        
        elif(port_a_flow < port_b_flow and port_a_pressure < port_b_pressure):
            q = self.massFlowRateExt()
            f_retraction = self.retractionForce()
            v_retraction = self.pistonVelocityRet()
            power_input = self.powerInputRet()
            power_output = self.powerOutputRet()
            displacement = self.displacementRet(self.event_time_instant)
            
            if (displacement < 0):
                displacement  = 0
            return displacement, q, f_retraction, v_retraction, power_input, power_output        
            
    def extensionForce(self):
        force_extension = self.operating_pressure *(np.pi * pow(self.bore_diameter/2, 2)) #in newtons
        return force_extension

    def massFlowRateExt(self):
         # massflow rate (m) = PAV
        mass_flow_rate = self.oil_flow_pressure * self.flow_rate
        # print("Massflr = " + str(mass_flow_rate) + " kg/s")
        return mass_flow_rate

    # important function to determine the postion of the extension  piston in meters
    def pistonVelocityExt(self):
        if (self.signal_flag_ext):
        # velocity = self.stroke_length / self.simulation_time #just calculating
            velocity = self.flow_rate / (np.pi * (pow(self.bore_diameter/2, 2)))
            return velocity
        else:
            return 0

    def powerInputExt(self):
        power_in = self.operating_pressure * self.flow_rate
        return power_in
        
    def powerOutputExt(self):
        #  after considerring packing friction
        forecenet = self.operating_pressure * (np.pi * pow(self.bore_diameter/2,2 )) - self.packingFriction
        p_out = forecenet * self.pistonVelocityExt()
        return p_out

    def pistonEfficiencyExt(self):
        efficiency = self.powerOutputExt() / self.powerInputExt()
        return efficiency
        
    def pistonAccelerationExt(self):
        acceleration = self.pistonVelocityExt() / self.simulation_time
        return acceleration

    def retractionForce(self):
        force_retraction = self.operating_pressure * (np.pi*(pow(self.bore_diameter/2, 2) - pow(self.rod_diameter/2, 2)))
        # print("retraction force = "+ str(force_retraction)+" N")
        return force_retraction

    # important  function as it defines the postion of the piston head during the retraction  
    def pistonVelocityRet(self):
        if (self.signal_flag_ret):
            velocity = self.flow_rate / ((np.pi * pow(self.bore_diameter/2, 2))-(np.pi * pow(self.rod_diameter/2, 2))) # m/s
            # print("return velocity ---------->", velocity)
            return velocity
        else:
            return 0
    def powerInputRet(self):
        power_in = self.operating_pressure * self.flow_rate
        return power_in
        
    def powerOutputRet(self):
        netForce = (self.operating_pressure * ((np.pi*pow(self.bore_diameter/2,2))-(np.pi * pow(self.rod_diameter/2,2)))) - self.packingFriction
        power_out = netForce * self.pistonVelocityRet()
        return power_out

    def pistonEfficiencyRet(self): 
        eff = self.powerOutputRet()/ self.powerInputRet()
        return eff
        
    # calculating the position of th top of the pistion during the extension phase
    def displacementExt(self, time_instant):
        position = self.current_stroke_position
        print("position ---> ", position)
        if ( position >= 0 and position < self.stroke_length):
            if (self.signal_flag_ext):
                disp = self.last_stroke_position + (self.pistonEfficiencyExt() * time_instant)
            else:
                disp = self.pistonVelocityExt() * time_instant
            return disp
        
        elif (position >= self.stroke_length):
            disp = self.stroke_length
            return disp
            
    def displacementRet(self, time_instant):
        if (self.current_stroke_position <= 0):
            # print("im hre")
            disp = 0
            return disp

        elif(self.current_stroke_position > 0):
            # print("im here")
            if (self.signal_flag_ret and self.current_stroke_position < self.stroke_length):
                disp = self.last_stroke_position - (self.pistonVelocityRet() * time_instant)
            else:
                disp = self.stroke_length - (self.pistonVelocityRet() * time_instant)
            # print("disp--->", disp)
            return disp
