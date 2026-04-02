import Component from '@glimmer/component';

export default class CounterComponent extends Component {
  get percent() {
    return this.args.data.value / this.args.data.max * 100;
  }

  <template>
    <div class="device-widget widget-device-bar-gauge">
      <div>{{@data.label}}</div>
      <div class="value" style="--percent: {{this.percent}}%">{{@data.value}}</div>
    </div>
  </template>
}
