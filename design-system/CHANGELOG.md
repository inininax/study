# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [3.2.0] - 2026-05-03

### Added
- Semantic destructive interaction tokens: `--color-status-bg-destructive-hover` and `--color-status-bg-destructive-pressed` (different values in light vs dark for proper contrast)
- `:hover` border state on `.ds-input`, `.ds-select`, `.ds-textarea`
- `:disabled` / `[aria-disabled]` state on `.ds-accordion-trigger`
- `.ds-navbar-actions` flex container class for navbar right-side controls
- `picture` element added to media reset
- `scripts/test.cjs` — zero-dependency Node E2E test harness with 25 tests across 9 groups (artifact integrity, CSS-var graph, light/dark parity, examples coverage, variant matrix, SCSS sanity, DTCG spec, build determinism, build fail-safety smoke tests)
- `npm test` script wired up to the harness
- Build pipeline: warning when a primitive token JSON file overwrites a top-level key from another file
- Build pipeline: hard failure when fewer than 50 primitive tokens are loaded (catches empty/malformed primitive files)

### Fixed
- `.ds-btn-destructive` hover/active now uses semantic tokens instead of mode-invariant primitive `--color-red-700/800` — dark-mode rendering now uses brighter shades for proper contrast
- SCSS `breakpoint-down` mixin uses `calc(#{$value} - 1px)` instead of bare arithmetic (modern dart-sass strict-mode compatible)
- `examples/index.html` now exercises every one of the 20 components (was 7) — version header bumped to v3.1
- `examples/index.html` no longer references undefined classes (`ds-modal-title`, `ds-divider-label`, `ds-accordion-icon`, `ds-accordion-body` — replaced with the canonical class names)
- README claim "every component supports hover/focus/active/disabled + sm/lg" replaced with accurate breakdown
- README divider entry now correctly states "orientation variants" (not size)

## [3.1.0] - 2026-05-03

> Bumped to MINOR rather than PATCH because DTCG output shape changed under `./tokens/dtcg` (see "Changed" — spec-compliance correction). All other items are pure fixes/additions.

### Fixed
- Build script now fails fast on unresolved token references with a list of offenders
- Build script JSON parse errors include the source filename
- Build output is now deterministic (no embedded timestamps)
- Build script validates breakpoint drift between primitive tokens and grid/utilities CSS
- Removed duplicate `@keyframes ds-spin` from `button.css` (now sourced solely from `animations.css`)
- Replaced hardcoded hex colors in button destructive states with `var(--color-red-700/800)`
- Replaced hardcoded `rgba(0,0,0,0.06)` in alert close button with `var(--color-bg-surface)` for dark-mode parity
- Added `xl` display utilities and a complete `2xl` breakpoint set in grid layout
- Fixed checkbox/radio invisible-state bug (added `~` sibling selectors to support label-wraps-input pattern)
- `examples/index.html` rewritten to use real `.ds-*` component classes

### Changed
- **DTCG output (`./tokens/dtcg`) — spec-compliance correction (potentially breaking for downstream parsers)**:
  - `fontFamily` `$value` is now an array of family names per W3C DTCG spec (was a comma-separated string)
  - Shadow offsets (`offsetX`, `offsetY`, `blur`, `spread`) always include units; bare `"0"` is now `"0px"`
  - Consumers reading `dist/json/tokens.tokens.json` may need to update parsers if they relied on the previous (non-compliant) shapes

### Added
- `:root { interpolate-size: allow-keywords; }` in reset for future `auto`-height transitions
- `text-wrap: balance` on headings and `text-wrap: pretty` on paragraphs in reset

## [3.0.0] - 2026-03-28

### Added
- **Component CSS Layer**: 20 pre-built UI components (button, input, select, textarea, checkbox, radio, toggle, card, badge, alert, modal, avatar, divider, navbar, table, tabs, dropdown, accordion, progress, skeleton, tooltip)
- **Layout System**: 12-column CSS Grid with responsive variants (sm/md/lg/xl), Stack/HStack/Center/Cluster patterns
- **Animation Library**: 12 keyframe animations (fade, slide, scale, spin, pulse, bounce, skeleton-wave) with utility classes and reduced-motion support
- **All-in-One Bundle**: `dist/css/all.css` includes tokens + reset + utilities + animations + layouts + components
- **Individual Component Exports**: `dist/css/components/*.css` for tree-shaking imports
- **Responsive Grid Utilities**: `.ds-sm\:grid-cols-*`, `.ds-md\:grid-cols-*`, `.ds-lg\:*`, `.ds-xl\:*`
- **Responsive Display Utilities**: `.ds-sm\:flex`, `.ds-md\:hidden`, `.ds-lg\:block`, etc.

### Changed
- Package version bumped to 3.0.0 (component layer is a major addition)
- Build pipeline now bundles component CSS, layout CSS, and generates all.css
- Package exports expanded: `./css/all.css`, `./css/components.css`, `./css/components/*`, `./css/layouts.css`, `./css/animations.css`
- `files` field in package.json includes `src/components/` and `src/layouts/`

## [2.0.0] - 2026-03-28

### Added
- **New Primitive Tokens**: z-index (9 levels), opacity (12 steps), border-width (4 sizes)
- **Expanded Semantic Tokens**: 33 → 48 per theme — interactive states (default/hover/pressed/disabled/focus), focus ring (color/width/offset), tertiary text, brand bg/border, disabled states
- **SCSS Auto-Generation**: `dist/scss/_tokens.scss` auto-generated from JSON (all 9 color palette maps, 7 utility maps)
- **W3C DTCG Format**: `dist/json/tokens.tokens.json` with structured shadow objects and cubicBezier arrays
- **CSS Utilities Expanded**: ~90 → ~180 classes (z-index, opacity, border-width, half-step spacing, focus-ring, tablet-only, more responsive, more spacing variants)
- **Motion Tokens**: Added `duration.instant`, `easing.linear`, fixed `easing.in-out` duplicate

### Changed
- Build pipeline: preserves number types in JS/TS, natural sort ordering, SCSS auto-generation
- Dark mode: status-bg uses custom dark-safe hex values instead of 900 shades (better contrast)
- Package exports: styles → dist/scss, semantic → dist/json, added DTCG export
- Border utilities use `var(--border-width-thin)` instead of hardcoded `1px`
- Focus ring uses `--focus-ring-*` semantic tokens

### Removed
- `docs/DESIGN_SYSTEM_PLAN.md` — initial planning doc (implementation complete)
- `src/scss/_tokens.scss` — replaced by auto-generated version in dist

## [1.0.0] - 2026-03-28

### Added
- **Color System**: 9 color palettes (Neutral, Mocha, Terracotta, Teal, Sage, Blue, Red, Green, Amber) with 10-step scales based on 2025-2026 global color trends
- **Semantic Tokens**: Light and Dark mode token mappings (background, text, border, accent, status)
- **Typography System**: Pretendard font stack, 10-step type scale, font weights, line heights, letter spacing
- **Spacing System**: 4px base unit spacing scale (0-96px), breakpoints, container widths
- **Component Foundations**: Border radius, elevation shadows (light/dark), transitions, easing curves
- **CSS Custom Properties**: Auto-generated from token JSON files
- **CSS Reset**: Modern cross-platform reset optimized for WebView, Mobile Web, PC Web
- **Utility Classes**: Layout, typography, color, spacing, border, shadow utilities with `ds-` prefix
- **SCSS Module**: Tokens as SCSS variables/maps, mixins for responsive, typography, layout, dark mode
- **Multi-format Output**: CSS, SCSS, JSON, JavaScript/TypeScript
- **Build Pipeline**: Node.js token build script with automatic reference resolution
- **npm Package**: Configured for distribution via npm/git submodule/npm link
