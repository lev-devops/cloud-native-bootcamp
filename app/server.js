import http from 'node:http';
const port = Number(process.env.PORT || 3000);
const version = process.env.APP_VERSION || 'dev';
const server = http.createServer((request, response) => {
  if (request.url === '/metrics') {
    response.writeHead(200, { 'content-type': 'text/plain; version=0.0.4' });
    response.end('# TYPE bootcamp_http_requests_total counter\nbootcamp_http_requests_total 1\n');
    return;
  }
  const payload = request.url === '/healthz' ? { status: 'ok' }
    : request.url === '/readyz' ? { status: 'ready' }
      : request.url === '/' ? { service: 'bootcamp-hello-service', version }
        : { error: 'not found' };
  response.writeHead(payload.error ? 404 : 200, { 'content-type': 'application/json' });
  response.end(JSON.stringify(payload));
});
server.listen(port, '0.0.0.0');
export {server};
