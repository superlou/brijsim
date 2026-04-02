import { pageTitle } from 'ember-page-title';
import { LinkTo } from '@ember/routing';

<template>
  {{pageTitle "Index"}}
  <LinkTo @route="eng-panel">Engineering</LinkTo>
  {{outlet}}
</template>
