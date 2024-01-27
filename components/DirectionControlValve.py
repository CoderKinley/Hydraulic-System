class DirectionControlValve:
    def __init__(
            self,
            control_signal,
            density,
            viscosity,
            ):
        self.control_signal = control_signal
        self.density = density
        self.viscosity = viscosity

    def simulation(self):
        print("Directional control valve")
        return self.control_signal