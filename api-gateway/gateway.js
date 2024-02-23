const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();

app.use((req, res, next) => {
  console.log(`Received request for ${req.url}`);
  next();
});

app.use('/api/v1/users', createProxyMiddleware({
  target: 'http://user-registration-service:5000',
  changeOrigin: true,
  logLevel: 'debug',
  onProxyReq: (proxyReq, req, res) => {
    console.log(`Proxying request for ${req.url} to ${'http://user-registration-service:5000'}${req.url}`);
  },
  onError: (err, req, res) => {
    console.log(`Error proxying ${req.url}: ${err.message}`);
  }
}));

app.use('/ping', createProxyMiddleware({
  target: 'http://user-registration-service:5000',
  changeOrigin: true,
  logLevel: 'debug',
  onProxyReq: (proxyReq, req, res) => {
    console.log(`Proxying request for ${req.url} to ${'http://user-registration-service:5000'}${req.url}`);
  },
  onError: (err, req, res) => {
    console.log(`Error proxying ${req.url}: ${err.message}`);
  }
}));

app.get('/test', (req, res) => {
  console.log('Test route accessed');
  res.send('API Gateway is up and running');
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`API Gateway running on port ${PORT}`);
});
