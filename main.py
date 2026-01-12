from brijsim.electrical_sim import ElectricalNetwork


def main():
    sim = ElectricalNetwork()
    sim.add_ind_voltage_source("V1", 1, 0, 5)
    sim.add_resistor("R1", 1, 2, 1_000)
    sim.add_resistor("R2", 2, 0, 2_000)
    sim.run()


if __name__ == "__main__":
    main()
