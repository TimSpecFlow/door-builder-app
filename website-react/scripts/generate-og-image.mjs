// Generates public/og-image.jpg (1200x630) for social share previews.
// Run: npm run og   (regenerate whenever branding changes)
import sharp from 'sharp';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const out = resolve(__dirname, '..', 'public', 'og-image.jpg');

const W = 1200;
const H = 630;

const svg = `
<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1a1a1a"/>
      <stop offset="100%" stop-color="#0d0d0d"/>
    </linearGradient>
  </defs>
  <rect width="${W}" height="${H}" fill="url(#bg)"/>

  <!-- gold hairline frame -->
  <rect x="40" y="40" width="${W - 80}" height="${H - 80}" fill="none" stroke="#c9a962" stroke-opacity="0.4" stroke-width="1.5"/>

  <!-- monogram -->
  <rect x="90" y="86" width="72" height="72" rx="10" fill="#c9a962"/>
  <text x="126" y="123" text-anchor="middle" dominant-baseline="central"
        font-family="Georgia, serif" font-size="34" font-weight="700" fill="#1a1a1a">SF</text>

  <!-- eyebrow -->
  <text x="90" y="330" font-family="Arial, Helvetica, sans-serif" font-size="22"
        letter-spacing="6" fill="#c9a962">PREMIUM DOOR SOLUTIONS</text>

  <!-- wordmark -->
  <text x="86" y="410" font-family="Georgia, serif" font-size="92" font-weight="700" fill="#ffffff">SpecFlow</text>

  <!-- gold divider -->
  <rect x="90" y="448" width="120" height="3" fill="#c9a962"/>

  <!-- tagline -->
  <text x="90" y="512" font-family="Arial, Helvetica, sans-serif" font-size="30" fill="#cccccc">Bespoke doors &amp; precision hardware</text>

  <!-- location -->
  <text x="90" y="558" font-family="Arial, Helvetica, sans-serif" font-size="24" fill="#888888">Phoenix &amp; Scottsdale, AZ  ·  specflow.tech</text>
</svg>`;

await sharp(Buffer.from(svg)).jpeg({ quality: 90 }).toFile(out);
console.log('Wrote', out);
