import numpy as np

from brijsim.electrical_sim import ElectricalNetwork, Node, Resistor


def test_example1():
    # https://lpsa.swarthmore.edu/Systems/Electrical/mna/MNA3.html
    sim = ElectricalNetwork()
    sim.add_voltage_source("V1", 2, 1, 32.0)
    sim.add_voltage_source("V2", 3, 0, 20.0)
    sim.add_resistor("R1", 1, 0, 2.0)
    sim.add_resistor("R2", 2, 3, 4.0)
    sim.add_resistor("R3", 2, 0, 8.0)

    np.testing.assert_array_equal(
        sim.build_G(), np.array([[0.5, 0, 0], [0, 0.375, -0.25], [0, -0.25, 0.25]])
    )
    np.testing.assert_array_equal(sim.build_B(), np.array([[-1, 0], [1, 0], [0, 1]]))
    np.testing.assert_array_equal(sim.build_C(), np.array([[-1, 1, 0], [0, 0, 1]]))
    np.testing.assert_array_equal(sim.build_D(), np.zeros((2, 2)))

    sim.run()

    assert sim.nodes[0].voltage == 0
    assert sim.nodes[1].voltage == -8
    assert sim.nodes[2].voltage == -24
    assert sim.nodes[3].voltage == 20
    assert sim.ind_voltage_sources[0] == -4
    assert sim.ind_voltage_sources[1] == -1


def test_node_spanning_resistors():
    r12 = Resistor("R12", 10)
    r23a = Resistor("R23A", 10)
    r23b = Resistor("R23B", 10)
    r2 = Resistor("R2", 10)

    n1 = Node(1).link(r12, "p")
    n2 = Node(2).link(r12, "n").link(r23a, "p").link(r23b, "p").link(r2, "p")
    n3 = Node(3).link(r23a, "n").link(r23b, "n")

    assert {c.name for c in n1.spanning_components(n2)} == {"R12"}
    assert {c.name for c in n2.spanning_components(n1)} == {"R12"}

    assert {c.name for c in n2.spanning_components(n3)} == {"R23A", "R23B"}
    assert {c.name for c in n3.spanning_components(n2)} == {"R23A", "R23B"}
