from nicegui import ui

from brijsim.devices.device import Device
from brijsim.flow_sim import FlowPort


def device_view(device: Device):
    with ui.expansion(device.name, value=True):
        with ui.row().classes("justify-between w-full"):
            ui.label("State")
            ui.label().bind_text_from(device, "state")

        for flow_port_name, flow_port in device.flow_ports.items():
            with ui.row().classes("justify-between w-full"):
                with ui.column():
                    ui.label(flow_port_name)
                with ui.column().classes("gap-1"):
                    flow_info_bar(
                        flow_port, "rate_fraction", "rate_info", "rate_capacity"
                    )
                    flow_info_bar(flow_port, "qty_fraction", "qty_info", "qty_capacity")

        with ui.row():
            for action_name, action in device.actions.items():
                ui.button(
                    action_name,
                    on_click=lambda evt, action=action, element=device: action(element),
                )


def flow_info_bar(flow_port: FlowPort, attr: str, text: str, capacity: str):
    with (
        ui.linear_progress(show_value=False, size="1.2em")
        .bind_value_from(flow_port, attr)
        .classes("w-32")
    ):
        ui.label().bind_text_from(flow_port, text).classes(
            "text-black text-xs w-32 absolute flex flex-center"
        )

        ui.label().bind_text_from(
            flow_port, capacity, backward=lambda x: flow_info_bar_direction(x)
        ).classes("text-black text-xs w-32 absolute flex flex-left")


def flow_info_bar_direction(capacity: float) -> str:
    if capacity > 0:
        return "▲"
    elif capacity < 0:
        return "▼"
    else:
        return ""
