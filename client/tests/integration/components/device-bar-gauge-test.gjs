import { module, test } from 'qunit';
import { setupRenderingTest } from 'client/tests/helpers';
import { render } from '@ember/test-helpers';
import DeviceBarGauge from 'client/components/device-bar-gauge';

module('Integration | Component | device-bar-gauge', function (hooks) {
  setupRenderingTest(hooks);

  test('it renders', async function (assert) {
    // Updating values is achieved using autotracking, just like in app code. For example:
    // class State { @tracked myProperty = 0; }; const state = new State();
    // and update using state.myProperty = 1; await rerender();
    // Handle any actions with function myAction(val) { ... };

    await render(<template><DeviceBarGauge /></template>);

    assert.dom().hasText('');

    // Template block usage:
    await render(<template>
      <DeviceBarGauge>
        template block text
      </DeviceBarGauge>
    </template>);

    assert.dom().hasText('template block text');
  });
});
