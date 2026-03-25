# Slidev Slide Style Guide

When creating or editing slides in `slides.md`, always follow these conventions.

## Theme & Colors

- Background: `#0a0a0a` (near-black) — set on every slide via `<style>.slidev-layout { background: #0a0a0a; }</style>`
- Card/panel background: `bg-[#141414]`
- Card border: `border border-[#222]`
- Body text: `text-gray-300` or `text-gray-400`
- Muted/label text: `text-gray-500`
- Accent colors by role:
  - Green `text-green-400` — solutions, good examples, MCP, checkmarks `✓`, bullets `›`
  - Red `text-red-400` — problems, bad examples, crosses `×`
  - Blue `text-blue-400` — user / fundamental truths
  - Purple `text-purple-400` — LLM / model
  - Orange `text-orange-400` — code / agent runtime
  - Yellow `text-yellow-400` — warnings, caveats

## Heading Style

Always put heading size in a `<style>` block at the bottom of the slide:

```html
<style>
  h1 { color: #fff; font-size: 2rem; font-weight: 800; }
  .slidev-layout { background: #0a0a0a; }
</style>
```

Font size variants:
- Normal content slide: `2rem`
- Section header slide: `3rem`
- Title slide: `2.5rem`

## Slide Separator & Frontmatter

Plain slide (no special layout):
```
---

# Slide Title
```

Slide with frontmatter:
```
---
layout: center
class: text-center
---
```

## Section Header Slides

```html
---
layout: center
class: text-center
---

<div class="text-green-400 text-xs font-extrabold tracking-widest mb-4">SECTION N</div>

# Section Title

<div class="mt-4 text-gray-500 text-lg">One-line subtitle</div>

<style>
  h1 { color: #fff; font-size: 3rem; font-weight: 800; line-height: 1.2; }
  .slidev-layout { background: #0a0a0a; }
</style>
```

## Content Slide Subtitle

Immediately under `# Title`, before the main content:
```html
<div class="text-gray-400 text-sm font-semibold -mt-2 mb-4">Subtitle text here</div>
```

## Bottom Callout Bar

Used at the bottom of most content slides as a key takeaway:
```html
<div class="absolute bottom-8 left-12 right-12 bg-[#141414] border-l-3 border-green-400 rounded-r-md px-5 py-3 font-mono text-sm text-gray-500">
  Key takeaway text here
</div>
```
Swap `border-green-400` for red/yellow/orange/purple as appropriate.

## Card Panels

Standard card:
```html
<div class="bg-[#141414] border border-[#222] rounded-xl p-5">
  <div class="text-green-400 text-xs font-extrabold tracking-widest mb-3">LABEL</div>
  <!-- content -->
</div>
```

Card with coloured top border:
```html
<div class="bg-[#141414] border border-[#222] border-t-3 border-t-green-400 rounded-xl p-4">
```

Left-border callout:
```html
<div class="bg-[#141414] border-l-3 border-yellow-400 rounded-r-lg px-6 py-5 text-gray-300 text-lg leading-relaxed">
```

## Bullet Lists

```html
<div class="flex items-start gap-3">
  <span class="text-green-400 font-extrabold shrink-0">›</span>
  <span class="text-gray-200">Item text</span>
</div>
```

For bad/problem items use `text-red-400` and `×` instead.

## Code Blocks

Add to the slide's `<style>` block when using fenced code:
```css
.slidev-code-wrapper { margin: 0 !important; }
pre.shiki { background: transparent !important; padding: 0.25rem 0 !important; font-size: 0.8rem !important; }
```

## Image Zoom/Pan Pattern

**Always use this pattern for any slide with a significant image.**

Frontmatter: `clicks: 4`

Layout:
- `$clicks === 0`: small image (`h-64`) + content side by side, with hover hint
- `$clicks >= 1`: full-slide overlay with `overflow-hidden` container, image zooms in from `scale(1)` then pans top→bottom

```html
---
clicks: 4
---

# Slide Title

<div class="text-gray-400 text-sm font-semibold -mt-2 mb-4">Subtitle</div>

<div v-if="$clicks === 0" class="flex gap-6 items-start">
  <div class="relative group shrink-0">
    <img src="/image.png" class="h-64 object-contain rounded-xl border border-[#222] cursor-pointer" />
    <div class="absolute inset-0 flex items-end justify-end p-2 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none">
      <span class="bg-black/80 text-gray-400 text-xs px-2 py-1 rounded font-mono">→ click to zoom</span>
    </div>
  </div>

  <!-- side content here -->
</div>

<transition name="fade">
  <div v-if="$clicks >= 1" class="absolute inset-0 bg-[#0a0a0a] z-10 flex items-center justify-center p-4">
    <div class="relative overflow-hidden rounded-xl border border-[#222] w-full h-full">
      <img
        src="/image.png"
        class="w-full h-full object-contain origin-center transition-transform duration-500 ease-in-out"
        :style="{
          transform: $clicks === 1
            ? 'scale(1) translateY(0)'
            : $clicks === 2
              ? 'scale(2) translateY(25%)'
              : $clicks === 3
                ? 'scale(2) translateY(0%)'
                : 'scale(2) translateY(-25%)'
        }"
      />
    </div>
  </div>
</transition>

<style>
  h1 { color: #fff; font-size: 2rem; font-weight: 800; }
  .slidev-layout { background: #0a0a0a; }
  .fade-enter-active, .fade-leave-active { transition: opacity 0.4s ease; }
  .fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
```

For **full-slide image slides** (no side content), use the in-place zoom from slide 14 style:

```html
---
clicks: 4
---

# Slide Title

<div class="text-gray-400 text-sm font-semibold -mt-2 mb-2">Subtitle — <span class="text-green-400">click through to zoom</span></div>

<div class="relative overflow-hidden rounded-xl border border-[#222] mx-auto" style="height: 75vh">
  <img
    src="/image.png"
    class="w-full h-full object-contain origin-center transition-transform duration-500 ease-in-out"
    :style="{
      transform: $clicks === 0
        ? 'scale(1) translateY(0)'
        : $clicks === 1
          ? 'scale(2) translateY(25%)'
          : $clicks === 2
            ? 'scale(2) translateY(8%)'
            : $clicks === 3
              ? 'scale(2) translateY(-8%)'
              : 'scale(2) translateY(-25%)'
    }"
  />
</div>

<style>
  h1 { color: #fff; font-size: 2rem; font-weight: 800; }
  .slidev-layout { background: #0a0a0a; }
</style>
```

## Good / Bad Code Comparison Layout

```html
<div class="grid grid-cols-2 gap-4">
  <div class="bg-[#141414] border border-red-400/30 border-t-3 border-t-red-400 rounded-xl p-4">
    <div class="text-red-400 text-xs font-extrabold tracking-wide mb-3">BAD</div>
    <!-- code block -->
  </div>
  <div class="bg-[#141414] border border-green-400/30 border-t-3 border-t-green-400 rounded-xl p-4">
    <div class="text-green-400 text-xs font-extrabold tracking-wide mb-3">GOOD</div>
    <!-- code block -->
  </div>
</div>
```

## v-for Lists in Templates

Use Vue's `v-for` with inline arrays for repeated items instead of copy-pasting markup:

```html
<div v-for="item in ['Item one', 'Item two', 'Item three']"
     class="bg-[#141414] border border-[#222] rounded-lg px-4 py-2.5 text-sm text-gray-300 flex items-center gap-3">
  <span class="text-green-400 font-extrabold shrink-0">›</span>
  <span>{{ item }}</span>
</div>
```

## Images

All images live in `public/` and are referenced as `/filename.png` (no `public/` prefix).
