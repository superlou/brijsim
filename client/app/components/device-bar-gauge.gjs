import Component from '@glimmer/component';

function format_number(value) {
  return value.toFixed(0);
}

export default class CounterComponent extends Component {
  get percent() {
    return this.args.data.value / this.args.data.max * 100;
  }

  <template>
    <div class="device-widget widget-device-bar-gauge">
      <div>{{@data.label}}</div>
      <div class="value" style="--percent: {{this.percent}}%">
        {{format_number @data.value}} / {{format_number @data.max}}
      </div>
    </div>
  </template>
}
