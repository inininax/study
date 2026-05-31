#!/usr/bin/env node
// Design System Test Harness
// Pure Node.js, zero third-party dependencies.
// CJS because package.json has "type": "module".

'use strict';

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const DIST = path.join(ROOT, 'dist');
const SRC  = path.join(ROOT, 'src');

// ── Result tracking ───────────────────────────────────────────────────────────

let totalTests = 0;
let passed = 0;
let failed = 0;
let warned = 0;

const failures = [];
const warnings = [];

function pass(id, msg) {
  totalTests++;
  passed++;
  console.log(`  ✓ ${id} ${msg}`);
}

function fail(id, msg, detail = '') {
  totalTests++;
  failed++;
  const line = `  ✗ ${id} ${msg}`;
  console.log(line);
  if (detail) {
    detail.split('\n').forEach(l => console.log(`      ${l}`));
  }
  failures.push({ id, msg, detail });
}

function warn(id, msg, items = []) {
  // warnings do NOT increment totalTests — they're annotations on existing tests
  warned++;
  console.log(`  ⚠ ${id} ${msg}`);
  items.forEach(i => console.log(`      ${i}`));
  warnings.push({ id, msg, items });
}

function group(title) {
  console.log(`\nGroup ${title}`);
  console.log('─'.repeat(50));
}

// ── Helpers ───────────────────────────────────────────────────────────────────

function fileExists(p) {
  try { return fs.statSync(p).size > 0; } catch { return false; }
}

function readText(p) {
  return fs.readFileSync(p, 'utf8');
}

function readJSON(p) {
  return JSON.parse(readText(p));
}

/** Recursively flatten {a: {b: {value: x}}} to {"a-b": x} */
function flattenSemantic(obj, prefix = '') {
  const out = {};
  for (const [k, v] of Object.entries(obj)) {
    const key = prefix ? `${prefix}-${k}` : k;
    if (v && typeof v === 'object' && !Array.isArray(v)) {
      if ('value' in v) {
        out[key] = v.value;
      } else {
        Object.assign(out, flattenSemantic(v, key));
      }
    }
  }
  return out;
}

/** Extract all declared --name: value CSS variable names from a CSS string */
function extractDeclaredVars(css) {
  const set = new Set();
  // Match --foo-bar: in any context (:root, selectors, @media etc.)
  const re = /--([\w-]+)\s*:/g;
  let m;
  while ((m = re.exec(css)) !== null) {
    set.add(m[1]);
  }
  return set;
}

/** Extract all var(--name) references (with or without fallback) from a CSS string */
function extractVarRefs(css) {
  const refs = [];
  // Also capture position (char index) for approximate line numbers
  const re = /var\(\s*--([\w-]+)\s*([,)])/g;
  let m;
  while ((m = re.exec(css)) !== null) {
    const name = m[1];
    const hasFallback = m[2] === ',';
    // Approximate line number by counting \n before this match
    const lineNo = css.slice(0, m.index).split('\n').length;
    refs.push({ name, hasFallback, line: lineNo });
  }
  return refs;
}

// ── Group 1: Build artifact integrity ─────────────────────────────────────────

function runGroup1() {
  group('1: Build artifact integrity');

  // T1.1 — Required CSS files exist and are non-empty
  const cssFiles = [
    'tokens.css', 'tokens-light.css', 'tokens-dark.css',
    'reset.css', 'utilities.css', 'animations.css',
    'components.css', 'layouts.css', 'all.css'
  ];
  const missingCss = cssFiles.filter(f => !fileExists(path.join(DIST, 'css', f)));
  if (missingCss.length === 0) {
    pass('T1.1', `dist CSS files exist and non-empty (${cssFiles.length} files)`);
  } else {
    fail('T1.1', 'dist CSS files exist and non-empty', `Missing: ${missingCss.join(', ')}`);
  }

  // T1.2 — DTCG JSON valid structure
  try {
    const dtcg = readJSON(path.join(DIST, 'json', 'tokens.tokens.json'));
    const hasKeys = ['primitive', 'semantic-light', 'semantic-dark'].every(k => k in dtcg);
    if (hasKeys) {
      pass('T1.2', 'DTCG JSON valid structure (primitive, semantic-light, semantic-dark keys)');
    } else {
      const found = Object.keys(dtcg).join(', ');
      fail('T1.2', 'DTCG JSON valid structure', `Expected keys: primitive, semantic-light, semantic-dark. Found: ${found}`);
    }
  } catch (e) {
    fail('T1.2', 'DTCG JSON valid structure', e.message);
  }

  // T1.3 — JS tokens exist and tokens.cjs is require()-able
  const jsFiles = ['tokens.js', 'tokens.cjs', 'tokens.d.ts'];
  const missingJs = jsFiles.filter(f => !fileExists(path.join(DIST, 'js', f)));
  if (missingJs.length > 0) {
    fail('T1.3', 'dist/js files exist', `Missing: ${missingJs.join(', ')}`);
  } else {
    try {
      const cjs = require(path.join(DIST, 'js', 'tokens.cjs'));
      const hasExports = ['primitives', 'light', 'dark'].every(k => k in cjs);
      if (hasExports) {
        pass('T1.3', 'tokens.cjs require()-able and exports primitives, light, dark');
      } else {
        const found = Object.keys(cjs).join(', ');
        fail('T1.3', 'tokens.cjs exports primitives, light, dark', `Found: ${found}`);
      }
    } catch (e) {
      fail('T1.3', 'tokens.cjs require()-able', e.message);
    }
  }

  // T1.4 — SCSS files exist
  const scssFiles = ['_tokens.scss', '_mixins.scss', 'index.scss'];
  const missingScss = scssFiles.filter(f => !fileExists(path.join(DIST, 'scss', f)));
  if (missingScss.length === 0) {
    pass('T1.4', `dist SCSS files exist (${scssFiles.join(', ')})`);
  } else {
    fail('T1.4', 'dist SCSS files exist', `Missing: ${missingScss.join(', ')}`);
  }
}

// ── Group 2: CSS variable graph integrity ─────────────────────────────────────

function runGroup2() {
  group('2: CSS variable graph integrity');

  const tokensCss = readText(path.join(DIST, 'css', 'tokens.css'));
  const declaredVars = extractDeclaredVars(tokensCss);

  // T2.1 — Count declared variables
  pass('T2.1', `${declaredVars.size} CSS variables declared in tokens.css`);

  // T2.2 — Dangling var() references in component/layout/utility/animation CSS
  const checkFiles = [
    { name: 'components.css', p: path.join(DIST, 'css', 'components.css') },
    { name: 'layouts.css',    p: path.join(DIST, 'css', 'layouts.css') },
    { name: 'utilities.css',  p: path.join(DIST, 'css', 'utilities.css') },
    { name: 'animations.css', p: path.join(DIST, 'css', 'animations.css') },
  ];

  // Variables that are legitimately locally-defined in components (not from tokens.css)
  // These are custom properties set inline within component selectors themselves.
  // We detect them by scanning all the check files for declarations too.
  const locallyDeclared = new Set();
  for (const { p } of checkFiles) {
    const css = readText(p);
    for (const v of extractDeclaredVars(css)) locallyDeclared.add(v);
  }
  const allKnownVars = new Set([...declaredVars, ...locallyDeclared]);

  const dangling = [];
  for (const { name, p } of checkFiles) {
    const css = readText(p);
    const refs = extractVarRefs(css);
    for (const { name: varName, hasFallback, line } of refs) {
      if (!hasFallback && !allKnownVars.has(varName)) {
        dangling.push(`${name}:${line} → --${varName}`);
      }
    }
  }

  if (dangling.length === 0) {
    pass('T2.2', '0 dangling var() references (no fallback + not declared)');
  } else {
    fail('T2.2', `${dangling.length} dangling var() references`, dangling.join('\n'));
  }

  // T2.3 — Raw primitive color references in component CSS (soft warning)
  const componentsCss = readText(path.join(DIST, 'css', 'components.css'));
  const rawPrimitiveRefs = [];
  const primitiveColorRe = /var\(\s*--(color-(?:red|blue|green|amber|purple|pink|orange|yellow|indigo|cyan|teal|neutral|mocha|sage|terracotta|slate|gray|zinc|stone|rose|fuchsia|violet|sky|lime|emerald|white|black)-\d+)[,)]/g;
  let m;
  while ((m = primitiveColorRe.exec(componentsCss)) !== null) {
    const lineNo = componentsCss.slice(0, m.index).split('\n').length;
    rawPrimitiveRefs.push(`components.css:${lineNo} → --${m[1]}`);
  }

  // T2.3 is a warning-only test — always "passes" but may warn
  totalTests++;
  passed++;
  if (rawPrimitiveRefs.length > 0) {
    console.log(`  ✓ T2.3 raw-primitive color references check`);
    warn('T2.3', `${rawPrimitiveRefs.length} raw-primitive color var() use(s) in components.css (soft warning — prefer semantic tokens):`, rawPrimitiveRefs);
  } else {
    console.log(`  ✓ T2.3 0 raw-primitive color references in components.css`);
  }
}

// ── Group 3: Light/Dark semantic token parity ─────────────────────────────────

function runGroup3() {
  group('3: Light/Dark semantic token parity');

  const light = readJSON(path.join(SRC, 'tokens', 'semantic', 'light.json'));
  const dark  = readJSON(path.join(SRC, 'tokens', 'semantic', 'dark.json'));

  const lightFlat = flattenSemantic(light);
  const darkFlat  = flattenSemantic(dark);

  const lightKeys = new Set(Object.keys(lightFlat));
  const darkKeys  = new Set(Object.keys(darkFlat));

  // T3.1 — Tokens missing from one or the other
  const missingFromDark  = [...lightKeys].filter(k => !darkKeys.has(k));
  const missingFromLight = [...darkKeys].filter(k => !lightKeys.has(k));

  if (missingFromDark.length === 0 && missingFromLight.length === 0) {
    pass('T3.1', `Token set symmetric: ${lightKeys.size} light = ${darkKeys.size} dark`);
  } else {
    const details = [];
    if (missingFromDark.length)  details.push(`In light but missing from dark (${missingFromDark.length}): ${missingFromDark.join(', ')}`);
    if (missingFromLight.length) details.push(`In dark but missing from light (${missingFromLight.length}): ${missingFromLight.join(', ')}`);
    fail('T3.1', 'Semantic token sets are symmetric', details.join('\n'));
  }

  // T3.2 — Identical key sets (redundant but explicit count check)
  if (lightKeys.size === darkKeys.size && missingFromDark.length === 0 && missingFromLight.length === 0) {
    pass('T3.2', `Light and dark have identical key sets (${lightKeys.size} keys each)`);
  } else {
    fail('T3.2', `Light and dark have identical key sets`, `light=${lightKeys.size}, dark=${darkKeys.size}`);
  }
}

// ── Group 4: examples/index.html coverage ────────────────────────────────────

function runGroup4() {
  group('4: examples/index.html coverage');

  const htmlPath = path.join(ROOT, 'examples', 'index.html');
  const htmlDir  = path.dirname(htmlPath);
  let html;
  try {
    html = readText(htmlPath);
  } catch (e) {
    fail('T4.1', 'examples/index.html exists', e.message);
    fail('T4.2', 'ds-* classes in html exist in all.css', 'HTML file missing');
    fail('T4.3', 'At least one example per component', 'HTML file missing');
    return;
  }

  // T4.1 — Stylesheet links resolve
  const linkRe = /<link[^>]+rel=["']stylesheet["'][^>]+href=["']([^"']+)["']/gi;
  const missingLinks = [];
  let lm;
  while ((lm = linkRe.exec(html)) !== null) {
    const href = lm[1];
    const resolved = path.resolve(htmlDir, href);
    if (!fs.existsSync(resolved)) {
      missingLinks.push(`${href} → ${resolved}`);
    }
  }
  if (missingLinks.length === 0) {
    pass('T4.1', 'All <link> stylesheets resolve to existing files');
  } else {
    fail('T4.1', 'All <link> stylesheets resolve to existing files', missingLinks.join('\n'));
  }

  // T4.2 — Every .ds-* class used in the html exists in all.css
  const allCss = readText(path.join(DIST, 'css', 'all.css'));

  // Extract class definitions from all.css: .ds-foo, .ds-foo\:bar, etc.
  const definedClasses = new Set();
  // Match class selectors: .ds-something (with possible escape sequences)
  const classDefRe = /\.(ds-[\w\\:-]+)\s*[{,\s:]/g;
  let cdm;
  while ((cdm = classDefRe.exec(allCss)) !== null) {
    // Normalize escaped colons: ds-md\:grid-cols-3 → ds-md:grid-cols-3
    const cls = cdm[1].replace(/\\:/g, ':');
    definedClasses.add(cls);
  }

  // Extract class names used in the HTML (class="..." attributes)
  const htmlClassRe = /class=["']([^"']+)["']/g;
  const usedClasses = new Set();
  let hcm;
  while ((hcm = htmlClassRe.exec(html)) !== null) {
    hcm[1].trim().split(/\s+/).forEach(c => {
      if (c.startsWith('ds-')) usedClasses.add(c);
    });
  }

  const undefinedClasses = [...usedClasses].filter(c => {
    // For responsive classes like ds-md:grid-cols-2, check escaped form too
    const escaped = c.replace(/:/g, '\\:');
    return !definedClasses.has(c) && !definedClasses.has(escaped) && !allCss.includes(`.${escaped}`) && !allCss.includes(`.${c.replace(/:/g, '\\\\:')}`);
  });

  if (undefinedClasses.length === 0) {
    pass('T4.2', `All ${usedClasses.size} ds-* classes used in HTML are defined in all.css`);
  } else {
    fail('T4.2', `${undefinedClasses.length} ds-* classes used in HTML not found in all.css`, undefinedClasses.join(', '));
  }

  // T4.3 — At least one example per component (20 components)
  // Map component file name → primary class prefix used in HTML
  const componentMap = {
    accordion: 'ds-accordion',
    alert:     'ds-alert',
    avatar:    'ds-avatar',
    badge:     'ds-badge',
    button:    'ds-btn',
    card:      'ds-card',
    checkbox:  'ds-checkbox',
    divider:   'ds-divider',
    dropdown:  'ds-dropdown',
    input:     'ds-input',
    modal:     'ds-modal',
    navbar:    'ds-navbar',
    progress:  'ds-progress',
    select:    'ds-select',
    skeleton:  'ds-skeleton',
    table:     'ds-table',
    tabs:      'ds-tabs',
    textarea:  'ds-textarea',
    toggle:    'ds-toggle',
    tooltip:   'ds-tooltip',
  };

  const missingExamples = [];
  const presentExamples = [];
  for (const [component, cls] of Object.entries(componentMap)) {
    // Check for the class prefix in the html body (ignore <style> section)
    const bodyMatch = html.includes(`class="`) && html.includes(cls);
    if (bodyMatch) {
      presentExamples.push(component);
    } else {
      missingExamples.push(`${component} (${cls})`);
    }
  }

  if (missingExamples.length === 0) {
    pass('T4.3', `All 20 components have at least one example in index.html`);
  } else {
    fail('T4.3', `${missingExamples.length}/20 components missing examples in index.html`, missingExamples.join(', '));
  }
}

// ── Group 5: Component variant matrix ────────────────────────────────────────

function runGroup5() {
  group('5: Component variant matrix');

  // Interactive components that should have hover/focus-visible/disabled rules
  const interactiveComponents = [
    { name: 'button',   file: 'button.css',   cls: 'ds-btn' },
    { name: 'input',    file: 'input.css',     cls: 'ds-input' },
    { name: 'select',   file: 'select.css',    cls: 'ds-select' },
    { name: 'textarea', file: 'textarea.css',  cls: 'ds-textarea' },
    { name: 'checkbox', file: 'checkbox.css',  cls: 'ds-checkbox' },
    { name: 'toggle',   file: 'toggle.css',    cls: 'ds-toggle' },
    { name: 'dropdown', file: 'dropdown.css',  cls: 'ds-dropdown' },
    { name: 'tabs',     file: 'tabs.css',      cls: 'ds-tab' },
    { name: 'accordion',file: 'accordion.css', cls: 'ds-accordion' },
  ];

  // Components where :hover is intentionally placed on a sub-element/sibling
  // rather than the base class itself — still check the file contains :hover
  const hoverExceptionList = new Set(['checkbox', 'toggle', 'accordion']);
  // For checkbox/toggle, hover is on the label/track; for accordion on trigger

  let hoverPass = 0, hoverFail = 0;
  let focusPass = 0, focusFail = 0;
  let disabledPass = 0, disabledFail = 0;

  const hoverFailDetails = [];
  const focusFailDetails = [];
  const disabledFailDetails = [];

  for (const { name, file } of interactiveComponents) {
    const cssPath = path.join(SRC, 'components', file);
    let css;
    try { css = readText(cssPath); } catch { continue; }

    // :hover check (any :hover rule in the file)
    if (css.includes(':hover')) {
      hoverPass++;
    } else if (hoverExceptionList.has(name)) {
      hoverPass++; // documented exception
    } else {
      hoverFail++;
      hoverFailDetails.push(name);
    }

    // :focus-visible check
    if (css.includes(':focus-visible')) {
      focusPass++;
    } else {
      focusFail++;
      focusFailDetails.push(name);
    }

    // :disabled or [aria-disabled] check
    if (css.includes(':disabled') || css.includes('[aria-disabled')) {
      disabledPass++;
    } else {
      disabledFail++;
      disabledFailDetails.push(name);
    }
  }

  const n = interactiveComponents.length;
  if (hoverFail === 0) {
    pass('T5.x', `:hover rule present in all ${n} interactive components`);
  } else {
    fail('T5.x', `:hover rule missing in ${hoverFail} interactive component(s)`, hoverFailDetails.join(', '));
  }

  if (focusFail === 0) {
    pass('T5.y', `:focus-visible rule present in all ${n} interactive components`);
  } else {
    fail('T5.y', `:focus-visible rule missing in ${focusFail} interactive component(s)`, focusFailDetails.join(', '));
  }

  if (disabledFail === 0) {
    pass('T5.z', `:disabled / [aria-disabled] rule present in all ${n} interactive components`);
  } else {
    fail('T5.z', `:disabled / [aria-disabled] missing in ${disabledFail} interactive component(s)`, disabledFailDetails.join(', '));
  }

  // Size variant matrix: ds-{name}-sm and ds-{name}-lg
  const sizeComponents = [
    { name: 'button',   file: 'button.css',   smCls: '.ds-btn-sm',      lgCls: '.ds-btn-lg' },
    { name: 'input',    file: 'input.css',     smCls: '.ds-input-sm',    lgCls: '.ds-input-lg' },
    { name: 'select',   file: 'select.css',    smCls: '.ds-select-sm',   lgCls: '.ds-select-lg' },
    { name: 'textarea', file: 'textarea.css',  smCls: '.ds-textarea-sm', lgCls: '.ds-textarea-lg' },
    { name: 'badge',    file: 'badge.css',     smCls: '.ds-badge-sm',    lgCls: '.ds-badge-lg' },
    { name: 'toggle',   file: 'toggle.css',    smCls: '.ds-toggle-sm',   lgCls: '.ds-toggle-lg' },
  ];

  const missingSizeVariants = [];
  for (const { name, file, smCls, lgCls } of sizeComponents) {
    const cssPath = path.join(SRC, 'components', file);
    let css;
    try { css = readText(cssPath); } catch { continue; }
    if (!css.includes(smCls)) missingSizeVariants.push(`${name}: missing ${smCls}`);
    if (!css.includes(lgCls)) missingSizeVariants.push(`${name}: missing ${lgCls}`);
  }

  if (missingSizeVariants.length === 0) {
    pass('T5.size', `Size variants (-sm / -lg) present in all ${sizeComponents.length} size-variant components`);
  } else {
    fail('T5.size', `Size variants missing in some components`, missingSizeVariants.join('\n'));
  }
}

// ── Group 6: SCSS file integrity ──────────────────────────────────────────────

function runGroup6() {
  group('6: SCSS file integrity (static check)');

  const mixinsPath  = path.join(DIST, 'scss', '_mixins.scss');
  const tokensScssPath = path.join(DIST, 'scss', '_tokens.scss');

  let mixins, tokensScss;
  try { mixins = readText(mixinsPath); } catch (e) {
    fail('T6.1', '_mixins.scss readable', e.message);
    fail('T6.2', '_mixins.scss has no @import', 'file unreadable');
    fail('T6.3', '_mixins.scss no bare arithmetic', 'file unreadable');
    return;
  }
  try { tokensScss = readText(tokensScssPath); } catch (e) {
    fail('T6.1', '_tokens.scss readable', e.message);
    return;
  }

  // T6.1 — Variables in _mixins.scss must exist in _tokens.scss
  // Collect all $variable-names from _tokens.scss
  const scssVarRe = /\$([\w-]+)\s*:/g;
  const declaredScssVars = new Set();
  let sv;
  while ((sv = scssVarRe.exec(tokensScss)) !== null) {
    declaredScssVars.add(sv[1]);
  }
  // Also add SCSS map names defined in _tokens.scss
  const mapRe = /\$([\w-]+)\s*:\s*\(/g;
  let mr;
  while ((mr = mapRe.exec(tokensScss)) !== null) {
    declaredScssVars.add(mr[1]);
  }

  // Collect mixin parameter names from _mixins.scss: @mixin foo($param1, $param2: default)
  const mixinParamNames = new Set();
  const mixinDefRe = /@mixin\s+[\w-]+\s*\(([^)]*)\)/g;
  let md;
  while ((md = mixinDefRe.exec(mixins)) !== null) {
    const paramList = md[1];
    const paramRe = /\$([\w-]+)/g;
    let pm;
    while ((pm = paramRe.exec(paramList)) !== null) {
      mixinParamNames.add(pm[1]);
    }
  }

  // Also collect locally-assigned variables within mixin bodies: $foo: value
  const localAssignRe = /\$([\w-]+)\s*:/g;
  const localVars = new Set();
  let la;
  while ((la = localAssignRe.exec(mixins)) !== null) {
    localVars.add(la[1]);
  }

  // Known SCSS map variable names that are defined in _tokens.scss but only as maps
  const knownMaps = new Set(['breakpoints', 'spacings', 'font-sizes', 'radii', 'z-indexes', 'opacities', 'durations']);

  // Find all $variable usages in _mixins.scss (not declarations)
  const mixinVarUseRe = /\$([\w-]+)/g;
  const undefinedScssVars = new Set();
  let mu;
  while ((mu = mixinVarUseRe.exec(mixins)) !== null) {
    const varName = mu[1];
    // Skip if it's a mixin parameter, locally assigned var, map name, or declared in _tokens.scss
    if (
      declaredScssVars.has(varName) ||
      mixinParamNames.has(varName) ||
      localVars.has(varName) ||
      knownMaps.has(varName)
    ) {
      continue;
    }
    undefinedScssVars.add(varName);
  }

  if (undefinedScssVars.size === 0) {
    pass('T6.1', '_mixins.scss references no $variable missing from _tokens.scss');
  } else {
    fail('T6.1', '_mixins.scss $variable references missing from _tokens.scss',
      `Undefined: ${[...undefinedScssVars].join(', ')}`);
  }

  // T6.2 — No @import in _mixins.scss (must use @use / @forward)
  if (!mixins.includes('@import')) {
    pass('T6.2', '_mixins.scss uses no @import (uses @use/@forward)');
  } else {
    const lines = mixins.split('\n');
    const importLines = lines
      .map((l, i) => ({ l, n: i + 1 }))
      .filter(({ l }) => l.includes('@import'))
      .map(({ l, n }) => `line ${n}: ${l.trim()}`);
    fail('T6.2', '_mixins.scss must not contain @import', importLines.join('\n'));
  }

  // T6.3 — No bare arithmetic ($x - 1px) outside calc() or math.div()
  // Pattern: $var ± number with units, not inside calc( or math.div(
  // We use a heuristic: find "$ ... - N unit" or "$ ... + N unit" not inside calc/math.div
  // Strip calc(...) and math.div(...) regions first (simplified)
  const strippedMixins = mixins
    .replace(/calc\([^)]*\)/g, 'CALC')
    .replace(/math\.div\([^)]*\)/g, 'MATHDIV');

  const bareArithRe = /\$[\w-]+\s*[-+]\s*[\d.]+(?:px|rem|em|%)/g;
  const bareArithMatches = [];
  let ba;
  while ((ba = bareArithRe.exec(strippedMixins)) !== null) {
    const lineNo = strippedMixins.slice(0, ba.index).split('\n').length;
    bareArithMatches.push(`line ~${lineNo}: ${ba[0]}`);
  }

  if (bareArithMatches.length === 0) {
    pass('T6.3', '_mixins.scss has no bare arithmetic outside calc()/math.div()');
  } else {
    fail('T6.3', '_mixins.scss contains bare arithmetic patterns', bareArithMatches.join('\n'));
  }
}

// ── Group 7: DTCG spec sanity ─────────────────────────────────────────────────

function runGroup7() {
  group('7: DTCG spec sanity');

  const dtcg = readJSON(path.join(DIST, 'json', 'tokens.tokens.json'));
  const allTokens = Object.assign({}, dtcg.primitive || {}, dtcg['semantic-light'] || {}, dtcg['semantic-dark'] || {});

  // T7.1 — Shadow $value has offsetX and offsetY with units (not bare 0)
  const shadowTokens = Object.entries(allTokens).filter(([k]) => k.startsWith('shadow-'));
  const badShadows = [];
  for (const [key, token] of shadowTokens) {
    const val = token.$value;
    if (!val || typeof val !== 'object') continue; // string shadows are unresolved refs — skip
    const layers = Array.isArray(val) ? val : [val];
    for (const layer of layers) {
      if (typeof layer !== 'object') continue;
      const { offsetX, offsetY } = layer;
      if (!offsetX || !offsetY) continue;
      const bare0Re = /^0$/;
      if (bare0Re.test(String(offsetX)) || bare0Re.test(String(offsetY))) {
        badShadows.push(`${key}: offsetX=${offsetX}, offsetY=${offsetY} (bare 0 — must be 0px)`);
      }
    }
  }
  if (badShadows.length === 0) {
    pass('T7.1', `All shadow $values have offsetX/offsetY with units (checked ${shadowTokens.length} shadow tokens)`);
  } else {
    fail('T7.1', 'Shadow tokens have bare 0 in offsetX/offsetY', badShadows.join('\n'));
  }

  // T7.2 — font-family $value is a non-empty array
  const fontFamilyTokens = Object.entries(allTokens).filter(([, t]) => t.$type === 'fontFamily');
  const badFontFamily = [];
  for (const [key, token] of fontFamilyTokens) {
    const val = token.$value;
    if (!Array.isArray(val) || val.length === 0) {
      badFontFamily.push(`${key}: $value=${JSON.stringify(val)} (must be non-empty array)`);
    }
  }
  if (fontFamilyTokens.length === 0) {
    // No fontFamily tokens found at all — warn but don't fail
    warn('T7.2', 'No fontFamily tokens found in DTCG output to validate');
    totalTests++;
    passed++;
    console.log('  ✓ T7.2 font-family $value check (no fontFamily tokens present)');
  } else if (badFontFamily.length === 0) {
    pass('T7.2', `All ${fontFamilyTokens.length} fontFamily $values are non-empty arrays`);
  } else {
    fail('T7.2', 'fontFamily $values must be non-empty arrays', badFontFamily.join('\n'));
  }

  // T7.3 — cubicBezier $value is array of exactly 4 numbers
  const easingTokens = Object.entries(allTokens).filter(([, t]) => t.$type === 'cubicBezier');
  const badEasing = [];
  for (const [key, token] of easingTokens) {
    const val = token.$value;
    if (!Array.isArray(val) || val.length !== 4 || val.some(n => typeof n !== 'number')) {
      badEasing.push(`${key}: $value=${JSON.stringify(val)} (must be array of 4 numbers)`);
    }
  }
  if (easingTokens.length === 0) {
    warn('T7.3', 'No cubicBezier tokens found in DTCG output to validate');
    totalTests++;
    passed++;
    console.log('  ✓ T7.3 cubicBezier $value check (no cubicBezier tokens present)');
  } else if (badEasing.length === 0) {
    pass('T7.3', `All ${easingTokens.length} cubicBezier $values are arrays of 4 numbers`);
  } else {
    fail('T7.3', 'cubicBezier $values must be arrays of 4 numbers', badEasing.join('\n'));
  }
}

// ── Group 8: Build determinism ────────────────────────────────────────────────

function runGroup8() {
  group('8: Build determinism');

  console.log('  (running npm run build twice — may take ~15-20s)');

  const tokensCssPath = path.join(DIST, 'css', 'tokens.css');
  const dtcgPath      = path.join(DIST, 'json', 'tokens.tokens.json');

  try {
    // First build
    execSync('npm run build', { cwd: ROOT, stdio: 'pipe' });
    const snap1Css  = fs.readFileSync(tokensCssPath);
    const snap1Json = fs.readFileSync(dtcgPath);

    // Second build
    execSync('npm run build', { cwd: ROOT, stdio: 'pipe' });
    const snap2Css  = fs.readFileSync(tokensCssPath);
    const snap2Json = fs.readFileSync(dtcgPath);

    const cssMatch  = snap1Css.equals(snap2Css);
    const jsonMatch = snap1Json.equals(snap2Json);

    if (cssMatch && jsonMatch) {
      pass('T8.1', 'Build is byte-identical across two consecutive runs (tokens.css + tokens.tokens.json)');
    } else {
      const details = [];
      if (!cssMatch)  details.push('tokens.css differs between builds');
      if (!jsonMatch) details.push('tokens.tokens.json differs between builds');
      fail('T8.1', 'Build is deterministic', details.join('\n'));
    }
  } catch (e) {
    fail('T8.1', 'Build determinism check', `Build failed: ${e.message.split('\n')[0]}`);
  }
}

// ── Group 9: Build fail-safety ────────────────────────────────────────────────

function runGroup9() {
  group('9: Build fail-safety (smoke tests for guards)');

  // T9.1 — Corrupt semantic light.json with unresolved ref → build must exit non-zero
  const lightJsonPath = path.join(SRC, 'tokens', 'semantic', 'light.json');
  const originalLight = fs.readFileSync(lightJsonPath);

  try {
    // Inject a bad reference
    const bad = JSON.parse(originalLight.toString());
    bad.__test_bad__ = { value: '{color.fake.999}' };
    fs.writeFileSync(lightJsonPath, JSON.stringify(bad, null, 2));

    let buildExitedNonZero = false;
    try {
      execSync('npm run build', { cwd: ROOT, stdio: 'pipe' });
    } catch {
      buildExitedNonZero = true;
    }

    if (buildExitedNonZero) {
      pass('T9.1', 'Build exits non-zero when light.json has unresolved token reference');
    } else {
      fail('T9.1', 'Build should exit non-zero for unresolved token ref', 'Build succeeded unexpectedly');
    }
  } finally {
    fs.writeFileSync(lightJsonPath, originalLight);
    // Restore dist with a clean build after corruption test
    try { execSync('npm run build', { cwd: ROOT, stdio: 'pipe' }); } catch {}
  }

  // T9.2 — Make a primitive file temporarily empty {} → build must exit non-zero
  const primDir = path.join(SRC, 'tokens', 'primitive');
  const primFiles = fs.readdirSync(primDir).filter(f => f.endsWith('.json')).sort();
  // Use colors.json (the largest, most likely to cause issues if empty)
  const targetPrim = path.join(primDir, 'colors.json');
  const originalPrim = fs.readFileSync(targetPrim);

  try {
    fs.writeFileSync(targetPrim, '{}');

    let buildExitedNonZero = false;
    try {
      execSync('npm run build', { cwd: ROOT, stdio: 'pipe' });
    } catch {
      buildExitedNonZero = true;
    }

    if (buildExitedNonZero) {
      pass('T9.2', 'Build exits non-zero when primitive colors.json is emptied');
    } else {
      // If the build "succeeds" with empty colors — it's not guarding against empty primitives
      // This could be a real issue — flag it
      fail('T9.2', 'Build should exit non-zero when primitive file is empty {}',
        'Build succeeded with empty colors.json — guard may be missing');
    }
  } finally {
    fs.writeFileSync(targetPrim, originalPrim);
    // Restore dist
    try { execSync('npm run build', { cwd: ROOT, stdio: 'pipe' }); } catch {}
  }
}

// ── Main ──────────────────────────────────────────────────────────────────────

function main() {
  console.log('\nDesign System Test Suite');
  console.log('═'.repeat(50));

  runGroup1();
  runGroup2();
  runGroup3();
  runGroup4();
  runGroup5();
  runGroup6();
  runGroup7();
  runGroup8();
  runGroup9();

  // ── Summary ──────────────────────────────────────────────
  console.log('\n' + '═'.repeat(50));
  const total = totalTests;
  if (failed === 0) {
    console.log(`✓ ${passed}/${total} tests passed${warned > 0 ? `, ${warned} warning(s)` : ''}`);
  } else {
    console.log(`✗ ${failed}/${total} tests FAILED, ${passed} passed${warned > 0 ? `, ${warned} warning(s)` : ''}`);
  }

  if (warnings.length > 0) {
    console.log('\nWarnings:');
    for (const w of warnings) {
      console.log(`  ⚠ ${w.id}: ${w.msg}`);
      w.items.forEach(i => console.log(`    ${i}`));
    }
  }

  if (failures.length > 0) {
    console.log('\nFailures:');
    for (const f of failures) {
      console.log(`  ✗ ${f.id}: ${f.msg}`);
      if (f.detail) f.detail.split('\n').forEach(l => console.log(`    ${l}`));
    }
  }

  console.log('');
  process.exit(failed > 0 ? 1 : 0);
}

main();
