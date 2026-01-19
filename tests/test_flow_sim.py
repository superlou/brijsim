from pytest import approx

from brijsim import FlowModel
from brijsim.flow_sim import FlowPort


def test_model_creation():
    model = FlowModel()
    model.add_port("p1", FlowPort(100.0, 0.0))


def test_run_model_without_quantity():
    model = FlowModel()
    p1 = model.add_port("p1", FlowPort(10, 0))
    p2 = model.add_port("p2", FlowPort(5, 0))
    p3 = model.add_port("p3", FlowPort(-4, 0))
    p4 = model.add_port("p4", FlowPort(-2, 0))

    model.link_ports("p1", "p2")
    model.link_ports("p1", "p3")
    model.link_ports("p1", "p4")

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


def test_run_model_with_quantity():
    model = FlowModel()
    r1 = model.add_port("r1", FlowPort(0, 0))
    r2 = model.add_port("r2", FlowPort(0, 0))
    q1 = model.add_port("q1", FlowPort(0, 10.0))
    q2 = model.add_port("q2", FlowPort(0, 10.0))

    model.link_ports("r1", "r2")
    model.link_ports("r1", "q1")
    model.link_ports("r1", "q2")

    # The rate ports have positive net capacity, so
    # the quantity ports increase.
    r1.rate_capacity = 10.0
    r2.rate_capacity = -5.0
    model.step(1.0)
    assert q1.qty == approx(2.5)
    assert q2.qty == approx(2.5)

    # The quantity ports should fill up completely
    model.step(100.0)
    assert q1.qty == approx(10.0)
    assert q2.qty == approx(10.0)

    # The positive rate port shuts off, so the quantity
    # ports should source.
    r1.rate_capacity = 0.0
    model.step(1.0)
    assert r2.rate == approx(-5.0)
    assert q1.qty == approx(7.5)
    assert q2.qty == approx(7.5)
    model.step(3.0)
    assert r2.rate == approx(-5.0)
    assert q1.qty == approx(0.0)
    assert q2.qty == approx(0.0)
    model.step(1.0)
    assert r2.rate == approx(0.0)
    assert q1.qty == approx(0.0)
    assert q2.qty == approx(0.0)
