// The World in One Day — Monday 23 November 2026
// Copies the pre-rendered entry.png into the grader output directory.
// Node standard library only: no Python, no Pillow, no third-party packages.
// The grader runs `node /bot/main.ts` from an unrelated cwd, so the image
// is resolved relative to this file, never via process.cwd().

import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { fileURLToPath } from "node:url";

const source = fileURLToPath(new URL("./entry.png", import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR;
if (!outDir) {
  throw new Error("MAKEFUN_OUTPUT_DIR is not set");
}
if (!existsSync(source)) {
  throw new Error(`entry image not found: ${source}`);
}
mkdirSync(outDir, { recursive: true });
copyFileSync(source, `${outDir}/entry.png`);
