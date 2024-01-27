class DirectionControlValve:
    def __init__(
            self,
            control_signal,
            density,
            viscosity,
            liquid_pressure,

            ):
        self.control_signal = control_signal
        
        if(control_signal == 1):
            # Open the valve
            self.flow_rate = (density * viscosity) / (2 * liquid_pressure)
        else:
            # Close the valve
            self.flow_rate = 0.0
            
        