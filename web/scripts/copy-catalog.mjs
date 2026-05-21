import { cp, mkdir, rm } from "node:fs/promises";
import { existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join, resolve } from "node:path";

const WEB_DIR = dirname(fileURLToPath(import.meta.url)) + "/..";
const REPO_DIR = resolve(WEB_DIR, "..");
const PUBLIC = join(WEB_DIR, "public");

const SOURCES = ["atoms", "prompts", "rules", "schemas", "exports"];

for (const src of SOURCES) {
  const from = join(REPO_DIR, src);
  const to = join(PUBLIC, src);
  if (!existsSync(from)) {
    console.warn(`skipping ${src}: ${from} does not exist`);
    continue;
  }
  await rm(to, { recursive: true, force: true });
  await mkdir(to, { recursive: true });
  await cp(from, to, { recursive: true });
  console.log(`copied ${src}/ → public/${src}/`);
}
