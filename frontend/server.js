/**
 * HTTPS development server for Next.js frontend.
 * Uses SSL certificates from the certs directory.
 * 
 * Usage:
 *   node server.js
 * 
 * Requirements:
 *   - SSL certificates in ../certs/ directory
 *   - localhost.pem (certificate)
 *   - localhost-key.pem (private key)
 * 
 * See HTTPS_SETUP.md for certificate generation instructions.
 */

const { createServer } = require('https');
const { parse } = require('url');
const next = require('next');
const fs = require('fs');
const path = require('path');

const dev = process.env.NODE_ENV !== 'production';
const hostname = 'localhost';
const port = parseInt(process.env.PORT, 10) || 3000;

// Path to certificates (in parent directory)
const certDir = path.join(__dirname, '..', 'certs');
const certFile = path.join(certDir, 'localhost.pem');
const keyFile = path.join(certDir, 'localhost-key.pem');

// Check if certificates exist
if (!fs.existsSync(certFile) || !fs.existsSync(keyFile)) {
  console.error('❌ SSL certificates not found!');
  console.error('\nExpected files:');
  console.error(`  - ${certFile}`);
  console.error(`  - ${keyFile}`);
  console.error('\n📚 Please generate certificates first:');
  console.error('  1. Install mkcert: https://github.com/FiloSottile/mkcert');
  console.error('  2. Run: mkcert -install');
  console.error('  3. Create certs directory: mkdir certs');
  console.error('  4. Generate certificates: cd certs && mkcert localhost 127.0.0.1 ::1');
  console.error('  5. Rename files:');
  console.error('     - mv localhost+2.pem localhost.pem');
  console.error('     - mv localhost+2-key.pem localhost-key.pem');
  console.error('\nSee HTTPS_SETUP.md for detailed instructions.');
  process.exit(1);
}

// HTTPS options
const httpsOptions = {
  key: fs.readFileSync(keyFile),
  cert: fs.readFileSync(certFile),
};

// Initialize Next.js app
const app = next({ dev, hostname, port });
const handle = app.getRequestHandler();

app.prepare().then(() => {
  createServer(httpsOptions, async (req, res) => {
    try {
      const parsedUrl = parse(req.url, true);
      await handle(req, res, parsedUrl);
    } catch (err) {
      console.error('Error occurred handling', req.url, err);
      res.statusCode = 500;
      res.end('internal server error');
    }
  })
    .once('error', (err) => {
      console.error('❌ Server error:', err);
      process.exit(1);
    })
    .listen(port, () => {
      console.log('='.repeat(60));
      console.log('🔒 HTTPS Development Server Started');
      console.log('='.repeat(60));
      console.log(`📁 Certificate directory: ${certDir}`);
      console.log(`🔑 Private key: ${path.basename(keyFile)}`);
      console.log(`📜 Certificate: ${path.basename(certFile)}`);
      console.log('-'.repeat(60));
      console.log(`🌐 Frontend URL: https://${hostname}:${port}`);
      console.log(`🔍 Ready for connections`);
      console.log('-'.repeat(60));
      console.log('💡 Tips:');
      console.log('  - First time? Your browser may show a security warning');
      console.log('  - With mkcert: No warnings, certificate is trusted');
      console.log('  - Self-signed: Click \'Advanced\' → \'Proceed to localhost\'');
      console.log('  - Press Ctrl+C to stop the server');
      console.log('='.repeat(60));
      console.log();
    });
});
