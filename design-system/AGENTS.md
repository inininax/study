# Repository Guidelines

## Project Structure & Module Organization
Core source files live under `src/`.
- `src/tokens/primitive/*.json`: raw token scales (color, spacing, typography, motion, etc.).
- `src/tokens/semantic/{light,dark}.json`: theme-level semantic aliases.
- `src/components/*.css`: component styles (button, modal, table, etc.).
- `src/layouts/*.css`: grid and stack layout utilities.
- `src/css/*.css`: shared layers such as reset, utilities, and animations.
- `src/scss/`: SCSS entry and mixins.

Generated artifacts are written to `dist/` (`css/`, `scss/`, `json/`, `js/`). Do not hand-edit generated files; modify `src/` or `scripts/build-tokens.cjs` instead.

## Build, Test, and Development Commands
- `npm install`: install dependencies (minimal; build is pure Node).
- `npm run build`: rebuild all distributable assets from `src/` into `dist/`.
- `npm run prepublishOnly`: runs build before publishing.

Example local workflow:
```bash
npm run build
open examples/index.html
```
Use `examples/index.html` for quick manual verification of token and component output.

## Coding Style & Naming Conventions
- Use 2-space indentation in JSON, JS/CJS, SCSS, and CSS.
- Keep token keys lowercase and hyphenated (for example `spacing-4`, `color-neutral-500`).
- Semantic token references should use token-path syntax in braces (for example `{color.neutral.100}`).
- Prefer `ds-` prefixed CSS classes for public component/layout APIs.
- Keep files ASCII unless an existing file already uses other characters.

## Testing Guidelines
There is no dedicated automated test suite yet. Every change should include:
- Successful `npm run build`.
- Manual check in `examples/index.html`.
- Verification that generated outputs in `dist/` reflect intended changes.

If you add automated tests, place them in a top-level `tests/` directory and use `*.test.*` naming.

## Commit & Pull Request Guidelines
Follow Conventional Commit style seen in history:
- `feat: ...`, `fix: ...`, `docs: ...`, `chore: ...`.

PRs should include:
- Clear summary of what changed and why.
- Affected paths (for example `src/tokens/primitive/colors.json`).
- Screenshots or short recordings for visual component/layout changes.
- Notes on manual verification steps performed.
