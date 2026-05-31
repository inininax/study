# Design System

Cross-platform design system for **Mobile App**, **Mobile Web**, and **PC Web**. Tokens + Components + Layouts + Animations — zero dependencies, framework-agnostic.

## Usage

### Fastest Way — All-in-One

```html
<link rel="stylesheet" href="@myorg/design-system/css/all.css">
```

This single file includes everything: tokens, reset, utilities, animations, layouts, and all 20 components.

```html
<button class="ds-btn ds-btn-primary">Save</button>
<div class="ds-card">
  <div class="ds-card-body">
    <h3 class="ds-card-title">Hello</h3>
  </div>
</div>
<div class="ds-grid ds-grid-cols-3 ds-gap-4">
  <div>Column 1</div>
  <div>Column 2</div>
  <div>Column 3</div>
</div>
```

### Modular Import

```css
/* Pick what you need */
@import "@myorg/design-system/css/tokens.css";      /* Design tokens (required) */
@import "@myorg/design-system/css/reset.css";        /* CSS reset */
@import "@myorg/design-system/css/utilities.css";    /* Utility classes */
@import "@myorg/design-system/css/components.css";   /* All 20 components */
@import "@myorg/design-system/css/layouts.css";      /* Grid + Stack */
@import "@myorg/design-system/css/animations.css";   /* Keyframe animations */
```

### Individual Components

```css
/* Import only what you use */
@import "@myorg/design-system/css/tokens.css";
@import "@myorg/design-system/css/components/button.css";
@import "@myorg/design-system/css/components/card.css";
@import "@myorg/design-system/css/components/input.css";
```

### SCSS

```scss
@use "@myorg/design-system/styles" as ds;

.custom-card {
  @include ds.elevation('md');
  @include ds.body-text('base');
  padding: ds.$spacing-4;
}
```

### JavaScript / TypeScript

```typescript
import { primitives, light, dark } from '@myorg/design-system';

// Token values with full type safety
console.log(primitives.colorNeutral50);  // "#FAFAF7"
console.log(primitives.fontWeightBold);  // 700 (number, not string)
```

### JSON (React Native / Flutter)

```javascript
import primitives from '@myorg/design-system/tokens/json/flat-primitives.json';
import lightTokens from '@myorg/design-system/tokens/semantic/light';
```

## Install

```bash
npm install @myorg/design-system
```

Requires Node.js 16+ for local builds.

| Method | Command | Use Case |
|---|---|---|
| npm | `npm install @myorg/design-system` | Production |
| git submodule | `git submodule add <repo-url>` | Source access |
| npm link | `npm link @myorg/design-system` | Local dev |

## Dark Mode

```html
<!-- Automatic (follows OS) -->
<html>

<!-- Force light -->
<html data-theme="light">

<!-- Force dark -->
<html data-theme="dark">
```

All components switch automatically — no extra CSS needed.

## Components (20)

| Category | Components | Example |
|---|---|---|
| **Form** | button, input, select, textarea, checkbox, radio, toggle | `.ds-btn-primary`, `.ds-input`, `.ds-toggle` |
| **Display** | card, badge, alert, modal, avatar, divider | `.ds-card`, `.ds-badge-success`, `.ds-alert-error` |
| **Navigation** | navbar, tabs, dropdown, accordion | `.ds-navbar`, `.ds-tab-active`, `.ds-dropdown` |
| **Data** | table | `.ds-table-striped`, `.ds-table-hoverable` |
| **Feedback** | progress, skeleton, tooltip | `.ds-progress`, `.ds-skeleton`, `data-tooltip="..."` |

Interactive components support `:hover`, `:focus-visible`, and `:disabled` states. Most form components support `sm`/`lg` size variants. Non-interactive display components (badge, skeleton, progress) provide size variants; divider provides orientation variants.

## Layout System

```html
<!-- 12-column CSS Grid -->
<div class="ds-grid ds-grid-cols-3 ds-gap-4">...</div>

<!-- Responsive grid -->
<div class="ds-grid ds-sm\:grid-cols-1 ds-md\:grid-cols-2 ds-lg\:grid-cols-4 ds-gap-4">...</div>

<!-- Vertical stack -->
<div class="ds-stack-md">...</div>

<!-- Horizontal stack -->
<div class="ds-hstack-md">...</div>
```

## Animations

```html
<div class="ds-animate-fade-in">Fades in</div>
<div class="ds-animate-slide-up">Slides up</div>
<div class="ds-animate-spin">Spinning</div>
```

12 animations available: fade-in/out, slide-up/down/left/right, scale-in/out, spin, pulse, bounce.
Automatically disabled when user prefers reduced motion.

## Tokens

**288 design tokens** across 9 primitive categories + semantic layer:

- **Colors**: 9 palettes (neutral, mocha, terracotta, teal, sage, blue, red, green, amber) × 10 shades
- **Typography**: font families, 10 sizes, 4 weights, line heights, letter spacing
- **Spacing**: 15-step scale (0–96px) + breakpoints + containers
- **Radius**: 7 sizes (none → full)
- **Shadow**: 5 light + 5 dark elevation levels
- **Motion**: 5 durations + 5 easings
- **Z-index**: 9 named layers (hide → tooltip)
- **Opacity**: 12 steps (0–100)
- **Border-width**: 4 sizes (none → thick)

Available as: CSS variables, SCSS, JSON, ESM JS, CJS, TypeScript, W3C DTCG.

## Build (for development)

```bash
npm run build    # Zero dependencies — pure Node.js
```

## AI-Assisted Contribution (Optional)

If you use coding assistants, follow [docs/AI_MODEL_SELECTION.md](docs/AI_MODEL_SELECTION.md) for task-based model selection and validation rules in this repository.

## Reference

See [docs/DESIGN_SYSTEM_LANDSCAPE.md](docs/DESIGN_SYSTEM_LANDSCAPE.md) for a comparison with the world's top design systems (Tailwind, MUI, Bootstrap, Ant Design, Mantine, shadcn/ui).

## License

MIT
