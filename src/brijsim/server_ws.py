import asyncio
import json
import traceback

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
                    }
                )
            )
            await asyncio.sleep(0.025)
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
            message = json.loads(message)
            print(f"Received: {message}")
            messaged_received.emit(str(message))

            if message["type"] == "device-action":
                device_uuid = message["data"]["device_uuid"]
                action = message["data"]["action"]
                device = tree.node_uuid_map[device_uuid]
                device.actions[action](device)

    except Exception as _exc:
        traceback.print_exc()
    finally:
        connections.remove(websocket)
        sender_task.cancel()
        await sender_task
        logger.info(f"Removed websocket connection: {websocket.id}")
        connections_updated.emit()
