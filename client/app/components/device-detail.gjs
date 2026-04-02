import DeviceWidget from './device-widget';

<template>
  <div class="device-detail">
    <div class="header">
      <div class="title">{{@name}}</div>
      <button type="button">X</button>
    </div>

    <div class="widgets">
      {{#each @widgets as |widget|}}
        <DeviceWidget @device={{@name}}
                      @device_uuid={{@uuid}}
                      @component_name={{widget.component}}
                      @data={{widget.data}}
                      @send_device_action={{@send_device_action}} />
      {{/each}}
    </div>
  </div>
</template>
