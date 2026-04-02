import Route from '@ember/routing/route';
import { service } from '@ember/service';

export default class EngPanelRoute extends Route {
  @service ServerConnection;

  model() {
    this.ServerConnection.connect();
    return {};
  }
}
