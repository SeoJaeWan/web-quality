# Web Quality Audit Report

**Target files:**
- `features/web-sample/pages/index.html`
- `features/web-sample/components/Card.tsx`

---

## 1. Accessibility

### index.html

| Severity | Issue | Location | Description | Recommendation |
|----------|-------|----------|-------------|----------------|
| Critical | Missing `alt` attribute on image | Line 30 | `<img src="/public/logo.png" width="120" height="40" />` has no `alt` attribute. Screen readers cannot convey the image's purpose. Violates WCAG 2.1 SC 1.1.1 (Non-text Content). | Add a descriptive `alt` attribute, or `alt=""` if purely decorative. |
| Major | No landmark regions | Entire file | The page body has no `<header>`, `<nav>`, `<main>`, or `<footer>` elements. Screen reader users cannot navigate by landmark. Violates WCAG 2.1 SC 1.3.1 (Info and Relationships). | Wrap content in appropriate semantic landmark elements. |
| Major | No skip-navigation link | Entire file | There is no mechanism to skip repeated blocks of content. Violates WCAG 2.1 SC 2.4.1 (Bypass Blocks). | Add a "Skip to main content" link at the top of `<body>`. |
| Minor | `<html lang="en">` is present | Line 2 | Correct language attribute is set. | No action needed. (PASS) |

### Card.tsx

| Severity | Issue | Location | Description | Recommendation |
|----------|-------|----------|-------------|----------------|
| Critical | Non-interactive element has `onClick` without keyboard support | Line 29 | The `<div>` has an `onClick` handler but lacks `role="button"`, `tabIndex={0}`, and `onKeyDown`/`onKeyPress` handlers. Keyboard-only and screen reader users cannot activate this control. Violates WCAG 2.1 SC 2.1.1 (Keyboard). | Either use a `<button>` element, or add `role="button"`, `tabIndex={0}`, and a key event handler that triggers on Enter/Space. |
| Major | Duplicate `id="card-item"` when rendered in a list | Line 27 | If this component is rendered multiple times, every instance gets the same `id`. Duplicate IDs break `getElementById`, ARIA references (`aria-labelledby`, `aria-describedby`), and assistive technology assumptions. Violates HTML spec and WCAG 2.1 SC 4.1.1 (Parsing). | Generate unique IDs per instance (e.g., pass an `id` prop or use `useId()` from React 18+). |
| Minor | Heading level may break hierarchy | Line 31 | Uses `<h3>` directly. If the Card is placed without a preceding `<h2>`, the heading hierarchy is broken. Violates WCAG 2.1 SC 1.3.1. | Consider making the heading level configurable via props, or verify usage context. |

---

## 2. SEO

### index.html

| Severity | Issue | Location | Description | Recommendation |
|----------|-------|----------|-------------|----------------|
| Critical | Missing meta description | `<head>` | No `<meta name="description" content="...">` tag. Search engines will auto-generate a snippet, often poorly. | Add a concise, unique meta description (120-160 characters). |
| Critical | Missing structured data (JSON-LD) | `<head>` | No structured data markup. The page cannot appear as a rich result in search. | Add appropriate JSON-LD (`WebPage`, `Organization`, `BreadcrumbList`, etc.). |
| Major | Generic `<title>` | Line 6 | `<title>Sample Page</title>` is not descriptive. Title tags are the single most impactful on-page SEO element. | Use a descriptive, keyword-rich title (50-60 characters). |
| Major | No canonical URL | `<head>` | No `<link rel="canonical" href="...">`. Duplicate content issues may arise. | Add a canonical link pointing to the preferred URL. |
| Major | No Open Graph / Twitter Card tags | `<head>` | No `og:title`, `og:description`, `og:image`, or `twitter:card` meta tags. Social sharing will lack rich previews. | Add Open Graph and Twitter Card meta tags. |
| Minor | No `robots` meta tag | `<head>` | While the default is to index/follow, explicitly setting it is good practice. | Add `<meta name="robots" content="index, follow">` if appropriate. |
| Minor | Links lack descriptive anchor text | Line 35 | "latest deals" is acceptable, but "About Us" on line 24 could benefit from more context depending on site structure. | Ensure anchor text is descriptive and relevant to the linked page. |

### Card.tsx

| Severity | Issue | Location | Description | Recommendation |
|----------|-------|----------|-------------|----------------|
| Info | Component is SEO-neutral | -- | As a React component, its SEO impact depends on whether it is server-side rendered (SSR/SSG). If client-side only, its content is invisible to crawlers that do not execute JavaScript. | Ensure the host application uses SSR or SSG (Next.js, Remix, etc.) so Card content is in the initial HTML. |

---

## 3. Performance

### index.html

| Severity | Issue | Location | Description | Recommendation |
|----------|-------|----------|-------------|----------------|
| Critical | Render-blocking external CSS | Line 10 | `<link rel="stylesheet" href="https://cdn.example.com/styles.css" />` blocks first paint. This directly impacts FCP and LCP. | Inline critical CSS, defer non-critical CSS with `media="print" onload="this.media='all'"`, or use `rel="preload"` with `as="style"`. |
| Critical | Missing `font-display: swap` | Lines 13-17 | The `@font-face` declaration does not include `font-display: swap`. This causes invisible text during font loading (FOIT), directly hurting FCP and LCP. | Add `font-display: swap;` to the `@font-face` rule. |
| Major | Inline script blocks parsing | Lines 37-44 | The `<script>` block at the end of `<body>` is synchronous. While placement at the bottom mitigates some blocking, it still holds up the `DOMContentLoaded` event. | Move the script to an external file and use `defer` or `async`. |
| Major | Image missing explicit dimensions (CLS risk) | Line 33 | `<img src="/public/promo.png" alt="Promotional banner" />` has no `width` or `height` attributes. The browser cannot reserve space, causing layout shift (CLS). | Add `width` and `height` attributes matching the image's intrinsic dimensions. |
| Minor | No resource hints | `<head>` | No `<link rel="preconnect">` or `<link rel="dns-prefetch">` for the external CDN domain. | Add `<link rel="preconnect" href="https://cdn.example.com" crossorigin>`. |
| Minor | No image lazy loading | Lines 27, 30, 33 | Below-the-fold images are not marked with `loading="lazy"`. | Add `loading="lazy"` to images that are not part of the initial viewport (keep the hero image eager). |
| Minor | Images not using modern format | Lines 27, 30, 33 | All images use `.png`. Modern formats like WebP or AVIF offer significantly smaller file sizes. | Convert images to WebP/AVIF with PNG fallbacks using `<picture>`. |

### Card.tsx

| Severity | Issue | Location | Description | Recommendation |
|----------|-------|----------|-------------|----------------|
| Major | Direct DOM manipulation via `document.querySelector` | Line 17 | Bypasses React's virtual DOM, causing potential unnecessary reflows and repaints. This is both a performance and maintainability issue. | Use a React `useRef` to reference the target element directly. |
| Minor | `console.log` left in production code | Line 13 | Console calls have a small but non-zero performance cost and are inappropriate in production. | Remove or gate behind a development environment check (`process.env.NODE_ENV === 'development'`). |
| Minor | String concatenation for `className` | Line 28 | `` `rounded border p-4 ${className}` `` can produce trailing spaces when `className` is empty. Not a performance issue per se, but using a utility like `clsx` or `classnames` is cleaner. | Use `clsx` or `classnames` for conditional class merging. |

---

## 4. Security

### index.html

| Severity | Issue | Location | Description | Recommendation |
|----------|-------|----------|-------------|----------------|
| Critical | XSS via `innerHTML` with unsanitized user input | Lines 37-44 | `label.innerHTML = "Hello, " + userInput` where `userInput` comes from `location.hash`. An attacker can inject arbitrary HTML/JavaScript via the URL hash. | Use `textContent` instead of `innerHTML`, or sanitize input with a library like DOMPurify. |
| Major | No Content Security Policy (CSP) | `<head>` | No CSP meta tag or header reference. This provides no defense-in-depth against XSS. | Add a CSP meta tag or configure CSP headers on the server. |

---

## Summary

| Category | Critical | Major | Minor | Info |
|----------|----------|-------|-------|------|
| Accessibility | 2 | 3 | 1 | 0 |
| SEO | 2 | 3 | 2 | 1 |
| Performance | 2 | 3 | 3 | 0 |
| Security | 1 | 1 | 0 | 0 |
| **Total** | **7** | **10** | **6** | **1** |

### Top Priority Fixes

1. **XSS vulnerability** (`innerHTML` with unsanitized `location.hash`) -- immediate security risk.
2. **Missing `alt` on logo image** -- accessibility compliance failure.
3. **Clickable `<div>` without keyboard support** in Card.tsx -- excludes keyboard users.
4. **Missing meta description and structured data** -- significant SEO gap.
5. **Render-blocking CSS and missing `font-display: swap`** -- directly degrades Core Web Vitals (FCP, LCP).
6. **Missing image dimensions on promo image** -- causes layout shift (CLS).
7. **Duplicate `id` in Card component** -- breaks HTML validity and assistive technology.
