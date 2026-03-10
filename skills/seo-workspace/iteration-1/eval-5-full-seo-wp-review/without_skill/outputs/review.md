# SEO + Web Performance Comprehensive Review

**Reviewed files:**
- `features/web-sample/pages/index.html`
- `features/web-sample/pages/dashboard.tsx`
- `features/web-sample/components/Card.tsx`

---

## SEO Issues

### SEO-01: Missing Meta Description

**File:** `index.html` (line 7)
**Severity:** High

`<meta name="description" content="...">` 태그가 없다. 검색엔진 결과 페이지(SERP)에서 snippet으로 표시되는 핵심 요소이며, CTR에 직접적인 영향을 준다.

**권장 수정:**
```html
<meta name="description" content="사이트의 핵심 내용을 요약한 150~160자 이내의 설명" />
```

---

### SEO-02: Title Tag Too Generic

**File:** `index.html` (line 6)
**Severity:** Medium

`<title>Sample Page</title>`는 페이지 내용을 전혀 반영하지 않는 범용적인 제목이다. 검색엔진이 페이지 주제를 파악하기 어렵고, SERP에서도 구분이 되지 않는다.

**권장 수정:**
브랜드명과 페이지 주제를 포함한 구체적 제목으로 변경. 예: `<title>Latest Deals & Promotions | BrandName</title>`

---

### SEO-03: Missing Structured Data (JSON-LD)

**File:** `index.html` (line 8)
**Severity:** Medium

JSON-LD 구조화 데이터가 없다. Rich snippet(별점, 가격, FAQ 등)을 획득할 기회를 놓치고 있다. 검색 결과에서의 가시성 및 CTR 향상에 기여한다.

**권장 수정:**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "Page Title",
  "description": "Page description"
}
</script>
```

---

### SEO-04: Missing Canonical URL

**File:** `index.html`
**Severity:** Medium

`<link rel="canonical" href="..." />` 태그가 없다. 중복 콘텐츠 문제가 발생할 수 있으며, 검색엔진이 정규 URL을 올바르게 인식하지 못할 수 있다.

**권장 수정:**
```html
<link rel="canonical" href="https://example.com/" />
```

---

### SEO-05: Missing Open Graph / Social Meta Tags

**File:** `index.html`
**Severity:** Low

`og:title`, `og:description`, `og:image`, `twitter:card` 등의 소셜 메타 태그가 없다. SNS 공유 시 미리보기가 올바르게 표시되지 않아 트래픽 유입에 불리하다.

**권장 수정:**
```html
<meta property="og:title" content="Page Title" />
<meta property="og:description" content="Page description" />
<meta property="og:image" content="https://example.com/og-image.png" />
<meta name="twitter:card" content="summary_large_image" />
```

---

### SEO-06: Image Missing Alt Attribute

**File:** `index.html` (line 30)
**Severity:** High

```html
<img src="/public/logo.png" width="120" height="40" />
```

`alt` 속성이 누락되어 있다. 검색엔진이 이미지 내용을 파악할 수 없고, 이미지 검색 노출 기회를 잃는다. 또한 접근성 위반(WCAG 1.1.1)이기도 하다.

**권장 수정:**
```html
<img src="/public/logo.png" alt="Company logo" width="120" height="40" />
```

---

### SEO-07: Missing Robots Meta Tag

**File:** `index.html`
**Severity:** Low

`<meta name="robots" content="index, follow" />` 태그가 없다. 기본 동작은 index/follow이지만, 명시적으로 선언하는 것이 크롤링 제어에 유리하다.

---

### SEO-08: No Heading Hierarchy Issues in HTML (Positive Note)

**File:** `index.html`
**Severity:** Info

`index.html`에서 `<h1>`이 1개만 사용되어 올바른 heading 구조를 갖추고 있다.

**File:** `dashboard.tsx`
**Severity:** Info (Positive)

`<h1>` -> `<h2>` 순서로 적절한 heading 계층 구조를 유지하고 있다.

---

### SEO-09: Missing hreflang / Language Alternates

**File:** `index.html`
**Severity:** Low

다국어 지원 시 `<link rel="alternate" hreflang="..." href="..." />` 태그가 필요하다. 현재 `lang="en"`만 설정되어 있으며, 다국어 대상이 아니라면 문제없다.

---

### SEO-10: No Sitemap or Robots.txt Reference

**File:** 전체
**Severity:** Low

사이트맵이나 robots.txt에 대한 참조가 없다. 크롤링 효율성을 높이려면 sitemap 생성 및 robots.txt 설정이 필요하다.

---

### SEO-11: Duplicate ID Pattern Harms SEO Semantics

**File:** `Card.tsx` (line 27)
**Severity:** Medium

```tsx
id="card-item"
```

Card 컴포넌트가 리스트에서 반복 렌더링될 경우 동일한 `id`가 여러 번 출현한다. HTML 명세상 `id`는 고유해야 하며, 중복 ID는 검색엔진의 DOM 파싱을 혼란시킬 수 있다. 또한 fragment 링크(`#card-item`) 사용 시 올바른 요소로 이동하지 못한다.

**권장 수정:**
동적 ID를 사용하거나 `id` 대신 `className`이나 `data-*` 속성을 활용한다.

---

## Web Performance Issues

### WP-01: Render-Blocking CSS in Head

**File:** `index.html` (line 10)
**Severity:** High

```html
<link rel="stylesheet" href="https://cdn.example.com/styles.css" />
```

외부 CSS가 동기적으로 로드되어 렌더링을 차단한다. FCP(First Contentful Paint)와 LCP(Largest Contentful Paint)를 지연시킨다.

**권장 수정:**
- Critical CSS를 inline으로 삽입하고, 나머지는 `media="print" onload="this.media='all'"` 패턴 또는 `rel="preload"`로 비동기 로드한다.
```html
<link rel="preload" href="https://cdn.example.com/styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'" />
```

---

### WP-02: Missing font-display: swap

**File:** `index.html` (lines 13-17)
**Severity:** High

```css
@font-face {
  font-family: "CustomFont";
  src: url("/fonts/custom.woff2") format("woff2");
  /* missing: font-display: swap */
}
```

`font-display: swap`이 없으면 커스텀 폰트 로드 완료 전까지 텍스트가 보이지 않는 FOIT(Flash of Invisible Text)가 발생한다. FCP에 직접적인 영향을 준다.

**권장 수정:**
```css
font-display: swap;
```

---

### WP-03: No Font Preload

**File:** `index.html`
**Severity:** Medium

커스텀 폰트(`custom.woff2`)에 대한 `<link rel="preload">` 선언이 없다. 폰트 파일 발견이 CSS 파싱 이후로 지연되어 LCP에 부정적 영향을 줄 수 있다.

**권장 수정:**
```html
<link rel="preload" href="/fonts/custom.woff2" as="font" type="font/woff2" crossorigin />
```

---

### WP-04: Image Missing Width/Height (CLS Risk)

**File:** `index.html` (line 33)
**Severity:** High

```html
<img src="/public/promo.png" alt="Promotional banner" />
```

`width`와 `height` 속성이 없어 브라우저가 이미지 로드 전 공간을 예약하지 못한다. 이미지 로드 시 레이아웃이 밀려나 CLS(Cumulative Layout Shift) 점수가 악화된다.

**권장 수정:**
```html
<img src="/public/promo.png" alt="Promotional banner" width="800" height="400" />
```

---

### WP-05: Image Missing Width/Height in Dashboard (CLS Risk)

**File:** `dashboard.tsx` (line 50)
**Severity:** High

```tsx
<img src="/public/promo.png" alt="Promo" className="mt-8" />
```

마찬가지로 `width`/`height`가 없어 CLS 유발 요인이다. CSS의 `aspect-ratio`를 사용하거나 명시적 크기를 지정해야 한다.

**권장 수정:**
```tsx
<img src="/public/promo.png" alt="Promo" width="800" height="400" className="mt-8" />
```

---

### WP-06: Missing lazy loading for Below-Fold Image

**File:** `dashboard.tsx` (line 50)
**Severity:** Medium

아래쪽(below-fold)에 위치한 이미지에 `loading="lazy"` 속성이 없다. 초기 로드 시 불필요한 네트워크 리소스를 소비하여 LCP 및 전체 페이지 로드 타임에 부정적 영향을 준다.

**권장 수정:**
```tsx
<img src="/public/promo.png" alt="Promo" width="800" height="400" loading="lazy" className="mt-8" />
```

---

### WP-07: No Image Format Optimization (WebP/AVIF)

**File:** `index.html`, `dashboard.tsx`
**Severity:** Medium

모든 이미지가 `.png` 형식이다. WebP나 AVIF 등 차세대 이미지 포맷을 사용하면 파일 크기를 30~50% 절감할 수 있어 로드 시간이 크게 개선된다.

**권장 수정:**
`<picture>` 태그로 포맷 분기 처리:
```html
<picture>
  <source srcset="/public/hero.avif" type="image/avif" />
  <source srcset="/public/hero.webp" type="image/webp" />
  <img src="/public/hero.png" alt="Hero banner" width="800" height="400" />
</picture>
```

---

### WP-08: No srcset/sizes for Responsive Images

**File:** `index.html` (line 27), `dashboard.tsx` (line 50)
**Severity:** Medium

`srcset`과 `sizes` 속성이 없다. 모바일 기기에서도 데스크톱 크기의 이미지를 다운로드하게 되어 불필요한 대역폭 소비가 발생한다.

**권장 수정:**
```html
<img src="/public/hero.png" srcset="/public/hero-480.png 480w, /public/hero-800.png 800w" sizes="(max-width: 600px) 480px, 800px" alt="Hero banner" width="800" height="400" />
```

---

### WP-09: Inline Script Blocks Rendering

**File:** `index.html` (lines 37-44)
**Severity:** Medium

`<body>` 내부의 인라인 `<script>`는 파싱을 차단한다. 또한 `innerHTML`을 사용하여 XSS 위험도 있다.

**권장 수정:**
- 스크립트를 외부 파일로 분리하고 `defer` 또는 `async` 속성을 사용한다.
- `innerHTML` 대신 `textContent`를 사용한다.

---

### WP-10: Layout Thrashing in useEffect

**File:** `dashboard.tsx` (lines 10-14)
**Severity:** High

```tsx
const h = containerRef.current.offsetHeight; // forces reflow
containerRef.current.style.minHeight = h + "px"; // triggers another reflow
```

`offsetHeight` 읽기 직후 `style.minHeight`를 쓰면 강제 동기 리플로우(forced synchronous layout)가 발생한다. 이 패턴은 프레임 드랍과 INP(Interaction to Next Paint) 악화를 유발한다.

**권장 수정:**
- `requestAnimationFrame`을 사용하여 읽기와 쓰기를 분리한다.
- 또는 CSS만으로 `min-height`를 설정한다.

---

### WP-11: Dynamic Content Without Size Reservation (CLS)

**File:** `dashboard.tsx` (lines 16-19)
**Severity:** High

```tsx
setTimeout(() => {
  setItems(["Dashboard", "Analytics", "Reports"]);
}, 500);
```

500ms 후 동적으로 콘텐츠가 삽입되면서 레이아웃이 밀려나는 CLS 문제가 발생한다. 콘텐츠가 추가될 영역의 최소 높이를 미리 확보해야 한다.

**권장 수정:**
- `min-height`를 CSS로 미리 설정하여 공간을 예약한다.
- skeleton UI를 사용하여 로드 전에도 동일한 공간을 차지하도록 한다.

---

### WP-12: No Resource Hints (preconnect, dns-prefetch)

**File:** `index.html`
**Severity:** Medium

외부 CDN(`cdn.example.com`)에 대한 `preconnect`나 `dns-prefetch` 힌트가 없다. DNS 조회 및 TCP 연결 시간을 절약할 수 있다.

**권장 수정:**
```html
<link rel="preconnect" href="https://cdn.example.com" />
<link rel="dns-prefetch" href="https://cdn.example.com" />
```

---

### WP-13: No Critical CSS Inlining Strategy

**File:** `index.html`
**Severity:** Medium

Above-the-fold 렌더링에 필요한 critical CSS가 별도로 인라인되어 있지 않고, 전체 외부 CSS에 의존하고 있다. 이로 인해 FCP가 지연된다.

---

### WP-14: console.log in Production Code

**File:** `Card.tsx` (line 13)
**Severity:** Low

```tsx
console.log("Card clicked:", title);
```

프로덕션 코드에 `console.log`가 남아 있다. 성능에 직접적 영향은 작지만, 빈번한 호출 시 메인 스레드를 점유하고, 메모리 누수의 원인이 될 수 있다.

**권장 수정:**
프로덕션 빌드에서 console 문을 제거하거나 빌드 도구(Terser 등)로 자동 strip 설정.

---

### WP-15: Direct DOM Manipulation Instead of React Refs

**File:** `Card.tsx` (lines 17-20)
**Severity:** Medium

```tsx
const el = document.querySelector(".card-highlight");
if (el) {
  (el as HTMLElement).style.background = "yellow";
}
```

React 컴포넌트 내에서 `document.querySelector`로 직접 DOM을 조작하고 있다. React의 가상 DOM과 충돌할 수 있으며, 불필요한 리플로우를 유발한다. `useRef`를 사용해야 한다.

---

### WP-16: Missing key Prop in List Rendering

**File:** `dashboard.tsx` (lines 45-47)
**Severity:** Medium

```tsx
{items.map((item) => (
  <div className="border p-2">{item}</div>
))}
```

`key` prop이 없다. React의 reconciliation 효율이 떨어지며, 리스트가 변경될 때 불필요한 DOM 업데이트가 발생하여 렌더링 성능이 저하된다.

**권장 수정:**
```tsx
{items.map((item) => (
  <div key={item} className="border p-2">{item}</div>
))}
```

---

### WP-17: No Code Splitting / Lazy Loading for Components

**File:** `dashboard.tsx`, `Card.tsx`
**Severity:** Low

컴포넌트가 정적으로 import되어 있다. 페이지 규모가 커질 경우 `React.lazy`와 `Suspense`를 활용한 코드 스플리팅이 초기 로드 번들 크기를 줄이는 데 도움이 된다.

---

### WP-18: No Compression / Caching Headers Consideration

**File:** 전체
**Severity:** Low

정적 리소스(CSS, 이미지, 폰트)에 대한 gzip/brotli 압축이나 cache-control 헤더에 대한 고려가 보이지 않는다. 서버 설정 영역이지만, 성능 최적화의 기본 요소이다.

---

## Summary Table

| ID | Category | Severity | File | Issue |
|---|---|---|---|---|
| SEO-01 | SEO | High | index.html | Missing meta description |
| SEO-02 | SEO | Medium | index.html | Generic title tag |
| SEO-03 | SEO | Medium | index.html | No JSON-LD structured data |
| SEO-04 | SEO | Medium | index.html | Missing canonical URL |
| SEO-05 | SEO | Low | index.html | No Open Graph / social meta tags |
| SEO-06 | SEO | High | index.html | Image missing alt attribute |
| SEO-07 | SEO | Low | index.html | Missing robots meta tag |
| SEO-08 | SEO | Info | index.html, dashboard.tsx | Heading hierarchy OK |
| SEO-09 | SEO | Low | index.html | No hreflang tags |
| SEO-10 | SEO | Low | All | No sitemap/robots.txt reference |
| SEO-11 | SEO | Medium | Card.tsx | Duplicate ID pattern |
| WP-01 | Performance | High | index.html | Render-blocking CSS |
| WP-02 | Performance | High | index.html | Missing font-display: swap |
| WP-03 | Performance | Medium | index.html | No font preload |
| WP-04 | Performance | High | index.html | Image missing width/height (CLS) |
| WP-05 | Performance | High | dashboard.tsx | Image missing width/height (CLS) |
| WP-06 | Performance | Medium | dashboard.tsx | No lazy loading for below-fold image |
| WP-07 | Performance | Medium | index.html, dashboard.tsx | No next-gen image formats |
| WP-08 | Performance | Medium | index.html, dashboard.tsx | No srcset/sizes |
| WP-09 | Performance | Medium | index.html | Inline script blocks rendering |
| WP-10 | Performance | High | dashboard.tsx | Layout thrashing in useEffect |
| WP-11 | Performance | High | dashboard.tsx | Dynamic content without size reservation (CLS) |
| WP-12 | Performance | Medium | index.html | No resource hints (preconnect) |
| WP-13 | Performance | Medium | index.html | No critical CSS inlining |
| WP-14 | Performance | Low | Card.tsx | console.log in production |
| WP-15 | Performance | Medium | Card.tsx | Direct DOM manipulation instead of refs |
| WP-16 | Performance | Medium | dashboard.tsx | Missing key prop in list |
| WP-17 | Performance | Low | dashboard.tsx, Card.tsx | No code splitting |
| WP-18 | Performance | Low | All | No compression/caching consideration |

**High severity issues: 7** | **Medium severity issues: 13** | **Low severity issues: 7** | **Info: 1**

Core Web Vitals 관점에서 가장 시급한 항목:
- **LCP:** WP-01 (render-blocking CSS), WP-02 (font-display), WP-03 (font preload)
- **CLS:** WP-04, WP-05 (image dimensions), WP-11 (dynamic content)
- **INP:** WP-10 (layout thrashing), WP-15 (direct DOM manipulation)
