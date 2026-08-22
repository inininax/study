# GitHub Copilot instructions

Read **[AGENTS.md](../AGENTS.md)** at the repository root first — it is the single source of truth for this repo (project structure, build commands, architecture notes, and gotchas).

Key rules:
- Each top-level directory is a self-contained project with its own toolchain; there is no shared root build system — work inside the relevant sub-project directory.
- Do not "fix" intentionally broken teaching fixtures (e.g. `k8s-study/examples/09-troubleshooting/*`).
- Era-pinned legacy toolchains (`webpack-gulp-study/`, `webpack-study/`) are historical snapshots — do not modernize unless asked.
