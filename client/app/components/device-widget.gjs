import Component from '@glimmer/component';
import DeviceButton from './device-button';
import LabeledString from './labeled-string';
import DeviceBarGauge from './device-bar-gauge';

export default class DeviceWidget extends Component {
  get component() {
    const widget_map = {
      "device-button": DeviceButton,
      "labeled-string": LabeledString,
      "device-bar-gauge": DeviceBarGauge,
    }
    return widget_map[this.args.component_name];
  }

  <template>
    <this.component @device={{@device}} @device_uuid={{@device_uuid}} @data={{@data}}
                    @send_device_action={{@send_device_action}} />
  </template>
}
