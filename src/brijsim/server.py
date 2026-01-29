import asyncio
import threading

import networkx_mermaid
import websockets
from loguru import logger
from nicegui import Event, app, ui
from websockets import ServerConnection

from brijsim.device_view import device_view
from brijsim.devices.computer import JumpComputer
from brijsim.devices.generator import AuxGenerator, FusionGenerator
from brijsim.devices.hatch import Hatch
from brijsim.devices.tanks import FuelTank
from brijsim.region import Region
from brijsim.ship import Ship
from brijsim.ship.room import Room
from brijsim.ship.ship_loader import ShipLoader
from brijsim.ship_view import ship_view

from .pydot import SceneTree

connections: set[ServerConnection] = set()
connections_updated = Event()
messaged_received = Event()


@app.on_startup
async def start_websocket_server():
    async with websockets.serve(handle_connect, "localhost", 8765):
        await asyncio.Future()


async def handle_connect(websocket: ServerConnection):
    try:
        connections.add(websocket)
        connections_updated.emit()

        while True:
            await websocket.send("test")
            await asyncio.sleep(1.0)

        async for message in websocket:
            messaged_received.emit(str(message))
    finally:
        connections.remove(websocket)
        connections_updated.emit()


ship = ShipLoader().load("assets/ships/demo_ship.yaml")
tree = SceneTree()
tree.add_child(ship)


@ui.page("/")
def root():
    ui.page_title("Index")

    dark = ui.dark_mode(True)

    with ui.header().classes("dark:bg-gray-800"):
        ui.switch("Dark").bind_value(dark).bind_text_from(
            dark, "value", lambda x: "dark" if x else "light"
        )

    ui.label("Index")

    devices = [device for room in ship.rooms for device in room.devices] + ship.devices

    with ui.grid(columns=4):
        for device in devices:
            with ui.list().props("bordered"):
                device_view(device)

    ship_view(ship)

    builder = networkx_mermaid.builders.DiagramBuilder(
        orientation=networkx_mermaid.DiagramOrientation.LEFT_RIGHT,
        node_shape=networkx_mermaid.DiagramNodeShape.ROUND_RECTANGLE,
    )
    ui.mermaid(builder.build(ship.flow_model.graph))


class RepeatTimer(threading.Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


def main(reload=False):
    logger.info(f"Starting nicegui, reload={reload}")
    RepeatTimer(0.1, lambda: tree.process(0.1)).start()
    ui.run(reload=reload, uvicorn_reload_includes="*.py,*.yaml")


if __name__ in {"__main__", "__mp_main__"}:
    main(True)


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Websocket Test</title>
    </head>
    <body>
        <h1>WebSocket Test</h1>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8765");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
        </script>
    </body>
</html>
"""


@ui.page("/websocket_test")
def websocket_test():
    return ui.add_body_html(html)
