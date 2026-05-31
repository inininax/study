#!/usr/bin/env node

/**
 * Design System — Token Build Pipeline (v2)
 *
 * Reads primitive and semantic token JSON files from src/tokens/
 * and outputs:
 *   - dist/css/tokens.css           (CSS Custom Properties, light + dark)
 *   - dist/css/tokens-light.css     (Light mode only)
 *   - dist/css/tokens-dark.css      (Dark mode only)
 *   - dist/css/reset.css            (Copy)
 *   - dist/css/utilities.css        (Copy)
 *   - dist/json/primitives.json     (Merged primitive tokens — nested)
 *   - dist/json/semantic.json       (Merged semantic tokens — nested)
 *   - dist/json/flat-primitives.json
 *   - dist/json/flat-light.json
 *   - dist/json/flat-dark.json
 *   - dist/json/tokens.tokens.json  (W3C DTCG format)
 *   - dist/js/tokens.js             (ESM export)
 *   - dist/js/tokens.cjs            (CJS export)
 *   - dist/js/tokens.d.ts           (TypeScript declarations)
 *   - dist/scss/_tokens.scss        (Auto-generated SCSS variables & maps)
 *   - dist/scss/_mixins.scss        (Copy)
 *   - dist/scss/index.scss          (Copy)
 */

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SRC = path.join(ROOT, 'src');
const DIST = path.join(ROOT, 'dist');

const BUILD_TIMESTAMP = process.env.DS_BUILD_TIMESTAMP || 'latest';

// ── Helpers ───────────────────────────────────────────────

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function readJSON(filePath) {
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch (err) {
    throw new Error(`Failed to parse ${path.relative(ROOT, filePath)}: ${err.message}`);
  }
}

function copyFile(src, dest) {
  fs.copyFileSync(src, dest);
}

/** Flatten nested tokens to hyphen-separated keys. Preserves original types (number, string). */
function flattenTokens(obj, prefix = '', separator = '-') {
  const result = {};
  for (const [key, val] of Object.entries(obj)) {
    const newKey = prefix ? `${prefix}${separator}${key}` : key;
    if (val && typeof val === 'object' && !Array.isArray(val)) {
      if ('value' in val) {
        result[newKey] = val.value;
      } else {
        Object.assign(result, flattenTokens(val, newKey, separator));
      }
    }
  }
  return result;
}

/**
 * Sort flat token map by key with natural numeric ordering.
 * Ensures spacing-0, spacing-0-5, spacing-1, spacing-1-5, spacing-2, ...
 */
function sortTokenMap(flatMap) {
  const sorted = {};
  const keys = Object.keys(flatMap).sort((a, b) => {
    const partsA = a.split('-');
    const partsB = b.split('-');
    const len = Math.max(partsA.length, partsB.length);
    for (let i = 0; i < len; i++) {
      const pA = partsA[i] || '';
      const pB = partsB[i] || '';
      const nA = Number(pA);
      const nB = Number(pB);
      const aIsNum = pA !== '' && !isNaN(nA);
      const bIsNum = pB !== '' && !isNaN(nB);
      if (aIsNum && bIsNum) {
        if (nA !== nB) return nA - nB;
      } else {
        const cmp = pA.localeCompare(pB);
        if (cmp !== 0) return cmp;
      }
    }
    return 0;
  });
  for (const key of keys) {
    sorted[key] = flatMap[key];
  }
  return sorted;
}

/**
 * Resolve token references like "{color.neutral.100}"
 * Looks up the primitive flat map for the raw value.
 */
function resolveReferences(flatTokens, primitiveFlatMap) {
  const resolved = {};
  for (const [key, val] of Object.entries(flatTokens)) {
    if (typeof val === 'string' && val.startsWith('{') && val.endsWith('}')) {
      const ref = val.slice(1, -1).replace(/\./g, '-');
      resolved[key] = primitiveFlatMap[ref] !== undefined ? primitiveFlatMap[ref] : val;
    } else {
      resolved[key] = val;
    }
  }
  const unresolved = Object.entries(resolved).filter(
    ([, v]) => typeof v === 'string' && v.startsWith('{') && v.endsWith('}')
  );
  if (unresolved.length > 0) {
    console.error('\n✗ Unresolved token references:');
    unresolved.forEach(([k, v]) => console.error(`    ${k} → ${v}`));
    process.exit(1);
  }
  return resolved;
}

// ── Load Tokens ───────────────────────────────────────────

function loadPrimitives() {
  const dir = path.join(SRC, 'tokens', 'primitive');
  const merged = {};
  for (const file of fs.readdirSync(dir).filter(f => f.endsWith('.json')).sort()) {
    const data = readJSON(path.join(dir, file));
    for (const key of Object.keys(data)) {
      if (key in merged) {
        console.warn(`⚠ Duplicate top-level primitive key "${key}" in ${file} — overwriting previous value`);
      }
    }
    Object.assign(merged, data);
  }
  return merged;
}

function loadSemantic(mode) {
  return readJSON(path.join(SRC, 'tokens', 'semantic', `${mode}.json`));
}

// ── Generate CSS Custom Properties ────────────────────────

function toCSSValue(val) {
  return String(val);
}

function toCSSVars(flatMap, indent = '  ') {
  return Object.entries(flatMap)
    .map(([key, val]) => `${indent}--${key}: ${toCSSValue(val)};`)
    .join('\n');
}

function buildCSS(primitiveFlatMap, lightFlatMap, darkFlatMap) {
  const primitiveVars = toCSSVars(primitiveFlatMap);
  const lightVars = toCSSVars(lightFlatMap);
  const darkVars = toCSSVars(darkFlatMap);

  const combined = `/* ============================================================
   Design System — CSS Custom Properties
   Generated at: ${BUILD_TIMESTAMP}
   ============================================================ */

/* Primitive tokens */
:root {
${primitiveVars}
}

/* Semantic tokens — Light mode (default) */
:root,
[data-theme="light"] {
${lightVars}
}

/* Semantic tokens — Dark mode */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
${toCSSVars(darkFlatMap, '    ')}
  }
}

[data-theme="dark"] {
${darkVars}
}
`;

  const lightOnly = `/* Design System — Light Mode Tokens */
:root {
${primitiveVars}
${lightVars}
}
`;

  const darkOnly = `/* Design System — Dark Mode Tokens */
:root {
${primitiveVars}
${darkVars}
}
`;

  return { combined, lightOnly, darkOnly };
}

// ── Generate JS/TS ────────────────────────────────────────

function toCamelCase(key) {
  return key.replace(/-([a-z0-9])/g, (_, c) => c.toUpperCase());
}

function jsLiteral(val) {
  if (typeof val === 'number') return String(val);
  return JSON.stringify(String(val));
}

function tsType(val) {
  return typeof val === 'number' ? 'number' : 'string';
}

function buildJS(primitiveFlatMap, lightFlatMap, darkFlatMap) {
  const toJSObject = (map) => {
    const entries = Object.entries(map)
      .map(([key, val]) => {
        const camelKey = toCamelCase(key);
        return `  ${JSON.stringify(camelKey)}: ${jsLiteral(val)}`;
      })
      .join(',\n');
    return `{\n${entries}\n}`;
  };

  const timestamp = BUILD_TIMESTAMP;

  const esm = `// Design System — Token Constants (ESM)
// Generated at: ${timestamp}

export const primitives = ${toJSObject(primitiveFlatMap)};

export const light = ${toJSObject(lightFlatMap)};

export const dark = ${toJSObject(darkFlatMap)};

export const tokens = { primitives, light, dark };
export default tokens;
`;

  const cjs = `// Design System — Token Constants (CJS)
// Generated at: ${timestamp}

const primitives = ${toJSObject(primitiveFlatMap)};

const light = ${toJSObject(lightFlatMap)};

const dark = ${toJSObject(darkFlatMap)};

const tokens = { primitives, light, dark };

module.exports = tokens;
module.exports.primitives = primitives;
module.exports.light = light;
module.exports.dark = dark;
module.exports.tokens = tokens;
module.exports.default = tokens;
`;

  const buildInterface = (name, map) => {
    const entries = Object.entries(map)
      .map(([key, val]) => `  readonly ${JSON.stringify(toCamelCase(key))}: ${tsType(val)};`)
      .join('\n');
    return `export interface ${name} {\n${entries}\n}`;
  };

  const dts = `// Design System — Token Type Declarations
// Generated at: ${timestamp}

${buildInterface('PrimitiveTokens', primitiveFlatMap)}

${buildInterface('LightSemanticTokens', lightFlatMap)}

${buildInterface('DarkSemanticTokens', darkFlatMap)}

export declare const primitives: PrimitiveTokens;
export declare const light: LightSemanticTokens;
export declare const dark: DarkSemanticTokens;

export interface DesignTokens {
  primitives: PrimitiveTokens;
  light: LightSemanticTokens;
  dark: DarkSemanticTokens;
}

export declare const tokens: DesignTokens;
export default tokens;
`;

  return { esm, cjs, dts };
}

// ── Generate SCSS (auto-generated from JSON) ─────────────

function buildSCSS(primitives, primitiveFlatMap) {
  const lines = [];
  lines.push('// ============================================================');
  lines.push('// Design System — SCSS Token Variables');
  lines.push(`// Auto-generated by build-tokens.cjs — DO NOT EDIT`);
  lines.push('// ============================================================');
  lines.push('');

  // Group tokens by top-level category
  const categories = {};
  for (const [key, val] of Object.entries(primitiveFlatMap)) {
    const cat = key.split('-')[0];
    if (!categories[cat]) categories[cat] = [];
    categories[cat].push([key, val]);
  }

  // Helper: format SCSS value
  const scssVal = (val) => {
    if (typeof val === 'number') return String(val);
    return val;
  };

  // Generate individual variables per category
  for (const [cat, entries] of Object.entries(categories)) {
    const title = cat.charAt(0).toUpperCase() + cat.slice(1);
    lines.push(`// ── ${title} ${'─'.repeat(Math.max(1, 55 - title.length))}`);

    for (const [key, val] of entries) {
      lines.push(`$${key}: ${scssVal(val)};`);
    }
    lines.push('');
  }

  // Generate maps for key categories
  const mapCategories = {
    'font-size': { prefix: 'font-size-', mapName: '$font-sizes' },
    'spacing': { prefix: 'spacing-', mapName: '$spacings' },
    'breakpoint': { prefix: 'breakpoint-', mapName: '$breakpoints' },
    'radius': { prefix: 'radius-', mapName: '$radii' },
    'z-index': { prefix: 'z-index-', mapName: '$z-indexes' },
    'opacity': { prefix: 'opacity-', mapName: '$opacities' },
    'duration': { prefix: 'duration-', mapName: '$durations' },
  };

  lines.push('// ── Maps ─────────────────────────────────────────────────');
  lines.push('');

  for (const [category, config] of Object.entries(mapCategories)) {
    const mapEntries = Object.entries(primitiveFlatMap)
      .filter(([key]) => key.startsWith(config.prefix))
      .map(([key, val]) => {
        const mapKey = key.slice(config.prefix.length);
        return `  '${mapKey}': $${key}`;
      });

    if (mapEntries.length > 0) {
      lines.push(`${config.mapName}: (`);
      lines.push(mapEntries.join(',\n') + ',');
      lines.push(');');
      lines.push('');
    }
  }

  // Color maps (nested by palette)
  const colorPalettes = {};
  for (const [key, val] of Object.entries(primitiveFlatMap)) {
    if (!key.startsWith('color-')) continue;
    const parts = key.split('-');
    if (parts.length !== 3) continue; // only palette-shade entries
    const palette = parts[1];
    if (!colorPalettes[palette]) colorPalettes[palette] = [];
    colorPalettes[palette].push([parts[2], val]);
  }

  for (const [palette, entries] of Object.entries(colorPalettes)) {
    if (entries.length < 3) continue; // skip white, black (single values)
    lines.push(`$colors-${palette}: (`);
    const mapEntries = entries.map(([shade, val]) => `  '${shade}': ${val}`);
    lines.push(mapEntries.join(',\n') + ',');
    lines.push(');');
    lines.push('');
  }

  return lines.join('\n');
}

// ── Generate W3C DTCG Format ─────────────────────────────

function inferDTCGType(key, val) {
  if (key.startsWith('color-') || (typeof val === 'string' && val.startsWith('#'))) return 'color';
  if (key.startsWith('font-family')) return 'fontFamily';
  if (key.startsWith('font-weight')) return 'fontWeight';
  if (key.startsWith('font-size') || key.startsWith('spacing-') || key.startsWith('radius-') || key.startsWith('border-width-') || key.startsWith('container-') || key.startsWith('breakpoint-') || key.startsWith('letter-spacing')) return 'dimension';
  if (key.startsWith('line-height') || key.startsWith('opacity-')) return 'number';
  if (key.startsWith('z-index-')) return 'number';
  if (key.startsWith('duration-')) return 'duration';
  if (key.startsWith('easing-')) return 'cubicBezier';
  if (key.startsWith('shadow-')) return 'shadow';
  if (key.startsWith('focus-ring-width') || key.startsWith('focus-ring-offset')) return 'dimension';
  return undefined;
}

function ensureUnit(v) {
  if (v === undefined || v === null) return '0px';
  return v === '0' ? '0px' : v;
}

function parseShadowLayer(s) {
  const trimmed = s.trim();
  // Match: offsetX offsetY blur [spread] rgba(...)
  const match = trimmed.match(/^([\d.-]+(?:px)?)\s+([\d.-]+(?:px)?)\s+([\d.-]+(?:px)?)\s+(?:([\d.-]+(?:px)?)\s+)?(rgba?\([^)]+\))$/);
  if (match) {
    return {
      offsetX: ensureUnit(match[1]),
      offsetY: ensureUnit(match[2]),
      blur: ensureUnit(match[3]),
      spread: ensureUnit(match[4] || '0px'),
      color: match[5]
    };
  }
  return trimmed;
}

function splitShadowLayers(val) {
  // Split on "), " followed by a digit — separates multi-layer shadows
  // without breaking inside rgba() parentheses
  const parts = val.split(/\),\s*(?=\d)/);
  return parts.map((p, i) => i < parts.length - 1 ? p + ')' : p);
}

function toDTCGValue(key, val, type) {
  if (type === 'fontFamily' && typeof val === 'string') {
    return val.split(',').map(s => s.trim().replace(/^['"]|['"]$/g, ''));
  }
  if (type === 'cubicBezier' && typeof val === 'string') {
    if (val === 'linear') return [0, 0, 1, 1];
    const match = val.match(/cubic-bezier\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*\)/);
    if (match) return [parseFloat(match[1]), parseFloat(match[2]), parseFloat(match[3]), parseFloat(match[4])];
  }
  if (type === 'duration' && typeof val === 'string') {
    const ms = parseInt(val, 10);
    return `${ms}ms`;
  }
  if (type === 'shadow' && typeof val === 'string') {
    const layers = splitShadowLayers(val);
    const parsed = layers.map(parseShadowLayer);
    return parsed.length === 1 ? parsed[0] : parsed;
  }
  return val;
}

function buildDTCG(primitiveFlatMap, lightFlatMap, darkFlatMap) {
  const dtcg = {};

  const addTokens = (flatMap, groupName) => {
    const group = {};
    for (const [key, val] of Object.entries(flatMap)) {
      const type = inferDTCGType(key, val);
      const token = {
        $value: toDTCGValue(key, val, type)
      };
      if (type) token.$type = type;
      group[key] = token;
    }
    dtcg[groupName] = group;
  };

  addTokens(primitiveFlatMap, 'primitive');
  addTokens(lightFlatMap, 'semantic-light');
  addTokens(darkFlatMap, 'semantic-dark');

  return JSON.stringify(dtcg, null, 2);
}

// ── Main ──────────────────────────────────────────────────

function main() {
  console.log('Building design system tokens...\n');

  // Load & flatten
  const primitives = loadPrimitives();
  const primitiveFlatMap = sortTokenMap(flattenTokens(primitives));

  // P1-3: Sanity-check primitive token count
  const primCount = Object.keys(primitiveFlatMap).length;
  if (primCount < 50) {
    console.error(`✗ Suspiciously few primitive tokens (${primCount}). Check src/tokens/primitive/*.json for empty or malformed files.`);
    process.exit(1);
  }

  // P1-5: Validate breakpoint token/CSS drift
  const expectedBreakpoints = ['sm', 'md', 'lg', 'xl', '2xl'].reduce((acc, bp) => {
    const v = primitiveFlatMap[`breakpoint-${bp}`];
    if (v) acc[bp] = v;
    return acc;
  }, {});
  const gridCSS = fs.readFileSync(path.join(SRC, 'layouts', 'grid.css'), 'utf8');
  const utilCSS = fs.readFileSync(path.join(SRC, 'css', 'utilities.css'), 'utf8');
  const drift = [];
  for (const [name, val] of Object.entries(expectedBreakpoints)) {
    const escapedVal = val.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const needle = new RegExp(`min-width:\\s*${escapedVal}`);
    if (!needle.test(gridCSS) && !needle.test(utilCSS)) {
      drift.push(`breakpoint-${name} (${val})`);
    }
  }
  if (drift.length > 0) {
    console.error(`\n✗ Breakpoint token/CSS drift — not used in grid.css or utilities.css:`);
    drift.forEach(d => console.error(`    ${d}`));
    process.exit(1);
  }

  const lightSemantic = loadSemantic('light');
  const darkSemantic = loadSemantic('dark');

  const lightFlat = sortTokenMap(resolveReferences(flattenTokens(lightSemantic), primitiveFlatMap));
  const darkFlat = sortTokenMap(resolveReferences(flattenTokens(darkSemantic), primitiveFlatMap));

  // Ensure dist directories
  ['css', 'scss', 'json', 'js'].forEach(d => ensureDir(path.join(DIST, d)));

  // Generate CSS
  const { combined, lightOnly, darkOnly } = buildCSS(primitiveFlatMap, lightFlat, darkFlat);
  fs.writeFileSync(path.join(DIST, 'css', 'tokens.css'), combined);
  fs.writeFileSync(path.join(DIST, 'css', 'tokens-light.css'), lightOnly);
  fs.writeFileSync(path.join(DIST, 'css', 'tokens-dark.css'), darkOnly);
  console.log('  ✓ CSS tokens generated');

  // Copy static CSS files
  copyFile(path.join(SRC, 'css', 'reset.css'), path.join(DIST, 'css', 'reset.css'));
  copyFile(path.join(SRC, 'css', 'utilities.css'), path.join(DIST, 'css', 'utilities.css'));
  copyFile(path.join(SRC, 'css', 'animations.css'), path.join(DIST, 'css', 'animations.css'));
  console.log('  ✓ CSS reset, utilities & animations copied');

  // Bundle component CSS
  const componentsDir = path.join(SRC, 'components');
  const componentFiles = fs.readdirSync(componentsDir).filter(f => f.endsWith('.css')).sort();
  const componentCSS = componentFiles.map(f => {
    return `/* ── ${f.replace('.css', '')} ─────────────────────────────────── */\n` +
           fs.readFileSync(path.join(componentsDir, f), 'utf8');
  }).join('\n\n');
  const componentsBanner = `/* ============================================================\n   Design System — Component Styles\n   Generated at: ${BUILD_TIMESTAMP}\n   Components: ${componentFiles.map(f => f.replace('.css', '')).join(', ')}\n   ============================================================ */\n\n`;
  fs.writeFileSync(path.join(DIST, 'css', 'components.css'), componentsBanner + componentCSS);
  // Also copy individual component files
  ensureDir(path.join(DIST, 'css', 'components'));
  componentFiles.forEach(f => copyFile(path.join(componentsDir, f), path.join(DIST, 'css', 'components', f)));
  console.log(`  ✓ ${componentFiles.length} component CSS files bundled`);

  // Bundle layout CSS
  const layoutsDir = path.join(SRC, 'layouts');
  const layoutFiles = fs.readdirSync(layoutsDir).filter(f => f.endsWith('.css')).sort();
  const layoutCSS = layoutFiles.map(f => {
    return `/* ── ${f.replace('.css', '')} ─────────────────────────────────── */\n` +
           fs.readFileSync(path.join(layoutsDir, f), 'utf8');
  }).join('\n\n');
  const layoutsBanner = `/* ============================================================\n   Design System — Layout System\n   Generated at: ${BUILD_TIMESTAMP}\n   ============================================================ */\n\n`;
  fs.writeFileSync(path.join(DIST, 'css', 'layouts.css'), layoutsBanner + layoutCSS);
  console.log(`  ✓ ${layoutFiles.length} layout CSS files bundled`);

  // Generate all-in-one bundle
  const allCSS = [
    combined,
    fs.readFileSync(path.join(SRC, 'css', 'reset.css'), 'utf8'),
    fs.readFileSync(path.join(SRC, 'css', 'utilities.css'), 'utf8'),
    fs.readFileSync(path.join(SRC, 'css', 'animations.css'), 'utf8'),
    layoutCSS,
    componentCSS
  ].join('\n\n');
  const allBanner = `/* ============================================================\n   Design System — All-in-One Bundle\n   Includes: tokens + reset + utilities + animations + layouts + components\n   Generated at: ${BUILD_TIMESTAMP}\n   ============================================================ */\n\n`;
  fs.writeFileSync(path.join(DIST, 'css', 'all.css'), allBanner + allCSS);
  console.log('  ✓ All-in-one CSS bundle generated');

  // Generate SCSS (auto-generated from tokens)
  const scssTokens = buildSCSS(primitives, primitiveFlatMap);
  fs.writeFileSync(path.join(DIST, 'scss', '_tokens.scss'), scssTokens);
  // Copy hand-authored SCSS files
  copyFile(path.join(SRC, 'scss', '_mixins.scss'), path.join(DIST, 'scss', '_mixins.scss'));
  copyFile(path.join(SRC, 'scss', 'index.scss'), path.join(DIST, 'scss', 'index.scss'));
  console.log('  ✓ SCSS generated & copied');

  // Generate JSON
  fs.writeFileSync(
    path.join(DIST, 'json', 'primitives.json'),
    JSON.stringify(primitives, null, 2)
  );
  fs.writeFileSync(
    path.join(DIST, 'json', 'semantic.json'),
    JSON.stringify({ light: lightSemantic, dark: darkSemantic }, null, 2)
  );
  fs.writeFileSync(
    path.join(DIST, 'json', 'flat-primitives.json'),
    JSON.stringify(primitiveFlatMap, null, 2)
  );
  fs.writeFileSync(
    path.join(DIST, 'json', 'flat-light.json'),
    JSON.stringify(lightFlat, null, 2)
  );
  fs.writeFileSync(
    path.join(DIST, 'json', 'flat-dark.json'),
    JSON.stringify(darkFlat, null, 2)
  );
  console.log('  ✓ JSON tokens generated');

  // Generate DTCG
  const dtcg = buildDTCG(primitiveFlatMap, lightFlat, darkFlat);
  fs.writeFileSync(path.join(DIST, 'json', 'tokens.tokens.json'), dtcg);
  console.log('  ✓ DTCG tokens generated');

  // Generate JS/TS (ESM + CJS + type declarations)
  const { esm, cjs, dts } = buildJS(primitiveFlatMap, lightFlat, darkFlat);
  fs.writeFileSync(path.join(DIST, 'js', 'tokens.js'), esm);
  fs.writeFileSync(path.join(DIST, 'js', 'tokens.cjs'), cjs);
  fs.writeFileSync(path.join(DIST, 'js', 'tokens.d.ts'), dts);
  console.log('  ✓ JS/TS tokens generated (ESM + CJS + .d.ts)');

  console.log('\nBuild complete!');

  // Summary
  const lightCount = Object.keys(lightFlat).length;
  const darkCount = Object.keys(darkFlat).length;
  console.log(`  Primitive tokens: ${primCount}`);
  console.log(`  Light semantic tokens: ${lightCount}`);
  console.log(`  Dark semantic tokens: ${darkCount}`);
  console.log(`  Total: ${primCount + lightCount + darkCount}`);
}

main();
