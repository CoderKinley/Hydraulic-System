import numpy as np

class HydraulicOil:
    def __init__(self, fluid_type):
        self.fluid_type = fluid_type
        self.fluid_properties = self.get_fluid_properties()

    def get_fluid_properties(self):
        if self.fluid_type == "skydrol_1":
            return self.skydrol_1()
        elif self.fluid_type == "skydrol_2":
            return self.skydrol_2()
        elif self.fluid_type == "skydrol_3":
            return self.skydrol_3()
        else:
            raise ValueError(f"Invalid fluid type: {self.fluid_type}")

    def skydrol_1(self):
        FLUID_DENSITY = 961.8  # [kg/m^3]
        VISCOSITY = 7.129    # [Pa*s]
        BULK_MODULUS = 1.24e+09  # [Pa]

        return FLUID_DENSITY, VISCOSITY, BULK_MODULUS

    def skydrol_2(self):
        FLUID_DENSITY = 1016.6  # [kg/m^3]
        VISCOSITY = 6.951    # [Pa*s]
        BULK_MODULUS = 1.33186e+09  # [Pa]

        return FLUID_DENSITY, VISCOSITY, BULK_MODULUS

    def skydrol_3(self):
        FLUID_DENSITY = 945.754  # [kg/m^3]
        VISCOSITY = 5.65406    # [Pa*s]
        BULK_MODULUS = 1.17931e+09  # [Pa]

        return FLUID_DENSITY, VISCOSITY, BULK_MODULUS

class HydraulicPump:
    def __init__(
            self,
            pump_type,
            motor_speed,
            operating_pressure,
            load_mass,
            pump_efficiency_factor
            ):
    
        self.operating_pressure = operating_pressure
        self.pump_type = pump_type
        self.motor_speed = motor_speed
        self.load_mass = load_mass
        self.pump_efficiency_factor = pump_efficiency_factor

        self.acceleration_gravity = 9.81 # m/s2'
        self.density, self.viscosity, self.bulk_modulus = HydraulicOil(pump_type).fluid_properties

    def simulate(self, on_signal):
        if (on_signal):
            flow_rate = self.flow_rate()
            pressure_out = self.operating_pressure
            
            return flow_rate, pressure_out

        elif (not on_signal):
            flow_rate = 0
            pressure_out = 0
            
            return flow_rate, pressure_out
        
        else:
            print("error in signal")


    def getOil(self):
        print("hydraulic pump oil function")

        return self.density, self.viscosity, self.bulk_modulus
    
    def volume_displacement(
            self, 
            gear_outer_dia, 
            gear_inner_dia, 
            width
            ):
        
        vdisp = np.pi * width * (np.square(gear_outer_dia) - np.square(gear_inner_dia)) / 4

        return vdisp
    
    def flow_rate(self):
        gear_outer_dia = 125/1000 # in meters
        gear_inner_dia = 85/1000 # in meters
        width = 40/1000 # in meters 
        flow_rate = self.volume_displacement(gear_outer_dia, gear_inner_dia, width) * self.motor_speed # m3/min
        theoratical_flow_rate = flow_rate * 1000 # converted to lpm
        actual_flow_rate = theoratical_flow_rate * self.pump_efficiency_factor

        return  actual_flow_rate

    # acceleration of the pistion retraction or extensdion can be calcularted
    # def acceleration(self, mass):
    #     # using the newton second law of motion
    #     force = mass * self.acceleration_gravity

    #     return force
    
    def required_force(self, area):
        # uses commonly in fluid mechanics
        force = area * self.operating_pressure
        return force

def main():
    # required system pressure in the Tala hydro power project
    operating_pressure = 7845320 # in pascals
    speed = 3000
    efficiency = 0.85
    mass =  50000 # in KG
    op = HydraulicPump("skydrol_1", speed, operating_pressure, mass, efficiency)
    op.getOil()
    print(str(op.flow_rate()) + " lpm")
    print(str(op.required_force(0.1)) + " Newtons")


if __name__ == "__main__":
    main()