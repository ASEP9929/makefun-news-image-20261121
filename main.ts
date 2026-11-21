import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";
mkdirSync(outDir, { recursive: true });
copyFileSync("entry.png", join(outDir, "entry.png"));

// Confirm the copy is byte-identical to the source image.
const src = readFileSync("entry.png");
const dst = readFileSync(join(outDir, "entry.png"));
const hash = (b: Buffer) => createHash("sha256").update(b).digest("hex");
if (hash(src) !== hash(dst)) throw new Error("entry.png copy mismatch");
console.log("entry.png written, sha256 " + hash(dst));
