from dataclasses import dataclass
from math import isclose

import networkx as nx


@dataclass
class FlowPort:
    rate_capacity: float
    qty_capacity: float
    rate: float = 0.0
    qty: float = 0.0
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

    @property
    def qty_open(self) -> float:
        return self.qty_capacity - self.qty


class FlowModel:
    def __init__(self):
        self.graph = nx.Graph()
        # todo Model ports in different connected graphs

    def add_port(self, id: str, port: FlowPort):
        self.graph.add_node(id, port=port)
        return port

    def link_ports(self, port1: str, port2: str):
        if not self.graph.has_node(port1):
            raise KeyError(f"Node {port1} not found while linking ports.")

        if not self.graph.has_node(port2):
            raise KeyError(f"Node {port2} not found while linking ports.")

        self.link_ports_by_id(port1, port2)

    def link_ports_by_id(self, id1: str, id2: str):
        self.graph.add_edge(id1, id2)

    def step(self, dt: float):
        for connected_nodes in nx.connected_components(self.graph):
            self.solve_connected_components(
                [self.graph.nodes[node]["port"] for node in connected_nodes], dt
            )

    def solve_connected_components(self, ports: list[FlowPort], dt: float):
        # Reset all ports
        for storage_sources in ports:
            storage_sources.rate = 0.0

        sources = [port for port in ports if port.rate_capacity > 0.0]
        sinks = [port for port in ports if port.rate_capacity < 0.0]
        source_capacity = sum(port.rate_capacity for port in sources)
        sink_demand = -sum(port.rate_capacity for port in sinks)

        storage_sources = [port for port in ports if port.qty > 0.0]
        storage_sinks = [port for port in ports if port.qty_open > 0.0]
        storage_source_capacity = sum(port.qty * dt for port in storage_sources)
        storage_source_qty = sum(port.qty for port in storage_sources)
        storage_sink_qty_open = sum(port.qty_open for port in storage_sinks)

        if source_capacity >= sink_demand:
            sink_supply = min(source_capacity, sink_demand)
            source_excess = source_capacity - sink_supply

            # All sink rates are met
            for sink in sinks:
                sink.rate = sink.rate_capacity

            # No storage was discharged, but some could be charged
            # Divide the excess proportionally to quantity open
            storage_supply = min(source_excess, storage_sink_qty_open)
            for storage_sink in storage_sinks:
                storage_sink.rate = (
                    -storage_supply * storage_sink.qty_open / storage_sink_qty_open
                )
                storage_sink.qty += -storage_sink.rate * dt

            # Supply is divided proportionally to capacity:
            supply = sink_supply + storage_supply
            for source in sources:
                source.rate = supply * source.rate_capacity / source_capacity
        elif (source_capacity + storage_source_capacity) >= sink_demand:
            # All sink rates are met
            for sink in sinks:
                sink.rate = sink.rate_capacity

            # All source rates are met
            for source in sources:
                source.rate = source.rate_capacity

            # Some (or all) storage was discharged based on what's left
            # after the sources hit capacity.
            storage_supply = sink_demand - source_capacity
            for storage_source in storage_sources:
                storage_source.rate = (
                    storage_supply * storage_source.qty / storage_source_qty
                )
                storage_source.qty -= storage_source.rate * dt
        else:  # Insufficient capacity, even with sources
            supply = source_capacity + storage_source_capacity

            # All sources are at capacity
            for source in sources:
                source.rate = source.rate_capacity

            # All storage is emptied
            for storage_sources in storage_sources:
                storage_sources.rate = -storage_sources.qty * dt
                storage_sources.qty = 0.0

            # Supply is divided proportionally to capacity
            for sink in sinks:
                sink.rate = supply * sink.rate_capacity / sink_demand
