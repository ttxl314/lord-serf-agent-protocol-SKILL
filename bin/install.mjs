#!/usr/bin/env node
/**
 * Installer for the Lord and Serf agent skills.
 *
 * Copies `lord/` and `serf/` into a host skills directory. It never touches
 * anything outside the target `lord` and `serf` folders, and it refuses to
 * replace an existing install unless `--force` is given.
 */

import { cp, mkdir, readFile, readdir, rm } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..');
const pkg = JSON.parse(await readFile(path.join(root, 'package.json'), 'utf8'));
const SKILLS = ['lord', 'serf'];

const HOSTS = {
  codex: {
    label: 'Codex',
    dir: () => path.join(os.homedir(), '.codex', 'skills'),
    invoke: '$lord / $serf',
  },
  claude: {
    label: 'Claude Code',
    dir: () => path.join(os.homedir(), '.claude', 'skills'),
    invoke: '/lord / /serf',
  },
  dsh: {
    label: 'DSH (DeepSeek)',
    dir: () => path.join(os.homedir(), '.dsh', 'skills'),
    invoke: 'skill("lord") / skill("serf")',
  },
};

const HELP = `lord-serf-skill ${pkg.version} - install the Lord and Serf skills

Usage:
  npx lord-serf-skill install --all
  npx lord-serf-skill install <target> [options]

Targets:
  --codex             install into ~/.codex/skills
  --claude, --cc      install into ~/.claude/skills
  --dsh               install into ~/.dsh/skills
  --dir <path>        install into any other skills directory
  --all, -a           install into Codex, Claude Code, and DSH

Options:
  --force, -f         replace an existing lord/ or serf/ install
  --dry-run           print the plan and write nothing
  --list, -l          show the detected host directories
  --version, -v       print the package version
  --help, -h          print this help

The installer only writes <skills-dir>/lord and <skills-dir>/serf.`;

function fail(message) {
  console.error(`error: ${message}`);
  console.error('Run with --help for usage.');
  process.exit(1);
}

const argv = process.argv.slice(2);
if (argv[0] === 'install') {
  argv.shift();
}

const opts = { hosts: [], dir: null, force: false, dryRun: false, list: false, help: false };

for (let i = 0; i < argv.length; i += 1) {
  const arg = argv[i];
  switch (arg) {
    case '--codex':
      opts.hosts.push('codex');
      break;
    case '--claude':
    case '--cc':
      opts.hosts.push('claude');
      break;
    case '--dsh':
      opts.hosts.push('dsh');
      break;
    case '--all':
    case '-a':
      opts.hosts.push('codex', 'claude', 'dsh');
      break;
    case '--dir': {
      const value = argv[i + 1];
      if (!value || value.startsWith('-')) {
        fail('--dir needs a path');
      }
      opts.dir = path.resolve(value);
      i += 1;
      break;
    }
    case '--force':
    case '-f':
      opts.force = true;
      break;
    case '--dry-run':
      opts.dryRun = true;
      break;
    case '--list':
    case '-l':
      opts.list = true;
      break;
    case '--version':
    case '-v':
      console.log(pkg.version);
      process.exit(0);
      break;
    case '--help':
    case '-h':
      opts.help = true;
      break;
    default:
      fail(`unknown option: ${arg}`);
  }
}

if (opts.help) {
  console.log(HELP);
  process.exit(0);
}

async function countFiles(dir) {
  let total = 0;
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    total += entry.isDirectory() ? await countFiles(path.join(dir, entry.name)) : 1;
  }
  return total;
}

function shortPath(target) {
  const home = os.homedir();
  return target.startsWith(home) ? `~${target.slice(home.length)}` : target;
}

if (opts.list) {
  console.log(`lord-serf-skill ${pkg.version} - detected host directories\n`);
  for (const host of Object.values(HOSTS)) {
    const dir = host.dir();
    const state = existsSync(dir) ? 'found' : 'not created yet';
    console.log(`  ${host.label.padEnd(15)} ${shortPath(dir).padEnd(24)} ${state}`);
  }
  console.log('\nUse --all to install everywhere, or pick one host.');
  process.exit(0);
}

if (!opts.hosts.length && !opts.dir) {
  console.log(HELP);
  console.error('\nChoose at least one target, for example: npx lord-serf-skill install --all');
  process.exit(1);
}

const targets = [];
if (opts.dir) {
  targets.push({ label: 'Custom directory', dir: opts.dir, invoke: 'load the skill files directly' });
}
for (const key of [...new Set(opts.hosts)]) {
  const host = HOSTS[key];
  targets.push({ label: host.label, dir: host.dir(), invoke: host.invoke });
}

console.log(`lord-serf-skill ${pkg.version}${opts.dryRun ? ' (dry run)' : ''}\n`);

let skipped = 0;
let written = 0;

for (const target of targets) {
  console.log(`${target.label}  ->  ${shortPath(target.dir)}`);
  for (const skill of SKILLS) {
    const source = path.join(root, skill);
    const dest = path.join(target.dir, skill);
    const existed = existsSync(dest);

    if (existed && !opts.force) {
      skipped += 1;
      console.log(`  ${skill}: kept the existing copy (use --force to replace)`);
      continue;
    }

    const files = await countFiles(source);
    if (!opts.dryRun) {
      await mkdir(target.dir, { recursive: true });
      if (existed) {
        await rm(dest, { recursive: true, force: true });
      }
      await cp(source, dest, { recursive: true });
    }
    written += 1;
    console.log(`  ${skill}: ${existed ? 'replaced' : 'installed'} (${files} files)`);
  }
  console.log(`  invoke: ${target.invoke}\n`);
}

if (!written && skipped) {
  console.log('Nothing was written. Re-run with --force to replace the existing copies.');
} else {
  console.log('Reload or restart the host so it picks up the new skills.');
}
console.log('Protocol 0.6: regenerate unfinished artifacts with protocol_version "0.6".');
