import asyncio
import json

from loguru import logger
from nicegui import Event
from websockets import ServerConnection

connections: set[ServerConnection] = set()
connections_updated = Event()
messaged_received = Event()


async def handle_connect(websocket: ServerConnection):
    try:
        connections.add(websocket)
        logger.info(f"Added websocket connection: {websocket.id}")
        connections_updated.emit()

        await websocket.send(
            json.dumps(
                {
                    "type": "devices",
                    "data": [
                        {
                            "name": "AuxGen1",
                            "type": "AuxGenerator",
                            "widgets": [
                                {
                                    "component": "labeled-string",
                                    "data": {
                                        "label": "state",
                                        "value": "off",
                                        "level": "normal",
                                    },
                                },
                                {
                                    "component": "device-bar-gauge",
                                    "data": {
                                        "label": "power",
                                        "value": 600,
                                        "max": 1000,
                                    },
                                },
                                {
                                    "component": "labeled-string",
                                    "data": {
                                        "label": "ready",
                                        "value": "true",
                                        "level": "normal",
                                    },
                                },
                                {
                                    "component": "device-button",
                                    "data": {
                                        "label": "activate",
                                        "command": "activate",
                                    },
                                },
                            ],
                        },
                    ],
                }
            )
        )

        # while True:
        #     await websocket.send("test")
        #     await asyncio.sleep(1.0)

        async for message in websocket:
            messaged_received.emit(str(message))
    finally:
        connections.remove(websocket)
        logger.info(f"Removed websocket connection: {websocket.id}")
        connections_updated.emit()
