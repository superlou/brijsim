import asyncio
import json

import websockets
from loguru import logger
from nicegui import Event
from websockets import ServerConnection

from brijsim.devices.device import Device
from brijsim.pydot.scene_tree import SceneTree

connections: set[ServerConnection] = set()
connections_updated = Event()
messaged_received = Event()


def device_details(device: Device) -> dict:
    actions = [
        {
            "component": "device-button",
            "data": {"label": action_name, "cmd": action_name},
        }
        for action_name, action in device.actions.items()
    ]

    if hasattr(device, "state"):
        state = {
            "component": "labeled-string",
            "data": {
                "label": "state",
                "value": device.state,
                "level": "normal",
            },
        }

    details = {"name": device.name, "widgets": [] + [state] + actions}

    return device.panel.to_dict()


async def state_sender(websocket, tree: SceneTree):
    while True:
        devices = tree.find_nodes_by_type(Device)

        try:
            await websocket.send(
                json.dumps(
                    {
                        "type": "devices",
                        "data": [device_details(device) for device in devices],
                        # "data": [
                        #     {
                        #         "name": "AuxGen1",
                        #         "type": "AuxGenerator",
                        #         "widgets": [
                        #             {
                        #                 "component": "labeled-string",
                        #                 "data": {
                        #                     "label": "state",
                        #                     "value": "off",
                        #                     "level": "normal",
                        #                 },
                        #             },
                        #             {
                        #                 "component": "device-bar-gauge",
                        #                 "data": {
                        #                     "label": "power",
                        #                     "value": 600,
                        #                     "max": 1000,
                        #                 },
                        #             },
                        #             {
                        #                 "component": "labeled-string",
                        #                 "data": {
                        #                     "label": "ready",
                        #                     "value": "true",
                        #                     "level": "normal",
                        #                 },
                        #             },
                        #         ],
                        #     },
                        # ],
                    }
                )
            )
            await asyncio.sleep(0.1)
        except websockets.ConnectionClosed:
            break
        except Exception as e:
            print(f"Exception in sender: {e}")
            break


async def handler(websocket: ServerConnection, tree: SceneTree):
    sender_task = asyncio.create_task(state_sender(websocket, tree))

    try:
        connections.add(websocket)
        logger.info(f"Added websocket connection: {websocket.id}")
        connections_updated.emit()

        async for message in websocket:
            messaged_received.emit(str(message))
    finally:
        connections.remove(websocket)
        sender_task.cancel()
        await sender_task
        logger.info(f"Removed websocket connection: {websocket.id}")
        connections_updated.emit()
