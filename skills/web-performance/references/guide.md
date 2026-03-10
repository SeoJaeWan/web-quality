# Web Performance Reference Guide

This file is the reference material for the web-performance skill.
See SKILL.md for execution instructions.

---

# Performance & Core Web Vitals optimization

Deep optimization covering loading speed, runtime efficiency, resource optimization, and the three Core Web Vitals metrics (LCP, INP, CLS).

## How it works

1. Identify performance bottlenecks in code and assets
2. Prioritize by impact on Core Web Vitals
3. Provide specific optimizations with code examples
4. Measure improvement with before/after metrics

## Performance budget

| Resource | Budget | Rationale |
|----------|--------|-----------|
| Total page weight | < 1.5 MB | 3G loads in ~4s |
| JavaScript (compressed) | < 300 KB | Parsing + execution time |
| CSS (compressed) | < 100 KB | Render blocking |
| Images (above-fold) | < 500 KB | LCP impact |
| Fonts | < 100 KB | FOIT/FOUT prevention |
| Third-party | < 200 KB | Uncontrolled latency |

## Core Web Vitals thresholds

| Metric | Measures | Good | Needs work | Poor |
|--------|----------|------|------------|------|
| **LCP** | Loading | ≤ 2.5s | 2.5s – 4s | > 4s |
| **INP** | Interactivity | ≤ 200ms | 200ms – 500ms | > 500ms |
| **CLS** | Visual Stability | ≤ 0.1 | 0.1 – 0.25 | > 0.25 |

Google measures at the **75th percentile** — 75% of page visits must meet "Good" thresholds.

---

## Critical rendering path

### Server response
* **TTFB < 800ms.** Time to First Byte should be fast. Use CDN, caching, and efficient backends.
* **Enable compression.** Gzip or Brotli for text assets. Brotli preferred (15-20% smaller).
* **HTTP/2 or HTTP/3.** Multiplexing reduces connection overhead.
* **Edge caching.** Cache HTML at CDN edge when possible.

### Resource loading

**Preconnect to required origins:**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://cdn.example.com" crossorigin>
```

**Preload critical resources:**
```html
<!-- LCP image -->
<link rel="preload" href="/hero.webp" as="image" fetchpriority="high">

<!-- Critical font -->
<link rel="preload" href="/font.woff2" as="font" type="font/woff2" crossorigin>
```

**Defer non-critical CSS:**
```html
<!-- Critical CSS inlined -->
<style>/* Above-fold styles */</style>

<!-- Non-critical CSS -->
<link rel="preload" href="/styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="/styles.css"></noscript>
```

### JavaScript optimization

**Defer non-essential scripts:**
```html
<!-- Deferred (preferred) -->
<script defer src="/app.js"></script>

<!-- Async (for independent scripts) -->
<script async src="/analytics.js"></script>

<!-- Module (deferred by default) -->
<script type="module" src="/app.mjs"></script>
```

**Code splitting patterns:**
```javascript
// Route-based splitting
const Dashboard = lazy(() => import('./Dashboard'));

// Component-based splitting
const HeavyChart = lazy(() => import('./HeavyChart'));

// Feature-based splitting
if (user.isPremium) {
  const PremiumFeatures = await import('./PremiumFeatures');
}
```

**Tree shaking best practices:**
```javascript
// ❌ Imports entire library
import _ from 'lodash';
_.debounce(fn, 300);

// ✅ Imports only what's needed
import debounce from 'lodash/debounce';
debounce(fn, 300);
```

## Image optimization

### Format selection
| Format | Use case | Browser support |
|--------|----------|-----------------|
| AVIF | Photos, best compression | 92%+ |
| WebP | Photos, good fallback | 97%+ |
| PNG | Graphics with transparency | Universal |
| SVG | Icons, logos, illustrations | Universal |

### Responsive images
```html
<picture>
  <source
    type="image/avif"
    srcset="hero-400.avif 400w, hero-800.avif 800w, hero-1200.avif 1200w"
    sizes="(max-width: 600px) 100vw, 50vw">

  <source
    type="image/webp"
    srcset="hero-400.webp 400w, hero-800.webp 800w, hero-1200.webp 1200w"
    sizes="(max-width: 600px) 100vw, 50vw">

  <img
    src="hero-800.jpg"
    srcset="hero-400.jpg 400w, hero-800.jpg 800w, hero-1200.jpg 1200w"
    sizes="(max-width: 600px) 100vw, 50vw"
    width="1200"
    height="600"
    alt="Hero image"
    loading="lazy"
    decoding="async">
</picture>
```

### LCP image priority
```html
<!-- Above-fold LCP image: eager loading, high priority -->
<img src="hero.webp" fetchpriority="high" loading="eager" decoding="sync" alt="Hero">

<!-- Below-fold images: lazy loading -->
<img src="product.webp" loading="lazy" decoding="async" alt="Product">
```

## Font optimization

### Loading strategy
```css
body {
  font-family: 'Custom Font', -apple-system, BlinkMacSystemFont,
               'Segoe UI', Roboto, sans-serif;
}

@font-face {
  font-family: 'Custom Font';
  src: url('/fonts/custom.woff2') format('woff2');
  font-display: swap;
  font-weight: 400;
  font-style: normal;
  unicode-range: U+0000-00FF;
}
```

> **font-display values:**
> - `swap` — Show fallback immediately, swap when custom loads (best for LCP, may cause CLS)
> - `optional` — Show fallback, only use custom if cached (best for CLS, may miss first visit)
> - `fallback` — Short block period then fallback, swap if loaded within ~3s (balanced)
> - `block` — **Avoid.** Invisible text until font loads → hurts LCP and may cause layout shift

### CLS prevention with font metrics matching
```css
/* Match fallback font metrics to reduce layout shift on swap */
@font-face {
  font-family: 'Custom';
  src: url('custom.woff2') format('woff2');
  font-display: swap;
  size-adjust: 105%;
  ascent-override: 95%;
  descent-override: 20%;
}
```

### Preloading critical fonts
```html
<link rel="preload" href="/fonts/heading.woff2" as="font" type="font/woff2" crossorigin>
```

### Variable fonts
```css
@font-face {
  font-family: 'Inter';
  src: url('/fonts/Inter-Variable.woff2') format('woff2-variations');
  font-weight: 100 900;
  font-display: swap;
}
```

## Caching strategy

### Cache-Control headers
```
# HTML (short or no cache)
Cache-Control: no-cache, must-revalidate

# Static assets with hash (immutable)
Cache-Control: public, max-age=31536000, immutable

# Static assets without hash
Cache-Control: public, max-age=86400, stale-while-revalidate=604800

# API responses
Cache-Control: private, max-age=0, must-revalidate
```

### Service worker caching
```javascript
self.addEventListener('fetch', (event) => {
  if (event.request.destination === 'image' ||
      event.request.destination === 'style' ||
      event.request.destination === 'script') {
    event.respondWith(
      caches.match(event.request).then((cached) => {
        return cached || fetch(event.request).then((response) => {
          const clone = response.clone();
          caches.open('static-v1').then((cache) => cache.put(event.request, clone));
          return response;
        });
      })
    );
  }
});
```

## Runtime performance

### Avoid layout thrashing
```javascript
// ❌ Forces multiple reflows
elements.forEach(el => {
  const height = el.offsetHeight;
  el.style.height = height + 10 + 'px';
});

// ✅ Batch reads, then batch writes
const heights = elements.map(el => el.offsetHeight);
elements.forEach((el, i) => {
  el.style.height = heights[i] + 10 + 'px';
});
```

### Debounce expensive operations
```javascript
function debounce(fn, delay) {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(...args), delay);
  };
}

window.addEventListener('scroll', debounce(handleScroll, 100));
```

### Use requestAnimationFrame
```javascript
// ❌ May cause jank
setInterval(animate, 16);

// ✅ Synced with display refresh
function animate() {
  requestAnimationFrame(animate);
}
requestAnimationFrame(animate);
```

### Virtualize long lists
```css
/* For lists > 100 items, render only visible items */
.virtual-list {
  content-visibility: auto;
  contain-intrinsic-size: 0 50px;
}
```

## Third-party scripts

### Load strategies
```html
<!-- ✅ Async loading -->
<script async src="https://analytics.example.com/script.js"></script>
```

```javascript
// ✅ Delay until element visible
const observer = new IntersectionObserver((entries) => {
  if (entries[0].isIntersecting) {
    const script = document.createElement('script');
    script.src = 'https://widget.example.com/embed.js';
    document.body.appendChild(script);
    observer.disconnect();
  }
});
observer.observe(document.querySelector('#widget-container'));
```

### Facade pattern
```html
<!-- Show static placeholder until interaction -->
<div class="youtube-facade"
     data-video-id="abc123"
     onclick="loadYouTube(this)">
  <img src="/thumbnails/abc123.jpg" alt="Video title">
  <button aria-label="Play video">▶</button>
</div>
```

---

## LCP: Largest Contentful Paint

LCP measures when the largest visible content element renders. Usually this is:
- Hero image or video
- Large text block
- Background image
- `<svg>` element

### Common LCP issues

**1. Slow server response (TTFB > 800ms)**
```
Fix: CDN, caching, optimized backend, edge rendering
```

**2. Render-blocking resources**
```html
<!-- ❌ Blocks rendering -->
<link rel="stylesheet" href="/all-styles.css">

<!-- ✅ Critical CSS inlined, rest deferred -->
<style>/* Critical above-fold CSS */</style>
<link rel="preload" href="/styles.css" as="style"
      onload="this.onload=null;this.rel='stylesheet'">
```

**3. Client-side rendering delays**
```javascript
// ❌ Content loads after JavaScript
useEffect(() => {
  fetch('/api/hero-text').then(r => r.json()).then(setHeroText);
}, []);

// ✅ Server-side or static rendering
export async function getServerSideProps() {
  const heroText = await fetchHeroText();
  return { props: { heroText } };
}
```

### LCP element identification
```javascript
new PerformanceObserver((list) => {
  const entries = list.getEntries();
  const lastEntry = entries[entries.length - 1];
  console.log('LCP element:', lastEntry.element);
  console.log('LCP time:', lastEntry.startTime);
}).observe({ type: 'largest-contentful-paint', buffered: true });
```

---

## INP: Interaction to Next Paint

INP measures responsiveness across ALL interactions (clicks, taps, key presses) during a page visit. It reports the worst interaction (at 98th percentile for high-traffic pages).

### INP breakdown

Total INP = **Input Delay** + **Processing Time** + **Presentation Delay**

| Phase | Target | Optimization |
|-------|--------|--------------|
| Input Delay | < 50ms | Reduce main thread blocking |
| Processing | < 100ms | Optimize event handlers |
| Presentation | < 50ms | Minimize rendering work |

### Common INP issues

**1. Long tasks blocking main thread**
```javascript
// ❌ Long synchronous task
function processLargeArray(items) {
  items.forEach(item => expensiveOperation(item));
}

// ✅ Break into chunks with yielding
async function processLargeArray(items) {
  const CHUNK_SIZE = 100;
  for (let i = 0; i < items.length; i += CHUNK_SIZE) {
    const chunk = items.slice(i, i + CHUNK_SIZE);
    chunk.forEach(item => expensiveOperation(item));
    await new Promise(r => setTimeout(r, 0));
  }
}
```

**2. Heavy event handlers**
```javascript
// ❌ All work in handler
button.addEventListener('click', () => {
  const result = calculateComplexThing();
  updateUI(result);
  trackEvent('click');
});

// ✅ Prioritize visual feedback
button.addEventListener('click', () => {
  button.classList.add('loading');
  requestAnimationFrame(() => {
    const result = calculateComplexThing();
    updateUI(result);
  });
  requestIdleCallback(() => trackEvent('click'));
});
```

**3. Excessive re-renders (React/Vue)**
```javascript
// ❌ Re-renders entire tree
function App() {
  const [count, setCount] = useState(0);
  return (
    <div>
      <Counter count={count} />
      <ExpensiveComponent />
    </div>
  );
}

// ✅ Memoized expensive components
const MemoizedExpensive = React.memo(ExpensiveComponent);

function App() {
  const [count, setCount] = useState(0);
  return (
    <div>
      <Counter count={count} />
      <MemoizedExpensive />
    </div>
  );
}
```

### INP debugging
```javascript
new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (entry.duration > 200) {
      console.warn('Slow interaction:', {
        type: entry.name,
        duration: entry.duration,
        target: entry.target
      });
    }
  }
}).observe({ type: 'event', buffered: true, durationThreshold: 16 });
```

---

## CLS: Cumulative Layout Shift

CLS measures unexpected layout shifts. A shift occurs when a visible element changes position between frames without user interaction.

**CLS Formula:** `impact fraction × distance fraction`

### Common CLS causes

**1. Images without dimensions**
```html
<!-- ❌ Causes layout shift when loaded -->
<img src="photo.jpg" alt="Photo">

<!-- ✅ Space reserved -->
<img src="photo.jpg" alt="Photo" width="800" height="600">

<!-- ✅ Or use aspect-ratio -->
<img src="photo.jpg" alt="Photo" style="aspect-ratio: 4/3; width: 100%;">
```

**2. Ads, embeds, and iframes**
```html
<!-- ❌ Unknown size until loaded -->
<iframe src="https://ad-network.com/ad"></iframe>

<!-- ✅ Reserve space with min-height -->
<div style="min-height: 250px;">
  <iframe src="https://ad-network.com/ad" height="250"></iframe>
</div>
```

**3. Dynamically injected content**
```javascript
// ❌ Inserts content above viewport
notifications.prepend(newNotification);

// ✅ Insert below viewport or use transform
const insertBelow = viewport.bottom < newNotification.top;
if (insertBelow) {
  notifications.prepend(newNotification);
} else {
  newNotification.style.transform = 'translateY(-100%)';
  notifications.prepend(newNotification);
  requestAnimationFrame(() => {
    newNotification.style.transform = '';
  });
}
```

**4. Web fonts causing FOUT**
```css
/* ❌ Font swap shifts text */
@font-face {
  font-family: 'Custom';
  src: url('custom.woff2') format('woff2');
}

/* ✅ Optional font (no shift if slow) */
@font-face {
  font-family: 'Custom';
  src: url('custom.woff2') format('woff2');
  font-display: optional;
}
```

**5. Animations triggering layout**
```css
/* ❌ Animates layout properties */
.animate {
  transition: height 0.3s, width 0.3s;
}

/* ✅ Use transform instead */
.animate {
  transition: transform 0.3s;
}
.animate.expanded {
  transform: scale(1.2);
}
```

### CLS debugging
```javascript
new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (!entry.hadRecentInput) {
      console.log('Layout shift:', entry.value);
      entry.sources?.forEach(source => {
        console.log('  Shifted element:', source.node);
      });
    }
  }
}).observe({ type: 'layout-shift', buffered: true });
```

---

## Measurement

### Key metrics
| Metric | Target | Tool |
|--------|--------|------|
| LCP | < 2.5s | Lighthouse, CrUX |
| INP | < 200ms | CrUX, web-vitals |
| CLS | < 0.1 | Lighthouse, CrUX |
| FCP | < 1.8s | Lighthouse |
| Speed Index | < 3.4s | Lighthouse |
| TBT | < 200ms | Lighthouse |

### Lab testing
- **Chrome DevTools** → Performance panel, Lighthouse
- **WebPageTest** → Detailed waterfall, filmstrip
- **Lighthouse CLI** → `npx lighthouse <url>`

### Field data (real users)
```javascript
import {onLCP, onINP, onCLS} from 'web-vitals';

function sendToAnalytics({name, value, rating}) {
  gtag('event', name, {
    event_category: 'Web Vitals',
    value: Math.round(name === 'CLS' ? value * 1000 : value),
    event_label: rating
  });
}

onLCP(sendToAnalytics);
onINP(sendToAnalytics);
onCLS(sendToAnalytics);
```

---

## Framework quick fixes

### Next.js
```jsx
// LCP: Use next/image with priority
import Image from 'next/image';
<Image src="/hero.jpg" priority fill alt="Hero" />

// INP: Use dynamic imports
const HeavyComponent = dynamic(() => import('./Heavy'), { ssr: false });

// CLS: Image component handles dimensions automatically
```

### React
```jsx
// LCP: Preload in head
// <link rel="preload" href="/hero.jpg" as="image" fetchpriority="high" />

// INP: Memoize and useTransition
const [isPending, startTransition] = useTransition();
startTransition(() => setExpensiveState(newValue));

// CLS: Always specify dimensions in img tags
```

### Vue/Nuxt
```vue
<!-- LCP: Use nuxt/image with preload -->
<!-- <NuxtImg src="/hero.jpg" preload loading="eager" /> -->

<!-- INP: Use async components -->
<!-- <component :is="() => import('./Heavy.vue')" /> -->

<!-- CLS: Use aspect-ratio CSS -->
<!-- <img :style="{ aspectRatio: '16/9' }" /> -->
```
