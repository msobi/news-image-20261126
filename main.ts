import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const PNG_SIGNATURE: readonly number[] = [
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
];
const REQUIRED_EDGE = 1024;
const SIZE_LIMIT = 1024 * 1024; // 1 MiB

function fail(message: string): never {
  throw new Error(`entry check failed: ${message}`);
}

function inspectPng(buf: Buffer): { width: number; height: number } {
  if (buf.length < 24) {
    fail(`file is only ${buf.length} bytes, too small to be a valid PNG`);
  }
  for (let i = 0; i < PNG_SIGNATURE.length; i++) {
    if (buf[i] !== PNG_SIGNATURE[i]) {
      fail("file does not start with the PNG magic bytes");
    }
  }
  // The first chunk after the signature must be IHDR; its payload begins
  // with width and height as big-endian uint32 values at offsets 16 and 20.
  const chunkName = buf.toString("ascii", 12, 16);
  if (chunkName !== "IHDR") {
    fail(`expected IHDR as first chunk, found "${chunkName}"`);
  }
  return { width: buf.readUInt32BE(16), height: buf.readUInt32BE(20) };
}

function main(): void {
  const here = path.dirname(fileURLToPath(import.meta.url));
  const source = path.join(here, "entry.png");
  if (!fs.existsSync(source)) {
    fail(`entry.png not found next to main.ts (looked in ${here})`);
  }

  const bytes = fs.readFileSync(source);
  if (bytes.length > SIZE_LIMIT) {
    fail(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
  }
  const { width, height } = inspectPng(bytes);
  if (width !== REQUIRED_EDGE || height !== REQUIRED_EDGE) {
    fail(`entry.png is ${width}x${height}, expected ${REQUIRED_EDGE}x${REQUIRED_EDGE}`);
  }

  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  fs.mkdirSync(outDir, { recursive: true });
  const target = path.join(outDir, "entry.png");
  fs.writeFileSync(target, bytes);
  console.log(`wrote ${target} (${bytes.length} bytes, ${width}x${height})`);
}

main();
