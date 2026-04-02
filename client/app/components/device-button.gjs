import Component from '@glimmer/component';
import { on } from '@ember/modifier';
import { fn } from '@ember/helper';

export default class DeviceButton extends Component {
  <template>
    <div>
      <button type="button"
          {{on "click" (fn @send_device_action @device_uuid @device this.args.data.action)}}>
        {{@data.label}}
      </button>
    </div>
  </template>
}
