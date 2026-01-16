from dataclasses import dataclass
from math import isclose


@dataclass
class FlowPort:
    rate_capacity: float
    qty_capacity: float
    qty_max_charge_rate: float = 0
    qty_max_discharge_rate: float = 0
    rate: float = 0
    qty: float = 0
    rate_unit: str = "W"
    qty_unit: str = "J"

    def at_p_capacity(self):
        return isclose(self.rate, self.rate_capacity)

    @property
    def flow_info(self):
        return (
            f"{self.rate:.0f}:{self.rate_capacity:.0f} {self.rate_unit}, "
            f"{self.qty:.0f}:{self.qty_capacity:.0f} {self.qty_unit}"
        )


class FlowModel:
    def __init__(self):
        self.ports: list[FlowPort] = []
        # todo Model ports in different connected graphs

    def add_port(self, port: FlowPort):
        self.ports.append(port)
        return port

    def step(self, dt: float):
        # For all connected ports, distribute as much power
        # proportionally from sources to sinks.
        sources = [port for port in self.ports if port.rate_capacity > 0]
        sinks = [port for port in self.ports if port.rate_capacity < 0]
        zeros = [port for port in self.ports if port.rate_capacity == 0]

        source_p = sum(port.rate_capacity for port in sources)
        sink_p = sum(port.rate_capacity for port in sinks)

        if source_p + sink_p >= 0:
            for sink in sinks:
                sink.rate = sink.rate_capacity

            for source in sources:
                source.rate = -sink_p * source.rate_capacity / source_p
        else:
            for source in sources:
                source.rate = source.rate_capacity

            for sink in sinks:
                sink.rate = -source_p * sink.rate_capacity / sink_p

        for port in zeros:
            port.rate = 0.0
