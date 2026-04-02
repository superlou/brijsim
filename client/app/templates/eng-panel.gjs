import { pageTitle } from 'ember-page-title';
import DeviceDetail from 'client/components/device-detail';
import { service } from '@ember/service';
import Component from '@glimmer/component';

export default class EngPanel extends Component {
  @service ServerConnection;

  <template>
    {{pageTitle "EngPanel"}}

    <div class="panel">
      <div class="device-map">
        {{this.ServerConnection.connected}}
      </div>

      <div class="device-details">
        {{#each this.ServerConnection.devices as |device| }}
          <DeviceDetail @name={{device.name}} @uuid={{device.uuid}} @widgets={{device.widgets}}
                        @send_device_action={{this.ServerConnection.send_device_action}} />
        {{/each}}
      </div>
    </div>
  </template>
}
