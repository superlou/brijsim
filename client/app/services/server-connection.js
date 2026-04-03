import Service from '@ember/service';
import { tracked } from '@glimmer/tracking';
import { trackedObject, trackedArray } from '@ember/reactive/collections';

class Device {
  @tracked name;
  @tracked type;
  @tracked uuid;
  widgets = trackedArray([]);
}

class Widget {
  @tracked component;
  data = trackedObject({});
}

class GameState {
  devices = trackedArray([]);
}

export default class ServerConnectionService extends Service {
  server_uri = 'ws://127.0.0.1:8765';
  websocket = null;
  // devices = trackedArray([]);
  @tracked game_state = new GameState();
  @tracked connected = false;

  on_open = () => {
    this.connected = true;
    console.log(`Connected to server ${this.websocket.url}`);
  };

  on_close = () => {
    this.connected = false;
    console.log(`Server connection closed`);

    setTimeout(() => {
      this.connect();
    }, 1000);
  };

  send_device_action = (device_uuid, device_name, action) => {
    if (!this.connected) {
      console.log(
        `Disconnected. Unable to send action: ${device_name}, ${action}`
      );
      return;
    }

    this.websocket.send(
      JSON.stringify({
        type: 'device-action',
        data: {
          device_uuid: device_uuid,
          device: device_name,
          action: action,
        },
      })
    );
  };

  on_message = (e) => {
    const msg = JSON.parse(e.data);

    if (msg.type === 'devices') {
      this.on_msg_devices(msg.data);
    }
  };

  on_msg_devices = (data) => {
    let devices = this.game_state.devices;
    for (let device of devices) {
      device.seen = false;
    }

    // todo Filter out unseen widgets
    for (const d of data) {
      let device = devices.find((device) => device.uuid === d.device_uuid);
      if (!device) {
        device = new Device();
        devices.push(device);
      }

      device.uuid = d.device_uuid;
      device.name = d.name;
      device.type = d.type;
      device.seen = true;

      for (const w of d.widgets) {
        let widget = device.widgets.find(
          (widget) => widget.data.label === w.data.label
        );
        if (!widget) {
          widget = new Widget();
          device.widgets.push(widget);
        }
        widget.component = w.component;
        Object.assign(widget.data, w.data);
      }
    }

    // Remove unseen devices in place
    for (let i = devices.length - 1; i >= 0; i--) {
      if (!devices[i].seen) {
        devices.splice(i, 1);
      }
    }
  };

  connect() {
    this.websocket = new WebSocket(this.server_uri);
    this.websocket.addEventListener('open', this.on_open);
    this.websocket.addEventListener('close', this.on_close);
    this.websocket.addEventListener('message', this.on_message);
  }
}
