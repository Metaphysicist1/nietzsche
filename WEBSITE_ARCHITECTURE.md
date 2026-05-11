# Nietzsche Site — Architecture Reference & Reusable Prompt

---

## Reusable Prompt (copy-paste this for future sites)

```
You are an expert creative frontend developer specializing in award-winning,
Awwwards SOTY-level web experiences.

Build a complete single-file `index.html` site with the following locked stack
and patterns. Do not deviate from the stack unless I explicitly ask.

---

### TOPIC
[REPLACE: e.g. "Friedrich Nietzsche — philosophy", "Elon Musk — biography",
"A dark sci-fi product landing page"]

### STYLE
[REPLACE one of:]
- Dark Manifesto   → dense typographic chaos, glitch, ink/void aesthetic
- Lando Energy     → cinematic, bold, high-speed, dramatic cuts
- Bruno Simon 3D   → playful WebGL canvas hero, minimal UI, physics feel
- Luxury Minimal   → slow editorial, museum-quality, heavy whitespace
- Creative Agency  → bold grid, strong color blocks, scroll-driven reveals

### COLOR PALETTE
[REPLACE one of:]
- Nihilism Void    → #020209 black + #00d2ff cold cyan
- Blood & Bone     → #0a0908 ink + #c14a2b ember + #f5efe1 parchment
- Neon Dark        → #050510 + #ff00ff magenta + #00ff88 green
- Arctic White     → #f8f8ff + #0a0a0a + #4488ff blue
- Custom           → [describe your palette]

### CONTENT SECTIONS
[REPLACE: list the sections you want, e.g.]
- Hero (full viewport, dramatic entrance, canvas background)
- Intro / Manifesto text reveal
- Concepts / Features grid (6 cards)
- Timeline (vertical, scroll-driven rail)
- Works / Portfolio grid (8 cards, 3/4 aspect ratio)
- Pinned quote section
- Footer with links

### REQUIRED FEATURES (keep all of these)
- Loader: percentage counter + thin glowing progress bar, releases on window.load
- Scroll progress bar: 1px gradient fixed at top
- Custom cursor: dot 1:1 tracking + ring that lerps with lag, expands on hover
- Canvas background: particle network (dots + connecting lines) with cursor repulsion
- Hero entrance: words clip inside overflow:hidden lines, slide up via GSAP on load
- Glitch effect: CSS ::before/::after on key hero word, red+accent split-clip, fires ~every 6s
- Section outline numbers: giant transparent -webkit-text-stroke background numerals
- Concept cards: mouse-follow radial spotlight via CSS vars (--mx, --my), top-line reveal
- Work cards: 3D perspective tilt on mousemove + radial glow
- Timeline: vertical rail that fills in height as ScrollTrigger scrolls through section
- Dual marquee: one forward, one reverse, pause on hover
- Active nav: ScrollTrigger onToggle adds .is-active class + underline scale animation
- Mobile menu: full-screen translateY(-100%) slide-down, Bebas Neue nav items
- Lenis smooth scroll synced to ScrollTrigger via lenis.on('scroll', ScrollTrigger.update)
- Grain overlay: SVG fractalNoise, opacity .04, mix-blend-mode overlay
- Scanline overlay: repeating-linear-gradient horizontal lines, subtle
- Reduced motion: @media prefers-reduced-motion disables all animations

### LOCKED TECH STACK
- Fonts: Bebas Neue (display), Cormorant Garamond (editorial/serif), Space Grotesk (eyebrow/UI)
- Tailwind CSS via Play CDN with custom config (no utility purge needed)
- GSAP 3.12.5 + ScrollTrigger via cdnjs CDN
- Lenis 1.1.13 via unpkg CDN
- Canvas API (vanilla JS, no Three.js unless explicitly asked)
- Zero other libraries

### OUTPUT FORMAT
- Single `index.html` file, everything embedded
- CSS in <style> in <head>
- Scripts at bottom of <body>
- Well-commented section blocks (LOADER, CURSOR, CANVAS, etc.)
- Production-ready, no placeholder lorem ipsum
- All German/Latin/relevant-language terms preserved in content
```

---

## Architecture Reference

### Color System

| Token        | Hex / Value                  | Usage                          |
|-------------|------------------------------|--------------------------------|
| `--void`     | `#020209`                    | Main background                |
| `--void-2`   | `#06060f`                    | Alternate section bg           |
| `--void-3`   | `#0d0d1e`                    | Deep surface                   |
| `--cyan`     | `#00d2ff`                    | Primary accent, glow, borders  |
| `--cyan-2`   | `#0066ff`                    | Progress bar gradient start    |
| `--bright`   | `#e8e8f8`                    | Headlines, high-emphasis text  |
| `--mist`     | `#c8c8e4`                    | Body text                      |
| `--dim`      | `#4a4a6a`                    | Secondary text, descriptions   |
| `--muted`    | `#1a1a2e`                    | Lowest emphasis, borders       |

---

### Typography Stack

```css
font-family: "Bebas Neue"          /* display-title — all caps, tracking .02em */
font-family: "Cormorant Garamond"  /* editorial — weight 300, italic for quotes */
font-family: "Space Grotesk"       /* eyebrow — 11px, tracking .35em, uppercase */
```

**Scale pattern:**
```css
/* Headlines  */ font-size: clamp(3rem, 7vw, 6rem)
/* Hero title */ font-size: clamp(4.5rem, 22vw, 20rem)
/* Manifesto  */ font-size: clamp(1.6rem, 3.5vw, 3.2rem)
/* Body       */ font-size: clamp(1.1rem, 2vw, 1.5rem)
/* Eyebrow    */ font-size: 11px, letter-spacing: .35em
```

---

### CSS Patterns

#### Glitch Effect
```css
.glitch { position: relative; }
.glitch::before, .glitch::after {
  content: attr(data-text);
  position: absolute; top: 0; left: 0; width: 100%; height: 100%;
}
.glitch::before {
  color: #ff0044;
  clip-path: polygon(0 0, 100% 0, 100% 28%, 0 28%);
  animation: g1 6s infinite;
}
.glitch::after {
  color: #00d2ff;
  clip-path: polygon(0 62%, 100% 62%, 100% 100%, 0 100%);
  animation: g2 6s infinite;
}
/* Keyframes: 0-88% opacity:0, 89-96% translate ±4px, 97%+ opacity:0 */
```
> HTML usage: `<span class="glitch" data-text="TOT.">TOT.</span>`

#### Split-line Word Reveal
```css
.split-line { overflow: hidden; display: block; line-height: .92; }
.split-line > .word { display: block; will-change: transform; }
```
```js
/* GSAP entrance */
gsap.from('#hero .word', { yPercent: 105, duration: 1.2, stagger: 0.06, ease: 'power4.out' });
```

#### Concept Card Spotlight (CPU-cheap mouse follow)
```css
.concept-card::before {
  content: ""; position: absolute; inset: 0;
  background: radial-gradient(500px circle at var(--mx,50%) var(--my,50%),
              rgba(0,210,255,.11), transparent 45%);
  opacity: 0; transition: opacity .4s ease;
}
.concept-card:hover::before { opacity: 1; }
```
```js
card.addEventListener('mousemove', e => {
  const r = card.getBoundingClientRect();
  card.style.setProperty('--mx', ((e.clientX - r.left) / r.width) * 100 + '%');
  card.style.setProperty('--my', ((e.clientY - r.top) / r.height) * 100 + '%');
});
```

#### Section Outline Numbers
```css
.sec-num {
  font-family: "Bebas Neue", sans-serif;
  color: transparent;
  -webkit-text-stroke: 1px rgba(0,210,255,.1);
  font-size: clamp(8rem, 22vw, 20rem);
  position: absolute; pointer-events: none; user-select: none;
}
```

#### Dual Marquee (seamless loop)
```css
.marquee-fwd { display:flex; width:max-content; animation: mfwd 55s linear infinite; }
.marquee-rev { display:flex; width:max-content; animation: mrev 42s linear infinite; }
@keyframes mfwd { to   { transform: translateX(-50%); } }
@keyframes mrev { from { transform: translateX(-50%); } to { transform: translateX(0); } }
```
> HTML: duplicate content twice inside the track div — `translateX(-50%)` makes loop seamless.

---

### JS Patterns

#### Lenis ↔ ScrollTrigger Sync (critical — must be exact)
```js
const lenis = new Lenis({ duration: 1.15, smoothWheel: true,
  easing: t => Math.min(1, 1.001 - Math.pow(2, -10 * t)) });
(function raf(t) { lenis.raf(t); requestAnimationFrame(raf); })(0);
gsap.registerPlugin(ScrollTrigger);
lenis.on('scroll', ScrollTrigger.update);   // keeps ST in sync with Lenis
```

#### Loader Release Pattern
```js
window.addEventListener('load', () => {
  // 'load' fires after all resources — fonts, images, scripts
  setTimeout(() => {
    document.getElementById('loader').classList.add('is-done'); // CSS transition fades it
    document.documentElement.classList.add('has-cursor');       // enables cursor:none
    playEntrance();                                             // fires GSAP hero animation
  }, 550);  // small buffer for font render
});
```

#### Canvas Void Network
```js
// Key constants
const CONNECT2 = 130 * 130;  // connect particles within 130px (squared, avoids sqrt)
const REP_R2   = 140 * 140;  // cursor repulsion radius (squared)

// Per particle per frame:
// 1. Check cursor distance, apply repulsion force if within REP_R2
// 2. Apply velocity, wrap at canvas edges
// 3. Draw dot: rgba(0,210,255, particle.opacity)
// 4. Inner loop j>i: if distance² < CONNECT2, draw line with alpha = (1 - d²/CONNECT2) * 0.2
```

#### 3D Tilt (work cards)
```js
card.addEventListener('mousemove', e => {
  const r  = card.getBoundingClientRect();
  const cx = (e.clientX - r.left) / r.width  - 0.5;  // -0.5 to 0.5
  const cy = (e.clientY - r.top)  / r.height - 0.5;
  card.style.transform = `perspective(900px) rotateX(${-cy * 8}deg) rotateY(${cx * 8}deg)`;
});
card.addEventListener('mouseleave', () => { card.style.transform = ''; });
```

#### Timeline Progress Rail
```js
ScrollTrigger.create({
  trigger: '#timeline',
  start: 'top 70%',
  end: 'bottom 70%',
  onUpdate: self => {
    document.querySelector('.tl-progress').style.height = (self.progress * 100) + '%';
  }
});
```

---

### Section Structure

```
#hero          → 100vh canvas + vignette + split-line title + subtitle
marquee-1      → forward scroll, concept keywords
#manifesto     → sticky sidebar + large editorial text, word-by-word read feel
#concepts      → 3-col grid, concept cards with spotlight
#timeline      → alternating left/right events, filling rail
#works         → 4-col grid, 3/4 aspect-ratio cards with 3D tilt
marquee-2      → reverse scroll, book/quote keywords
#quote         → full-width pinned blockquote
footer         → 12-col grid, Memento Vivere headline, link columns
```

---

### Performance Notes

- Canvas: `devicePixelRatio` capped at 2. Particle count halved on mobile (`W < 768`).
- All hover effects use CSS `transition` not GSAP where possible (cheaper).
- Spotlight gradients live in CSS using `--mx`/`--my` vars — only JS writes two numbers.
- `will-change: transform` only on `.word` and `.work-card` (high-motion elements).
- `{ passive: true }` on all scroll/mousemove listeners.
- Grain and scanline overlays use `pointer-events: none` + fixed position (no layout cost).
- `@media (prefers-reduced-motion)` disables all animations including marquees.

---

### CDN URLs (pinned versions)

```html
<!-- Fonts -->
https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400;1,600&family=Space+Grotesk:wght@300;400;500

<!-- Tailwind Play CDN -->
https://cdn.tailwindcss.com

<!-- GSAP -->
https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js
https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js

<!-- Lenis -->
https://unpkg.com/lenis@1.1.13/dist/lenis.min.js
```
