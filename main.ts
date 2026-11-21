import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// The grader runs `node /bot/main.ts` from a different working directory
// with the repo read-only at /bot, so never resolve entry.png relative to
// the working directory: resolve it next to this entrypoint instead.
const entryDir = dirname(fileURLToPath(import.meta.url));
const srcPath = join(entryDir, "entry.png");

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? join(entryDir, "out");
mkdirSync(outDir, { recursive: true });
const dstPath = join(outDir, "entry.png");
copyFileSync(srcPath, dstPath);

// Confirm the copy is byte-identical to the source image.
const src = readFileSync(srcPath);
const dst = readFileSync(dstPath);
const hash = (b: Buffer) => createHash("sha256").update(b).digest("hex");
if (hash(src) !== hash(dst)) throw new Error("entry.png copy mismatch");
console.log("entry.png written, sha256 " + hash(dst));
