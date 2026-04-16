// Convierte los SVG de assets/icons/*.svg a PNG 144x144
const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const ICONS_DIR = path.join(__dirname, '..', 'assets', 'icons');

async function main() {
  const files = fs.readdirSync(ICONS_DIR).filter(f => f.endsWith('.svg'));
  for (const f of files) {
    const src = path.join(ICONS_DIR, f);
    const out = path.join(ICONS_DIR, f.replace(/\.svg$/, '.png'));
    const svgBuf = fs.readFileSync(src);
    const info = await sharp(svgBuf, { density: 300 })
      .resize(144, 144, { fit: 'contain', background: { r: 0, g: 0, b: 0, alpha: 0 } })
      .png()
      .toFile(out);
    console.log(`${f} -> ${path.basename(out)} (${info.size} bytes, ${info.width}x${info.height})`);
  }
}

main().catch(err => { console.error(err); process.exit(1); });
