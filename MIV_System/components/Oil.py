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
