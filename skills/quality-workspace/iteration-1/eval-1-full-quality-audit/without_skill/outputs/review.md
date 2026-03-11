# Comprehensive Web Quality Review

**Reviewed files:**
- `features/web-sample/pages/index.html`
- `features/web-sample/pages/dashboard.tsx`
- `features/web-sample/components/Card.tsx`

---

## 1. Accessibility

### 1.1 Missing `alt` attribute on image (index.html, line 30)

**Severity: Critical**

```html
<img src="/public/logo.png" width="120" height="40" />
```

The `alt` attribute is absent entirely. This violates WCAG 2.x Success Criterion 1.1.1 (Non-text Content). Screen readers will fall back to reading the file name, which provides no meaningful information. Every `<img>` element must have an `alt` attribute -- use an empty string (`alt=""`) only if the image is purely decorative.

**Recommendation:** Add a descriptive `alt` attribute, e.g. `alt="Company logo"`.

---

### 1.2 Icon buttons without accessible names (dashboard.tsx, lines 29-36)

**Severity: Critical**

```tsx
<button>
  <svg width="16" height="16" viewBox="0 0 16 16"><circle cx="8" cy="8" r="8" /></svg>
</button>
```

Both icon buttons contain only SVG content with no text, `aria-label`, or `aria-labelledby`. This violates WCAG 2.x SC 4.1.2 (Name, Role, Value) and SC 1.1.1. Assistive technologies will announce these as unlabelled buttons, making them impossible to identify.

**Recommendation:** Add `aria-label` to each `<button>`, e.g. `<button aria-label="Settings">`. Alternatively, add `<title>` inside the SVG element with a corresponding `aria-labelledby`.

---

### 1.3 Clickable `<div>` without keyboard accessibility (Card.tsx, lines 24-33)

**Severity: High**

```tsx
<div id="card-item" className={...} onClick={handleClick}>
```

The Card component uses a `<div>` with an `onClick` handler but lacks:
- `role="button"` or a semantic `<button>` element
- `tabIndex={0}` to make it focusable via keyboard
- `onKeyDown` / `onKeyUp` handler for Enter and Space key activation

This violates WCAG SC 2.1.1 (Keyboard) and SC 4.1.2 (Name, Role, Value). Keyboard-only users cannot interact with this element.

**Recommendation:** Either replace the `<div>` with a `<button>` element, or add `role="button"`, `tabIndex={0}`, and a keyboard event handler that responds to Enter and Space keys.

---

### 1.4 Duplicate `id` attribute (Card.tsx, line 27)

**Severity: High**

```tsx
id="card-item"
```

When multiple `Card` components are rendered in a list, every instance receives the same `id="card-item"`. Duplicate IDs violate the HTML specification and WCAG SC 4.1.1 (Parsing). They break `aria-labelledby`, `aria-describedby`, label associations, and `document.getElementById` behavior.

**Recommendation:** Either remove the static `id` or generate a unique ID per instance (e.g., using a prop or `useId()` hook in React 18+).

---

### 1.5 Missing landmark and skip navigation (index.html)

**Severity: Medium**

The page body has no `<main>`, `<nav>`, `<header>`, or `<footer>` landmarks. Users relying on assistive technologies cannot navigate by landmark regions. There is also no skip-navigation link.

**Recommendation:** Wrap primary content in `<main>`, add a `<header>` with navigation if needed, and provide a "Skip to main content" link at the top of the page.

---

## 2. SEO

### 2.1 Missing meta description (index.html)

**Severity: High**

There is no `<meta name="description" content="...">` tag. Search engines use the meta description for snippet generation. Without it, search engines will auto-generate a snippet from page content, often yielding poor results.

**Recommendation:** Add a concise, unique meta description (120-160 characters) that summarizes the page content.

```html
<meta name="description" content="Welcome to our sample page. Explore our latest deals and services." />
```

---

### 2.2 Missing structured data / JSON-LD (index.html)

**Severity: Medium**

There is no JSON-LD or other structured data markup (Schema.org). Structured data enables rich results in search engines (sitelinks, breadcrumbs, FAQ snippets, etc.).

**Recommendation:** Add a JSON-LD script block with appropriate schema types (e.g., `WebPage`, `Organization`).

---

### 2.3 Non-descriptive page title (index.html)

**Severity: Medium**

```html
<title>Sample Page</title>
```

The title "Sample Page" is generic and provides no SEO value. The `<title>` element is one of the strongest on-page ranking signals.

**Recommendation:** Use a descriptive, keyword-rich title unique to this page (50-60 characters).

---

### 2.4 Missing canonical URL (index.html)

**Severity: Medium**

No `<link rel="canonical" href="...">` tag is present. Without a canonical tag, search engines may index duplicate URLs or parameter variations separately, diluting ranking signals.

**Recommendation:** Add `<link rel="canonical" href="https://example.com/" />` in the `<head>`.

---

### 2.5 Missing Open Graph and Twitter Card meta tags (index.html)

**Severity: Low**

No `og:title`, `og:description`, `og:image`, or `twitter:card` meta tags are present. These tags control how the page appears when shared on social media platforms.

**Recommendation:** Add Open Graph and Twitter Card meta tags for improved social sharing.

---

### 2.6 Images missing width/height causing CLS (index.html, line 33)

**Severity: Medium (also a performance/CLS issue)**

```html
<img src="/public/promo.png" alt="Promotional banner" />
```

Missing `width` and `height` attributes prevent the browser from reserving space before the image loads. This affects Core Web Vitals (CLS), which is a Google ranking factor.

**Recommendation:** Add explicit `width` and `height` attributes.

---

## 3. Performance

### 3.1 Render-blocking CSS (index.html, line 10)

**Severity: High**

```html
<link rel="stylesheet" href="https://cdn.example.com/styles.css" />
```

A synchronous external stylesheet in the `<head>` blocks rendering until fully downloaded and parsed. This directly impacts First Contentful Paint (FCP) and Largest Contentful Paint (LCP).

**Recommendation:**
- Inline critical CSS and load the rest asynchronously.
- Use `<link rel="preload" href="..." as="style" onload="this.onload=null;this.rel='stylesheet'">` for non-critical CSS.
- Or use `media="print" onload="this.media='all'"` pattern.

---

### 3.2 Missing `font-display: swap` (index.html, lines 13-17)

**Severity: High**

```css
@font-face {
  font-family: "CustomFont";
  src: url("/fonts/custom.woff2") format("woff2");
  /* missing: font-display: swap */
}
```

Without `font-display: swap`, browsers may hide text until the custom font loads (Flash of Invisible Text / FOIT). This degrades FCP and user-perceived performance.

**Recommendation:** Add `font-display: swap;` to the `@font-face` declaration.

---

### 3.3 Layout thrashing in useEffect (dashboard.tsx, lines 11-13)

**Severity: High**

```tsx
const h = containerRef.current.offsetHeight; // forces reflow
containerRef.current.style.minHeight = h + "px"; // triggers another reflow
```

Reading `offsetHeight` forces a synchronous layout reflow. Immediately writing to `style.minHeight` invalidates the layout and triggers another reflow on the next read. This read-write-read pattern causes layout thrashing, which is expensive on the main thread and impacts Interaction to Next Paint (INP).

**Recommendation:** Batch DOM reads and writes separately. Use `requestAnimationFrame` to defer writes, or use CSS solutions (e.g., `min-height: fit-content`) to avoid JavaScript-based sizing entirely.

---

### 3.4 Dynamic content injection without size reservation (dashboard.tsx, lines 17-19)

**Severity: High (CLS impact)**

```tsx
setTimeout(() => {
  setItems(["Dashboard", "Analytics", "Reports"]);
}, 500);
```

Content is injected after a 500ms delay without any placeholder or size reservation. This causes Cumulative Layout Shift (CLS) as surrounding elements reposition when the items appear.

**Recommendation:**
- Reserve space with a minimum height or placeholder skeleton.
- If loading data asynchronously, show loading skeletons with fixed dimensions.

---

### 3.5 Below-fold image without lazy loading (dashboard.tsx, line 50)

**Severity: Medium**

```tsx
<img src="/public/promo.png" alt="Promo" className="mt-8" />
```

This image appears below the fold (after a grid of content) but lacks `loading="lazy"`. It will be fetched eagerly on page load, consuming bandwidth and delaying more critical resources.

**Recommendation:** Add `loading="lazy"` to below-fold images: `<img loading="lazy" ... />`.

---

### 3.6 Missing image dimensions causing CLS (dashboard.tsx, line 50)

**Severity: Medium**

The same image also lacks `width` and `height` attributes, contributing to layout shift when the image loads.

**Recommendation:** Add explicit `width` and `height` attributes.

---

### 3.7 Missing `key` prop on list items (dashboard.tsx, lines 45-47)

**Severity: Medium**

```tsx
{items.map((item) => (
  <div className="border p-2">{item}</div>
))}
```

React list items are rendered without a `key` prop. This forces React to use index-based reconciliation, which can cause unnecessary re-renders and DOM mutations, impacting rendering performance. It also generates a React console warning.

**Recommendation:** Add a stable `key` prop: `<div key={item} className="border p-2">{item}</div>`.

---

## 4. Security

### 4.1 innerHTML with user input (XSS vulnerability) (index.html, lines 38-43)

**Severity: Critical**

```js
var userInput = location.hash.slice(1);
if (label) {
  label.innerHTML = "Hello, " + userInput;
}
```

User-controlled input (`location.hash`) is directly injected into the DOM via `innerHTML` without any sanitization. This is a textbook reflected XSS vulnerability. An attacker can craft a URL like `page.html#<img src=x onerror=alert(1)>` to execute arbitrary JavaScript.

**Recommendation:** Use `textContent` instead of `innerHTML`, or sanitize input with a library like DOMPurify.

```js
label.textContent = "Hello, " + userInput;
```

---

### 4.2 Direct DOM manipulation via querySelector (Card.tsx, lines 17-20)

**Severity: Low**

```tsx
const el = document.querySelector(".card-highlight");
if (el) {
  (el as HTMLElement).style.background = "yellow";
}
```

Using `document.querySelector` inside a React component bypasses React's virtual DOM. In a list rendering context, this may select the wrong element (it will always pick the first `.card-highlight` in the document). While not a direct security vulnerability, it is an anti-pattern that could lead to unexpected behavior.

**Recommendation:** Use a React `useRef` to reference the target element directly.

---

### 4.3 Console.log in production code (Card.tsx, line 13)

**Severity: Low**

```tsx
console.log("Card clicked:", title);
```

Leaving `console.log` statements in production code can leak information and clutter the browser console.

**Recommendation:** Remove console.log statements or use a logging library with environment-aware log levels.

---

## Summary

| Category       | Critical | High | Medium | Low |
|----------------|----------|------|--------|-----|
| Accessibility  | 2        | 2    | 1      | 0   |
| SEO            | 0        | 1    | 3      | 1   |
| Performance    | 0        | 3    | 3      | 0   |
| Security       | 1        | 0    | 0      | 2   |
| **Total**      | **3**    | **6**| **7**  | **3**|

### Top Priority Fixes

1. **XSS via innerHTML** (index.html) -- Critical security vulnerability that must be fixed immediately.
2. **Missing alt attribute** (index.html) -- Critical accessibility violation.
3. **Icon buttons without accessible names** (dashboard.tsx) -- Critical accessibility violation.
4. **Non-keyboard-accessible clickable div** (Card.tsx) -- High accessibility issue.
5. **Render-blocking CSS and missing font-display** (index.html) -- High performance impact on Core Web Vitals.
6. **Layout thrashing and CLS from dynamic content** (dashboard.tsx) -- High performance impact on Core Web Vitals.
7. **Missing meta description** (index.html) -- High SEO impact.
