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
        fluid_density = 961.8  # [kg/m^3]
        viscosity = 7.129    # [Pa*s]
        bulk_modulus = 1.24e+09  # [Pa]
        return fluid_density, viscosity, bulk_modulus

    def skydrol_2(self):
        fluid_density = 1016.6  # [kg/m^3]
        viscosity = 6.951    # [Pa*s]
        bulk_modulus = 1.33186e+09  # [Pa]
        return fluid_density, viscosity, bulk_modulus

    def skydrol_3(self):
        fluid_density = 945.754  # [kg/m^3]
        viscosity = 5.65406    # [Pa*s]
        bulk_modulus = 1.17931e+09  # [Pa]
        return fluid_density, viscosity, bulk_modulus

class HydraulicPump:
    def __init__(
            self,
            pump_type,
            motor_speed,
            ):
    
        self.pump_type = pump_type
        self.motor_speed = motor_speed

        self.density, 
        self.viscosity, 
        self.bulk_modulus = HydraulicOil(pump_type).fluid_properties

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

        flow_rate = self.volume_displacement(gear_outer_dia, gear_inner_dia, width) * self.motor_speed

        return flow_rate, flow_rate/self.motor_speed



def main():
    speed = 1500
    op = HydraulicPump("skydrol_1", speed)
    op.getOil()
    print(op.flow_rate())


if __name__ == "__main__":
    main()