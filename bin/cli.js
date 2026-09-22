#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const os = require('os');
const { execFileSync } = require('child_process');

// Piping into head/less closes stdout early; exit quietly instead of throwing.
process.stdout.on('error', err => { if (err.code === 'EPIPE') process.exit(0); throw err; });

const ROOT = path.join(__dirname, '..');
const PKG = require(path.join(ROOT, 'package.json'));

const MODULES = [
  ['spec-writer',          'Router and shared conventions'],
  ['mrd-writer',          '1. Market Requirements Document'],
  ['brd-writer',          '2. Business Requirements Document'],
  ['prd-writer',          '3. Product Requirements Document'],
  ['design-spec-writer',  '4. Design Specification'],
  ['trd-writer',          '5. Technical Requirements Document'],
  ['qa-test-plan-writer', '6. QA Test Plan'],
];
const NAMES = MODULES.map(([n]) => n);

// --------------------------------------------------------------------------- //
const c = process.stdout.isTTY && !process.env.NO_COLOR
  ? { b: s => `\x1b[1m${s}\x1b[0m`, d: s => `\x1b[2m${s}\x1b[0m`,
      g: s => `\x1b[32m${s}\x1b[0m`, y: s => `\x1b[33m${s}\x1b[0m`, r: s => `\x1b[31m${s}\x1b[0m` }
  : { b: s => s, d: s => s, g: s => s, y: s => s, r: s => s };

const say  = (...a) => console.log(...a);
const tilde = p => p.startsWith(os.homedir()) ? p.replace(os.homedir(), '~') : p;
const ok   = m => say(`  ${c.g('✓')} ${m}`);
const skip = m => say(`  ${c.y('·')} ${m}`);
const die  = m => { console.error(`${c.r('error')} ${m}`); process.exit(1); };

function copyFile(src, dest, force, base) {
  const show = base ? path.relative(base, dest) || dest : dest;
  if (fs.existsSync(dest) && !force) { skip(`${show} ${c.d('exists — pass --force to overwrite')}`); return false; }
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.copyFileSync(src, dest);
  ok(show);
  return true;
}

function resolveModule(name) {
  if (!name) die(`which document? one of: ${NAMES.join(', ')}`);
  if (NAMES.includes(name)) return name;
  const guess = NAMES.find(n => n.startsWith(name) || n.replace('-writer', '') === name);
  if (guess) return guess;
  die(`unknown document "${name}". Try: ${NAMES.join(', ')}`);
}

// --------------------------------------------------------------------------- //
const TARGETS = {
  claude: {
    label: 'Claude Code',
    run(opts) {
      const home = opts.global ? os.homedir() : opts.dir;
      const base = path.join(home, '.claude', 'skills');
      say(`\n${c.b('Claude Code')} ${c.d('→ ' + tilde(base))}`);
      let n = 0;
      for (const [name] of MODULES) {
        if (copyFile(path.join(ROOT, 'skills', name, 'SKILL.md'),
                     path.join(base, name, 'SKILL.md'), opts.force, base)) n++;
        // SKILL.md points at references/ for the document template and the
        // router's platform tables; a skill installed without them is broken.
        const refs = path.join(ROOT, 'skills', name, 'references');
        if (!fs.existsSync(refs)) continue;
        for (const f of fs.readdirSync(refs).sort()) {
          copyFile(path.join(refs, f), path.join(base, name, 'references', f), opts.force, base);
        }
      }
      if (n) say(`\n  ${c.d('Restart Claude Code, then ask for any of the six documents.')}`);
    },
  },
  cursor: {
    label: 'Cursor',
    run(opts) {
      const base = path.join(opts.dir, '.cursor', 'rules');
      say(`\n${c.b('Cursor')} ${c.d('→ ' + tilde(base))}`);
      for (const [name] of MODULES) {
        copyFile(path.join(ROOT, 'dist', 'agents', 'cursor-rules', `${name}.mdc`),
                 path.join(base, `${name}.mdc`), opts.force, base);
      }
    },
  },
  copilot: {
    label: 'GitHub Copilot',
    run(opts) {
      say(`\n${c.b('GitHub Copilot')}`);
      copyFile(path.join(ROOT, 'dist', 'agents', 'copilot-instructions.md'),
               path.join(opts.dir, '.github', 'copilot-instructions.md'), opts.force, opts.dir);
    },
  },
  agents: {
    label: 'AGENTS.md (Codex, Jules, Gemini CLI, and others)',
    run(opts) {
      say(`\n${c.b('AGENTS.md')}`);
      copyFile(path.join(ROOT, 'dist', 'agents', 'AGENTS.md'),
               path.join(opts.dir, 'AGENTS.md'), opts.force, opts.dir);
    },
  },
};

function detect(dir) {
  const found = [];
  if (fs.existsSync(path.join(dir, '.claude'))) found.push('claude');
  if (fs.existsSync(path.join(dir, '.cursor'))) found.push('cursor');
  if (fs.existsSync(path.join(dir, '.github'))) found.push('copilot');
  if (fs.existsSync(path.join(dir, 'AGENTS.md'))) found.push('agents');
  return found;
}

// --------------------------------------------------------------------------- //
function cmdInstall(args, opts) {
  const bad = args.filter(a => !(a in TARGETS) && a !== 'all');
  if (bad.length) die(`unknown target "${bad[0]}". Try: ${Object.keys(TARGETS).join(', ')}, or all`);

  let targets = args.includes('all') ? Object.keys(TARGETS) : args.filter(a => a in TARGETS);
  if (!targets.length) {
    targets = detect(opts.dir);
    if (!targets.length) {
      say(`\nNo assistant detected in ${c.d(tilde(opts.dir))}.\n`);
      say(`  Name one explicitly:  ${c.b('npx spec-writer install claude')}`);
      say(`  Or all of them:       ${c.b('npx spec-writer install all')}\n`);
      say(`  Targets: ${Object.keys(TARGETS).join(', ')}`);
      say(`\n  For ChatGPT, Grok, or Gemini there is nothing to install — those take a`);
      say(`  pasted prompt: ${c.b('npx spec-writer copy prd')}\n`);
      return;
    }
    say(`\nDetected: ${targets.map(t => TARGETS[t].label).join(', ')}`);
  }
  for (const t of targets) TARGETS[t].run(opts);
  say('');
}

function cmdList() {
  say(`\n${c.b('spec-writer')} ${c.d('— six connected specification documents')}\n`);
  for (const [name, desc] of MODULES) say(`  ${c.b(name.padEnd(22))} ${desc}`);
  say(`\n  ${c.d('print a prompt:')} npx spec-writer print prd`);
  say(`  ${c.d('copy to clipboard:')} npx spec-writer copy prd`);
  say(`  ${c.d('install locally:')} npx spec-writer install claude\n`);
}

function readPrompt(name) {
  return fs.readFileSync(path.join(ROOT, 'dist', 'universal', `${name}.md`), 'utf8');
}

function cmdPrint(args) {
  const name = args[0] === 'all' ? 'spec-writer-complete' : resolveModule(args[0]);
  process.stdout.write(readPrompt(name));
}

function cmdCopy(args) {
  const name = args[0] === 'all' ? 'spec-writer-complete' : resolveModule(args[0]);
  const text = readPrompt(name);
  const cmds = { darwin: ['pbcopy', []], win32: ['clip', []], linux: ['xclip', ['-selection', 'clipboard']] };
  const [bin, bargs] = cmds[process.platform] || [];
  if (!bin) die(`no clipboard command for ${process.platform} — use "print" and pipe it instead`);
  try {
    execFileSync(bin, bargs, { input: text });
  } catch {
    die(`couldn't run ${bin} — use "print" and pipe it instead`);
  }
  say(`\n  ${c.g('✓')} ${c.b(name)} copied (${text.length.toLocaleString()} chars)`);
  say(`  ${c.d('Paste it into ChatGPT, Grok, Gemini, or Claude, then send your idea.')}\n`);
}

function cmdHelp() {
  say(`
${c.b('spec-writer')} ${c.d('v' + PKG.version)} — MRD → BRD → PRD → Design Spec → TRD → QA Test Plan

${c.b('USAGE')}
  npx spec-writer <command> [args]

${c.b('COMMANDS')}
  ${c.b('list')}                    show the six documents
  ${c.b('install')} [target...]     install into this project (auto-detects if omitted)
  ${c.b('print')} <doc|all>         write a paste-ready prompt to stdout
  ${c.b('copy')} <doc|all>          copy a paste-ready prompt to the clipboard

${c.b('TARGETS')}
  claude    .claude/skills/          ${c.d('Claude Code')}
  cursor    .cursor/rules/           ${c.d('Cursor')}
  copilot   .github/                 ${c.d('GitHub Copilot')}
  agents    AGENTS.md                ${c.d('Codex, Jules, Gemini CLI, and others')}
  all       every target above

${c.b('OPTIONS')}
  --global      install Claude skills to ~/.claude/skills instead of this project
  --dir <path>  install into <path> instead of the current directory
  --force       overwrite files that already exist
  --version     print the version

${c.b('EXAMPLES')}
  npx spec-writer install                  ${c.d('detect and install')}
  npx spec-writer install claude --global  ${c.d('all projects')}
  npx spec-writer copy prd                 ${c.d('paste into ChatGPT or Grok')}
  npx spec-writer print all > spec-writer.md

${c.d('ChatGPT, Grok, and Gemini have nothing to install — they take a pasted')}
${c.d('prompt, or an uploaded file from dist/universal/. See PLATFORMS.md.')}
`);
}

// --------------------------------------------------------------------------- //
function main(argv) {
  const opts = { dir: process.cwd(), force: false, global: false, dirGiven: false };
  const args = [];
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--force' || a === '-f') opts.force = true;
    else if (a === '--global' || a === '-g') opts.global = true;
    else if (a === '--dir') { opts.dir = path.resolve(argv[++i] || '.'); opts.dirGiven = true; }
    else if (a === '--version' || a === '-v') return say(PKG.version);
    else if (a === '--help' || a === '-h') return cmdHelp();
    else args.push(a);
  }
  if (opts.global && opts.dirGiven) {
    die('--global installs to ~/.claude/skills and ignores --dir — pass one or the other');
  }
  const cmd = args.shift();
  switch (cmd) {
    case undefined:
    case 'help':    return cmdHelp();
    case 'list':    return cmdList();
    case 'install': return cmdInstall(args, opts);
    case 'print':   return cmdPrint(args);
    case 'copy':    return cmdCopy(args);
    default:        die(`unknown command "${cmd}" — run with --help`);
  }
}

main(process.argv.slice(2));
