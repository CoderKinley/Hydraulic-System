class DirectionControlValve:
    def __init__(
            self,
            density,
            viscosity,
            pressure,
            flow_rate,

            ):
        
        self.density = density
        self.viscosity = viscosity
        self.pressure = pressure
        self.flow_rate = flow_rate


    def simulate(
            self, 
            left_solenoid_signal, 
            right_solenoid_signal
            ):
        
        if (left_solenoid_signal == 1 and right_solenoid_signal == 0):
            self.extension()

        elif (left_solenoid_signal == 0 and right_solenoid_signal == 1):
            self.retraction()

        elif (left_solenoid_signal == right_solenoid_signal):
            print("both signal can't be high")        

        else:
            print("invalid signal")    
        
    def extension(self):
        print("extending")
        port_a = {"flow_rate" : self.flow_rate, "pressure" : self.pressure} 
        port_b = {"flow_rate" : 0, "pressure" : 0}

        return port_a, port_b

    def retraction(self): 
        print("retracting")
        port_a= {"flow_rate" : 0, "pressure" : 0}
        port_b = {"flow_rate" : self.flow_rate, "pressure" : self.pressure}
            
        return port_a, port_b