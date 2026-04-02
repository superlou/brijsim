import { module, test } from 'qunit';
import { setupRenderingTest } from 'client/tests/helpers';
import { render } from '@ember/test-helpers';
import DeviceDetail from 'client/components/device-detail';

module('Integration | Component | device-detail', function (hooks) {
  setupRenderingTest(hooks);

  test('it renders', async function (assert) {
    // Updating values is achieved using autotracking, just like in app code. For example:
    // class State { @tracked myProperty = 0; }; const state = new State();
    // and update using state.myProperty = 1; await rerender();
    // Handle any actions with function myAction(val) { ... };

    await render(<template><DeviceDetail /></template>);

    assert.dom().hasText('');

    // Template block usage:
    await render(<template>
      <DeviceDetail>
        template block text
      </DeviceDetail>
    </template>);

    assert.dom().hasText('template block text');
  });
});
