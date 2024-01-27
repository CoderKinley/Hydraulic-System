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
            time
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
        self.time = time
        self.position_data = {}
        self.max_position = 0
    
    def extensionForce(self):
        force_extension = self.operating_pressure *(np.pi * pow(self.bore_diameter/2, 2)) #in newtons
        return force_extension

    def massFlowRateExt(self):
         # massflow rate (m) = PAV
        mass_flow_rate = self.oil_flow_pressure * self.flow_rate
        print("Massflr = " + str(mass_flow_rate) + " kg/s")
        return mass_flow_rate
        
    def pistonVelocityExt(self):
        # velocity = self.stroke_length / self.simulation_time #just calculating
        velocity = self.flow_rate / (np.pi * (pow(self.bore_diameter/2, 2)))
        return velocity

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
        print("retraction force = "+ str(force_retraction)+" N")
        return force_retraction
        
    def pistonVelocityRet(self):
        velocity = self.flow_rate / ((np.pi * pow(self.bore_diameter/2, 2))-(np.pi * pow(self.rod_diameter/2, 2))) 
        return velocity
        
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
    def displacementExt(self, timeinstant):
        disp = self.pistonVelocityExt() * timeinstant
        return disp
    
    def displacementRet(self, time_instant):
        disp = self.pistonVelocityRet() * time_instant
        # print(disp)
        return disp