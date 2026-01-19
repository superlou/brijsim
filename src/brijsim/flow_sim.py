from dataclasses import dataclass
from math import isclose

import networkx as nx


@dataclass
class FlowPort:
    rate_capacity: float
    qty_capacity: float
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

    @property
    def qty_open(self) -> float:
        return self.qty_capacity - self.qty


class FlowModel:
    def __init__(self):
        self.ports: list[FlowPort] = []
        self.graph = nx.Graph()
        # todo Model ports in different connected graphs

    def add_port(self, id: str, port: FlowPort):
        self.ports.append(port)
        self.graph.add_node(id, port=port)
        return port

    def link_ports(self, port1_id: str, port2_id: str):
        self.graph.add_edge(port1_id, port2_id)

    def step(self, dt: float):
        for connected_nodes in nx.connected_components(self.graph):
            self.solve_connected_components(
                [self.graph.nodes[node]["port"] for node in connected_nodes], dt
            )

    def solve_connected_components(self, ports: list[FlowPort], dt: float):
        # For all connected ports, distribute as much power
        # proportionally from sources to sinks.
        sources = [port for port in ports if port.rate_capacity > 0.0]
        sinks = [port for port in ports if port.rate_capacity < 0.0]
        inactives = [
            port
            for port in ports
            if port.rate_capacity == 0.0 and port.qty_capacity == 0.0
        ]

        stores = [port for port in ports if port.qty_capacity > 0.0]

        source_rate_capacity = sum(port.rate_capacity for port in sources)
        sink_rate_capacity = sum(port.rate_capacity for port in sinks)

        net_rate_capacity = source_rate_capacity + sink_rate_capacity

        if net_rate_capacity >= 0.0:
            for sink in sinks:
                sink.rate = sink.rate_capacity

            for source in sources:
                source.rate = (
                    -sink_rate_capacity * source.rate_capacity / source_rate_capacity
                )

            # Whatever's leftover is divided among stores based on how much
            # capacity remains.
            # todo This doesn't make a lot of sense physically.
            total_store_qty_open = sum([store.qty_open for store in stores])
            quantity_available = net_rate_capacity * dt
            if total_store_qty_open > 0.0:
                for store in stores:
                    store.qty += (
                        quantity_available * store.qty_open / total_store_qty_open
                    )
                    store.qty = min(store.qty, store.qty_capacity)
        else:
            total_store_qty_available = sum([store.qty for store in stores])
            needed_qty = -net_rate_capacity * dt
            store_provided_qty = min(needed_qty, total_store_qty_available)
            # Use stores
            for store in stores:
                if total_store_qty_available > 0:
                    store.qty -= needed_qty * store.qty / total_store_qty_available
                else:
                    store.qty = 0.0

            # All sources are maxed out
            for source in sources:
                source.rate = source.rate_capacity

            for sink in sinks:
                sink.rate = (
                    -(source_rate_capacity + store_provided_qty / dt)
                    * sink.rate_capacity
                    / sink_rate_capacity
                )

        for port in inactives:
            port.rate = 0.0
