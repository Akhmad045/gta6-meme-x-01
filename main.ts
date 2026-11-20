// gta6-meme-x-01 entry program (Node 22, standard library only).
//
// The entry itself is a post on X: a GTA 6 meme picture (a ghost who waited
// 13 years for the game, sitting on his suitcases in a neon Vice City
// boulevard, calendar in hand) whose text carries the bounty link, the
// @makefunai tag and my play code. This program's whole job is to hand the
// post's address to the grader: it reads POST.json at the repository root,
// sanity-checks the address, and copies the file to the output directory,
// where the gate picks it up and reads the post from X itself.
//
// Local run (the grader's /bot and /output are replaced by two env vars):
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const LINK_FILE = 'POST.json';

// An X post address: x.com/<handle>/status/<numeric id>, with the www. or
// mobile. subdomain and the twitter.com host read as the same thing.
const POST_URL =
  /^https:\/\/(www\.|mobile\.)?(x\.com|twitter\.com)\/[^/?#]+\/status\/\d+(?:[?#].*)?$/;

function readLink(): string {
  const raw = readFileSync(join(BOT_DIR, LINK_FILE), 'utf8');
  const data = JSON.parse(raw) as { url?: unknown };
  if (typeof data.url !== 'string' || data.url.length === 0) {
    throw new Error(`${LINK_FILE} must be a JSON object with a "url" string`);
  }
  return data.url;
}

function main(): void {
  const url = readLink();
  if (!POST_URL.test(url)) {
    // Not fatal here: the placeholder that ships before the post exists has
    // this shape too. The gate on the site is the judge of the real address.
    console.error(`warning: ${url} is not a finished X post address yet`);
  }
  mkdirSync(OUTPUT_DIR, { recursive: true });
  copyFileSync(join(BOT_DIR, LINK_FILE), join(OUTPUT_DIR, LINK_FILE));
  console.log(`${LINK_FILE}: ${url}`);
  console.log(`copied to ${join(OUTPUT_DIR, LINK_FILE)}`);
}

try {
  main();
} catch (err) {
  console.error(`gta6-meme-x-01: ${(err as Error).message}`);
  process.exit(1);
}
