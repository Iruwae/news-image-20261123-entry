import { execFileSync } from "node:child_process";
import { existsSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const drawPy = join(here, "draw.py");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

execFileSync("python3", [drawPy, outDir], { stdio: "inherit" });

const out = join(outDir, "entry.png");
if (!existsSync(out)) {
  throw new Error("entry.png was not produced in " + outDir);
}
console.log("entry.png:", statSync(out).size, "bytes");
