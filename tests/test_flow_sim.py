from pytest import approx

from brijsim import FlowModel
from brijsim.flow_sim import FlowPort


def test_model_creation():
    model = FlowModel()
    model.add_port(FlowPort(100.0, 0.0))


def test_run_model_without_capacitance():
    model = FlowModel()
    p1 = model.add_port(FlowPort(10, 0))
    p2 = model.add_port(FlowPort(5, 0))
    p3 = model.add_port(FlowPort(-4, 0))
    p4 = model.add_port(FlowPort(-2, 0))

    model.step(0.1)

    # 6 W of demand and 15 of supply, so actual power
    # of both sinks should match their capacity.
    # The 6 W of demand should be source proportionally
    # from the ports with postiive capacity.
    assert p1.rate == approx(4)
    assert p2.rate == approx(2)
    assert p3.rate == approx(-4)
    assert p4.rate == approx(-2)

    # Reduce the power capacity of the sources and run again
    p1.rate_capacity = 2
    p2.rate_capacity = 2
    model.step(0.1)

    # Now, the sources actual power output should match capacity,
    # but the sinks should get power based on the ratio of demand.
    assert p1.rate == approx(2)
    assert p2.rate == approx(2)
    assert p3.rate == approx(-2.66666666)
    assert p4.rate == approx(-1.33333333)
