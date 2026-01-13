from pytest import approx

from brijsim import ElectricalEnergyModel
from brijsim.energy_sim import Port


def test_model_creation():
    model = ElectricalEnergyModel()
    model.add_port(Port(100.0, 0.0))


def test_run_model_without_capacitance():
    model = ElectricalEnergyModel()
    p1 = model.add_port(Port(10, 0))
    p2 = model.add_port(Port(5, 0))
    p3 = model.add_port(Port(-4, 0))
    p4 = model.add_port(Port(-2, 0))

    model.step(0.1)

    # 6 W of demand and 15 of supply, so actual power
    # of both sinks should match their capacity.
    # The 6 W of demand should be source proportionally
    # from the ports with postiive capacity.
    assert p1.p == approx(4)
    assert p2.p == approx(2)
    assert p3.p == approx(-4)
    assert p4.p == approx(-2)

    # Reduce the power capacity of the sources and run again
    p1.p_capacity = 2
    p2.p_capacity = 2
    model.step(0.1)

    # Now, the sources actual power output should match capacity,
    # but the sinks should get power based on the ratio of demand.
    assert p1.p == approx(2)
    assert p2.p == approx(2)
    assert p3.p == approx(-2.66666666)
    assert p4.p == approx(-1.33333333)
