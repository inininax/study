# AI Model Selection Guide

Last updated: 2026-05-03

## Purpose
This repository does not require AI tooling, but contributors often use coding assistants. This guide standardizes model choice by task so results are more consistent.

## Recommended Baseline
- Default for complex coding/refactoring: `gpt-5.5`
- Cost/latency-sensitive coding tasks: `gpt-5.4-mini`
- Hard bug hunts or architecture decisions: `gpt-5.2-pro` (or equivalent high-effort mode)

Rationale: OpenAI model docs currently position GPT-5.5/GPT-5.2 family as top choices for complex reasoning and coding-heavy tasks.

## Source of Truth
- https://developers.openai.com/api/docs/models
- https://platform.openai.com/docs/guides/latest-model

Review cadence: re-check model names and recommendations monthly.

## Task-to-Model Mapping
- Token/schema edits (`src/tokens/**`): `gpt-5.4-mini`
- Build pipeline changes (`scripts/build-tokens.cjs`): `gpt-5.5`
- Cross-file component/layout refactors: `gpt-5.5`
- Complex breakage/debug sessions: `gpt-5.2-pro`
- Documentation-only updates: `gpt-5.4-mini`

## Prompting Pattern
Use this structure for better outputs:
1. Goal and constraints (e.g., backward compatibility in `exports`)
2. Exact files to touch
3. Required verification (`npm run build`)
4. Output format (patch + summary + risk notes)

## Verification Rule
Regardless of model choice, accept changes only when:
- `npm run build` passes
- Generated `dist/` output matches intent
- Public API changes are documented in `README.md` or `CHANGELOG.md`
