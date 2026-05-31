# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Verify

```bash
npm run build          # prebuild clears dist/, then runs scripts/build-tokens.cjs
npm run clean          # remove dist/ only
```

No dependencies to install — pure Node.js (>=16). The build script is `.cjs` because `package.json` has `"type": "module"`. There is no automated test suite; verify changes by running the build and opening `examples/index.html` in a browser to confirm token + component output (light and dark via `<html data-theme="dark">`).

`dist/` is fully generated. Never hand-edit anything under `dist/` — change the source in `src/` (or `scripts/build-tokens.cjs`) and rebuild.

**Build-time guarantees** (the script will exit non-zero on any of these):
- An unresolved `{token.path}` reference anywhere in semantic tokens
- A malformed JSON file (error message includes the source filename)
- A `breakpoint-*` primitive token whose value never appears in `src/layouts/grid.css` or `src/css/utilities.css` (drift detection — CSS `@media` cannot use custom properties, so both must be updated together)

Output is **deterministic** — no embedded build timestamps. Override the marker via `DS_BUILD_TIMESTAMP=<value> npm run build` if needed for release pipelines.

## Architecture

**5-Layer System** — each layer consumes the one below it:

```
Layer 5: Utilities + Animations    (src/css/utilities.css, animations.css)
Layer 4: Layout system             (src/layouts/grid.css, stack.css)
Layer 3: Component CSS (20)        (src/components/*.css)
Layer 2: Semantic tokens           (src/tokens/semantic/light.json, dark.json)
Layer 1: Primitive tokens          (src/tokens/primitive/*.json)
```

Light/dark mode switching is at Layer 2 only — Layers 3-5 inherit automatically via CSS custom properties.

**Build pipeline** (`scripts/build-tokens.cjs`):
1. Merges `src/tokens/primitive/*.json` → flat map with natural sort
2. Resolves `{color.neutral.100}` references in semantic tokens
3. Outputs 7 token formats: CSS, SCSS (auto-generated), JSON (nested+flat), DTCG, ESM, CJS, TypeScript
4. Bundles `src/components/*.css` → `dist/css/components.css` + individual files in `dist/css/components/`
5. Bundles `src/layouts/*.css` → `dist/css/layouts.css`
6. Generates `dist/css/all.css` (tokens+reset+utilities+animations+layouts+components)

**Token reference syntax**: `{color.neutral.100}` in semantic JSON — dot notation inside braces, resolved at build time against the flattened primitive map (dots become hyphens).

**Natural sort**: token keys are sorted with numeric awareness so `spacing-0`, `spacing-0-5`, `spacing-1`, `spacing-1-5`, `spacing-2` stay in the expected order. When adding fractional steps, use the `-N-M` pattern (e.g. `spacing-2-5`) — do not introduce a different separator.

## Key Conventions

- **CSS prefix**: `.ds-` on all classes (`.ds-btn`, `.ds-card`, `.ds-grid-cols-3`)
- **CSS variables**: `--color-neutral-50`, `--spacing-4` (hyphen-separated)
- **JS keys**: camelCase (`colorNeutral50`, `fontSizeBase`)
- **JSON keys**: kebab-case (CSS variable suffix)
- **Number types**: `font-weight`, `line-height`, `opacity`, `z-index` are `number` in JS/TS (not strings)
- **Dark mode**: both `prefers-color-scheme` media query AND `[data-theme="dark"]` attribute
- **Component variants**: modifier classes (`.ds-btn-primary`), sizes (`.ds-btn-sm`, `.ds-btn-lg`)
- **SCSS tokens auto-generated** — never edit `dist/scss/_tokens.scss`, edit JSON source instead
- **Form-control state selectors**: checkbox/radio/toggle each support BOTH the sibling pattern (`<input>` then `<label>`) and the wrapping pattern (`<label><input/>...</label>`). Always pair `:state +` with `:state ~` so checked/disabled/error styles render in both DOMs (see `src/components/checkbox.css`, `toggle.css`).
- **`src/components/checkbox.css` contains BOTH `.ds-checkbox` and `.ds-radio` rules** — there is no separate `radio.css`. Keep parallel changes in sync.

## Modifying

- **Tokens**: edit `src/tokens/primitive/*.json` or `src/tokens/semantic/*.json`, run build
- **Components**: edit/add CSS in `src/components/`, run build (auto-bundled into `dist/css/components.css` + per-file under `dist/css/components/`)
- **Layouts**: edit/add CSS in `src/layouts/`, run build (auto-bundled)
- **Utilities / animations / reset**: edit `src/css/utilities.css`, `src/css/animations.css`, `src/css/reset.css`, run build
- **SCSS mixins**: edit `src/scss/_mixins.scss` or `src/scss/index.scss` — these are copied as-is to `dist/scss/`. The token map in `dist/scss/_tokens.scss` is regenerated, never edit it.

When adding a semantic token referencing a primitive: `{"value": "{color.mocha.500}"}`.

## Package Exports

- `@myorg/design-system` → JS/TS tokens (ESM/CJS)
- `./css/all.css` → all-in-one bundle
- `./css/tokens.css` → CSS custom properties
- `./css/components.css` → all 20 components bundled
- `./css/components/*` → individual component files
- `./css/layouts.css` → grid + stack
- `./css/animations.css` → keyframe animations
- `./css/reset.css`, `./css/utilities.css`
- `./styles` → SCSS entry (`@use` with `@forward`)
- `./tokens/dtcg` → W3C DTCG format

## Versioning & Commits

SemVer: MAJOR = token renames/deletions/component API changes, MINOR = new tokens/components, PATCH = value tweaks. **Treat the shape of `dist/json/tokens.tokens.json` (DTCG export) as part of the public API** — changing field types there (e.g., string → array) is at minimum a MINOR bump even if the underlying tokens are unchanged.

Commits follow Conventional Commits as in history (`feat:`, `fix:`, `docs:`, `chore:`). Update `CHANGELOG.md` in the same commit when the change is user-visible. PRs touching components or layouts should include a screenshot/recording from `examples/index.html` plus the manual verification steps run.
