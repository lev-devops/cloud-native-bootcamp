import test from 'node:test';
import assert from 'node:assert/strict';
import {server} from './server.js';
test('health endpoint is available', async () => {
  if (!server.listening) await new Promise(resolve => server.once('listening', resolve));
  const response = await fetch(`http://127.0.0.1:${server.address().port}/healthz`);
  assert.equal(response.status, 200); assert.deepEqual(await response.json(), {status: 'ok'}); server.close();
  server.closeIdleConnections();
});
