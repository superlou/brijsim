import asyncio
import threading

import networkx_mermaid
import websockets
from loguru import logger
from nicegui import Event, app, ui
from websockets import ServerConnection

from brijsim.body_3d import BoxShape3D, Vector3
from brijsim.device_view import device_view
from brijsim.devices.computer import JumpComputer
from brijsim.devices.generator import AuxGenerator, FusionGenerator
from brijsim.devices.hatch import Hatch
from brijsim.devices.tanks import FuelTank
from brijsim.region import Region
from brijsim.ship import Ship
from brijsim.ship.room import Room
from brijsim.ship_view import ship_view

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


region = Region()
ship = Ship()

ship.add_room("Hall1", Room(Vector3.ZERO, 1000, BoxShape3D(Vector3(20, 4, 3))))
storage1 = ship.add_room(
    "Storage1", Room(Vector3(0.0, 4, 0.0), 1000, BoxShape3D(Vector3(4, 4, 3)))
)
storage2 = ship.add_room(
    "Storage2", Room(Vector3(4, 4, 0.0), 1000, BoxShape3D(Vector3(4, 4, 3)))
)
engineering = ship.add_room(
    "Engine Room", Room(Vector3(-10, 0, 0), 4000, BoxShape3D(Vector3(10, 15, 3)))
)

ship.add_device(Hatch("S1S2Hatch", [storage1, storage2]))

engineering.add_device(AuxGenerator("AuxGen1", 100.0))
engineering.add_device(FusionGenerator("FusGen1"))
storage1.add_device(JumpComputer("JumpCom1"))
storage2.add_device(FuelTank("Tank1", 40000.0, 40000.0))

ship.link_ports("AuxGen1:src", "FusGen1:boost")
ship.link_ports("FusGen1:src", "JumpCom1:pwr")
ship.link_ports("AuxGen1:src", "JumpCom1:pwr")
ship.link_ports("Tank1:fuel", "AuxGen1:fuel")


@ui.page("/")
def root():
    ui.page_title("Index")

    dark = ui.dark_mode(True)

    with ui.header().classes("dark:bg-gray-800"):
        ui.switch("Dark").bind_value(dark).bind_text_from(
            dark, "value", lambda x: "dark" if x else "light"
        )

    ui.label("Index")

    devices = [
        device for room in ship.rooms.values() for device in room.devices
    ] + ship.devices

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
    RepeatTimer(0.1, lambda: ship.process(0.1)).start()
    ui.run(reload=reload)


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
