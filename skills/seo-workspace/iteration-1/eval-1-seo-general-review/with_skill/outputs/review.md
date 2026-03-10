## SEO & Web Performance 검토 결과 — 2026-03-10

검토 파일:
- `features/web-sample/pages/index.html`
- `features/web-sample/pages/dashboard.tsx`

### Technical SEO (11항목)

| 코드   | 우선순위 | 항목                     | 결과 | 발견된 문제 |
| ------ | -------- | ------------------------ | ---- | ----------- |
| SEO-01 | Critical | noindex 없음             | ✅   | 두 파일 모두 `noindex` 메타 태그 없음. 정상적으로 검색엔진 인덱싱 가능. |
| SEO-02 | Critical | title 태그 존재하고 고유 | ❌   | `index.html`: `<title>Sample Page</title>` — 11자로 너무 짧고 비서술적 (권장 50-60자). `dashboard.tsx`: title 태그 설정 없음 (SPA 컴포넌트에서 document.title 또는 Helmet 등으로 설정하지 않음). |
| SEO-03 | Critical | h1 하나                  | ✅   | `index.html`: `<h1>` 1개 존재. `dashboard.tsx`: `<h1>` 1개 존재. 정상. |
| SEO-04 | Critical | HTTPS 사용               | ✅   | `index.html`: 외부 링크 및 리소스 모두 `https://` 사용. `dashboard.tsx`: 외부 URL 참조 없음 (로컬 경로만 사용). |
| SEO-05 | High     | meta description         | ❌   | `index.html`: `<meta name="description">` 태그 없음 (코드 주석에서도 BAD로 표시). `dashboard.tsx`: meta description 설정 없음. |
| SEO-06 | High     | canonical URL            | ❌   | `index.html`: `<link rel="canonical">` 없음. `dashboard.tsx`: canonical 설정 없음. |
| SEO-07 | High     | 구조화 데이터 (JSON-LD)  | ❌   | `index.html`: `<script type="application/ld+json">` 없음 (코드 주석에서도 BAD로 표시). `dashboard.tsx`: JSON-LD 없음. |
| SEO-08 | Medium   | 서술적 URL 구조          | ✅   | 링크 href가 서술적 경로 사용 (`/about`, `/deals`). 불필요한 쿼리 파라미터 없음. |
| SEO-09 | High     | DOCTYPE html 선언        | ✅   | `index.html`: 첫 줄에 `<!DOCTYPE html>` 선언 존재. `dashboard.tsx`: React 컴포넌트이므로 HTML 문서 자체가 아님 — 호스트 HTML에서 선언되어야 함. |
| SEO-10 | High     | charset UTF-8 최상단     | ✅   | `index.html`: `<head>` 내 첫 번째 요소로 `<meta charset="UTF-8" />` 존재. |
| SEO-11 | High     | viewport meta 태그       | ✅   | `index.html`: `<meta name="viewport" content="width=device-width, initial-scale=1.0" />` 존재. |

### Page Experience / Web Performance (18항목)

| 코드  | 영역   | 항목                               | 결과 | 발견된 문제 |
| ----- | ------ | ---------------------------------- | ---- | ----------- |
| WP-01 | CRP    | render-blocking script 없음        | ❌   | `index.html` 37행: `<script>` 태그가 `defer`, `async`, `type="module"` 없이 `<body>` 끝에 인라인으로 존재. 인라인 스크립트는 파서 블로킹을 유발함. |
| WP-02 | CRP    | LCP fetchpriority + preload        | ❌   | `index.html`: hero 이미지(`/public/hero.png`, 27행)에 `fetchpriority="high"` 미설정. `<link rel="preload" as="image">` 미설정. LCP 후보 이미지의 우선순위 최적화 필요. |
| WP-03 | CRP    | Critical CSS 처리                  | ❌   | `index.html` 10행: `<link rel="stylesheet" href="https://cdn.example.com/styles.css" />` — 외부 CSS가 `media` 속성 없이 `<head>`에서 동기 로딩. Render-blocking CSS. |
| WP-04 | 이미지 | img width/height 또는 aspect-ratio | ❌   | `index.html` 33행: `<img src="/public/promo.png" alt="Promotional banner" />` — `width`, `height` 또는 `aspect-ratio` 미설정. CLS 위험. `dashboard.tsx` 50행: `<img src="/public/promo.png" alt="Promo" className="mt-8" />` — `width`, `height` 미설정. CLS 위험. |
| WP-05 | 이미지 | loading="lazy"                     | ❌   | `index.html` 30행: `/public/logo.png` — below-fold 가능성 있는 이미지에 `loading="lazy"` 없음. `index.html` 33행: `/public/promo.png` — `loading="lazy"` 없음. `dashboard.tsx` 50행: `/public/promo.png` — below-fold 이미지에 `loading="lazy"` 없음. |
| WP-06 | 이미지 | WebP/AVIF 포맷                     | ❌   | 모든 이미지가 `.png` 포맷 사용. `<picture>` 요소 없음. WebP/AVIF 같은 현대 포맷 미사용. `index.html`: hero.png, logo.png, promo.png. `dashboard.tsx`: promo.png. |
| WP-07 | JS     | 코드 스플리팅                      | ⚠️   | `dashboard.tsx`: `import()` 동적 import 표현식 없음. Dashboard 컴포넌트가 lazy loading 없이 정적으로 export됨. 앱 규모에 따라 코드 스플리팅 도입 권장. |
| WP-08 | JS     | 트리 쉐이킹 패턴                   | ✅   | 전체 라이브러리를 통째로 import하는 패턴 없음 (`import _ from 'lodash'` 등 미발견). React import도 named import 사용. |
| WP-09 | JS     | 레이아웃 스래싱 없음               | ❌   | `dashboard.tsx` 11-13행: `useEffect` 내에서 `offsetHeight` 읽기 직후 `style.minHeight` 쓰기 — 레이아웃 스래싱 패턴. 읽기와 쓰기를 분리하거나 `requestAnimationFrame`으로 쓰기를 지연시켜야 함. |
| WP-10 | 폰트   | font-display 최적화                | ❌   | `index.html` 13-17행: `@font-face`에서 `font-display` 속성 누락. 기본값은 `auto`(대부분 브라우저에서 `block`처럼 동작)로 FOIT(Flash of Invisible Text) 발생 → LCP 악화. `font-display: swap` 또는 `optional` 추가 필요. |
| WP-11 | 폰트   | 중요 폰트 preload                  | ❌   | `index.html`: `/fonts/custom.woff2` 폰트를 사용하지만 `<link rel="preload" as="font">` 없음. 폰트 로딩 지연으로 LCP 및 CLS에 부정적 영향. |
| WP-12 | LCP    | LCP 요소 초기 HTML 존재            | ✅   | `index.html`: hero 이미지가 초기 HTML에 존재 (JS fetch로 동적 로딩하지 않음). `dashboard.tsx`: LCP 후보인 `<h1>Dashboard</h1>`이 초기 렌더링에 포함됨. |
| WP-13 | INP    | 이벤트 핸들러 즉각 피드백          | ⚠️   | `dashboard.tsx` 29-36행: `<button>` 요소에 `onClick` 핸들러가 없어 현재 상호작용이 없음. 향후 핸들러 추가 시 즉각적 시각 피드백(loading 상태 등)을 포함할 것을 권장. |
| WP-14 | INP    | 무거운 연산 지연 처리              | ➖   | 두 파일 모두 무거운 동기 연산(큰 루프, 복잡한 계산 등)이 발견되지 않음. 해당 사항 없음. |
| WP-15 | INP    | React memo 활용                    | ⚠️   | `dashboard.tsx`: `Dashboard` 컴포넌트 내 `items.map()` 렌더링이 있으나 현재 규모에서는 성능 영향 미미. 다만 컴포넌트가 복잡해질 경우 `React.memo` 또는 `useMemo` 적용을 고려할 것. |
| WP-16 | CLS    | 뷰포트 위 동적 삽입 금지           | ✅   | `prepend()`, `insertBefore()` 등 뷰포트 위 동적 삽입 패턴 미발견. |
| WP-17 | CLS    | 애니메이션 transform/opacity       | ➖   | 두 파일 모두 CSS `transition`이나 `animation` 속성 미사용. 해당 사항 없음. |
| WP-18 | CLS    | 동적 콘텐츠 공간 예약              | ❌   | `dashboard.tsx` 17-19행: `setTimeout`으로 500ms 후 `items` 상태 업데이트 → 콘텐츠가 동적으로 삽입되면서 레이아웃 이동 발생. 삽입될 영역에 `min-height`로 공간을 미리 예약하지 않음. CLS 위험. |

### 수정 가이드

#### SEO-02: title 태그 개선
- **index.html**: `<title>Sample Page</title>`를 페이지 내용을 반영하는 50-60자 제목으로 변경. 예: `<title>Welcome to Example Store - Premium Products & Best Deals</title>`
- **dashboard.tsx**: `useEffect` 또는 `react-helmet` 등으로 `document.title` 설정 추가. 예: `document.title = "Dashboard - Analytics Overview | Example Store";`

#### SEO-05: meta description 추가
- **index.html** `<head>` 내에 추가:
  ```html
  <meta name="description" content="Explore our premium product collection with free shipping. Discover the latest deals and exclusive offers at Example Store. Shop now and save." />
  ```
- **dashboard.tsx**: Helmet 등을 통해 페이지별 meta description 설정

#### SEO-06: canonical URL 추가
- **index.html** `<head>` 내에 추가:
  ```html
  <link rel="canonical" href="https://example.com/" />
  ```

#### SEO-07: JSON-LD 구조화 데이터 추가
- **index.html** `<head>` 또는 `<body>` 끝에 Organization 또는 WebPage 스키마 추가:
  ```html
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "WebPage",
    "name": "Example Store Home",
    "url": "https://example.com/"
  }
  </script>
  ```

#### WP-01: render-blocking script 제거
- **index.html** 37행: 인라인 스크립트를 외부 파일로 분리하고 `defer` 추가하거나, DOM 조작 로직을 `DOMContentLoaded` 이벤트로 래핑:
  ```html
  <script defer src="/js/label.js"></script>
  ```

#### WP-02: LCP 이미지 우선순위 설정
- **index.html** hero 이미지에 `fetchpriority` 추가 및 preload 설정:
  ```html
  <link rel="preload" href="/public/hero.png" as="image" fetchpriority="high" />
  <img src="/public/hero.png" alt="Hero banner" width="800" height="400" fetchpriority="high" />
  ```

#### WP-03: Critical CSS 처리
- 외부 CSS를 비동기로 로딩하고, 핵심 스타일만 인라인 처리:
  ```html
  <style>/* Critical above-fold CSS here */</style>
  <link rel="preload" href="https://cdn.example.com/styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'" />
  <noscript><link rel="stylesheet" href="https://cdn.example.com/styles.css" /></noscript>
  ```

#### WP-04: 이미지 width/height 추가
- **index.html** 33행:
  ```html
  <img src="/public/promo.png" alt="Promotional banner" width="600" height="300" />
  ```
- **dashboard.tsx** 50행:
  ```html
  <img src="/public/promo.png" alt="Promo" width="600" height="300" className="mt-8" />
  ```

#### WP-05: lazy loading 추가
- below-fold 이미지에 `loading="lazy"` 추가:
  ```html
  <!-- index.html -->
  <img src="/public/logo.png" width="120" height="40" loading="lazy" />
  <img src="/public/promo.png" alt="Promotional banner" width="600" height="300" loading="lazy" />
  <!-- dashboard.tsx -->
  <img src="/public/promo.png" alt="Promo" width="600" height="300" loading="lazy" className="mt-8" />
  ```

#### WP-06: 현대 이미지 포맷 사용
- `.png` 대신 `.webp` 또는 `.avif`로 변환하고 `<picture>` 요소로 폴백 제공:
  ```html
  <picture>
    <source type="image/avif" srcset="/public/hero.avif" />
    <source type="image/webp" srcset="/public/hero.webp" />
    <img src="/public/hero.png" alt="Hero banner" width="800" height="400" />
  </picture>
  ```

#### WP-09: 레이아웃 스래싱 수정
- **dashboard.tsx** 11-13행: 읽기/쓰기를 분리하거나 `requestAnimationFrame`으로 쓰기를 지연:
  ```typescript
  useEffect(() => {
    if (containerRef.current) {
      const h = containerRef.current.offsetHeight;
      requestAnimationFrame(() => {
        if (containerRef.current) {
          containerRef.current.style.minHeight = h + "px";
        }
      });
    }
  }, []);
  ```

#### WP-10: font-display 추가
- **index.html** `@font-face` 규칙에 `font-display: swap` 추가:
  ```css
  @font-face {
    font-family: "CustomFont";
    src: url("/fonts/custom.woff2") format("woff2");
    font-display: swap;
  }
  ```

#### WP-11: 폰트 preload 추가
- **index.html** `<head>` 상단에 추가:
  ```html
  <link rel="preload" href="/fonts/custom.woff2" as="font" type="font/woff2" crossorigin />
  ```

#### WP-18: 동적 콘텐츠 공간 예약
- **dashboard.tsx**: 동적으로 삽입되는 items 영역에 `min-height`를 설정하여 CLS 방지:
  ```tsx
  <section ref={containerRef} className="grid gap-4" style={{ minHeight: '200px' }}>
  ```
