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
            ):
    
        self.pump_type = pump_type
        self.motor_speed = motor_speed
        self.acceleration_gravity = 9.81 # m/s2

        self.density, self.viscosity, self.bulk_modulus = HydraulicOil(pump_type).fluid_properties

    def getOil(self):
        print("hydraulic pump")
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
        flow_rate_lpm = flow_rate * 1000 # converted to lpm

        return flow_rate_lpm

    def force(self, mass):
        force = mass * self.acceleration_gravity
        
        return force
    
    def pressure(self, area):
        mass = 1000
        pressure = self.force(mass)/ area

        return pressure

def main():
    speed = 3000
    op = HydraulicPump("skydrol_1", speed)
    op.getOil()
    print(str(op.flow_rate()) + " lpm")
    print(op.pressure(0.094))


if __name__ == "__main__":
    main()