import asyncio
import threading

import websockets
from loguru import logger
from nicegui import Event, app, ui
from websockets import ServerConnection

from brijsim.elements.computer import JumpComputer
from brijsim.elements.generator import AuxGenerator, FusionGenerator
from brijsim.ship import Ship

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


ship = Ship()
ship.add_element(AuxGenerator("AuxGen1", 100.0))
ship.add_element(FusionGenerator("FusGen1"))
ship.add_element(JumpComputer("JumpCom1"))


@ui.page("/")
def root():
    ui.page_title("Index")
    ui.label("Index")

    with ui.grid(columns=3):
        for element in ship.elements:
            with ui.list().props("bordered"):
                with ui.expansion(element.name, value=True):
                    with ui.row():
                        ui.label("State")
                        ui.label().bind_text_from(element, "state")

                    for flow_port_name, flow_port in element.flow_ports.items():
                        with ui.row():
                            ui.label(flow_port_name)
                            ui.label().bind_text_from(
                                flow_port, "flow_info", backward=lambda text: text
                            )

                    with ui.row():
                        for action_name, action in element.actions.items():
                            ui.button(action_name, on_click=action)


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
