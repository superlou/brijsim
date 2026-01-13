from dataclasses import dataclass


@dataclass
class Port:
    p_capacity: float
    e_capacity: float
    e_max_charge_rate: float = 0
    e_max_discharge_rate: float = 0
    p: float = 0  # Power in watts
    e: float = 0  # Energy in joules


class ElectricalEnergyModel:
    def __init__(self):
        self.ports: list[Port] = []
        # todo Model ports in different connected graphs

    def add_port(self, port: Port):
        self.ports.append(port)
        return port

    def step(self, dt: float):
        # For all connected ports, distribute as much power
        # proportionally from sources to sinks.
        sources = [port for port in self.ports if port.p_capacity > 0]
        sinks = [port for port in self.ports if port.p_capacity < 0]

        source_p = sum(port.p_capacity for port in sources)
        sink_p = sum(port.p_capacity for port in sinks)

        if source_p + sink_p >= 0:
            for sink in sinks:
                sink.p = sink.p_capacity

            for source in sources:
                source.p = -sink_p * source.p_capacity / source_p

        else:
            for source in sources:
                source.p = source.p_capacity

            for sink in sinks:
                sink.p = -source_p * sink.p_capacity / sink_p
