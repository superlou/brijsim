import { concat } from '@ember/helper';

<template>
  <div class="device-widget widget-labeled-string">
    <div>{{@data.label}}</div>
    <div class="value {{concat 'level-' @data.level}}">{{@data.value}}</div>
  </div>
</template>
