from nicegui import ui

from brijsim.devices.device import Device


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
                    flow_info_bar(flow_port, "rate_fraction", "rate_info")
                    flow_info_bar(flow_port, "qty_fraction", "qty_info")

        with ui.row():
            for action_name, action in device.actions.items():
                ui.button(
                    action_name,
                    on_click=lambda evt, action=action, element=device: action(element),
                )


def flow_info_bar(flow_port, attr, text):
    with (
        ui.linear_progress(show_value=False, size="1.2em")
        .bind_value_from(flow_port, attr)
        .classes("w-32")
    ):
        ui.label().bind_text_from(flow_port, text).classes(
            "text-black text-xs w-32 absolute flex flex-center"
        )
