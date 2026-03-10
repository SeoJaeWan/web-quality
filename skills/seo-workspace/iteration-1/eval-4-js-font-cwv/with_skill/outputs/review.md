## SEO & Web Performance 검토 결과 — 2026-03-10

검토 파일: `features/web-sample/pages/index.html`

### Technical SEO (11항목)

| 코드   | 우선순위 | 항목                     | 결과 | 발견된 문제 |
| ------ | -------- | ------------------------ | ---- | ----------- |
| SEO-01 | Critical | noindex 없음             | ✅ | `<meta name="robots" content="noindex">` 없음. 정상. |
| SEO-02 | Critical | title 태그 존재하고 고유 | ⚠️ | `<title>Sample Page</title>` (line 6) — 11자로 너무 짧고 비서술적. 50-60자 권장. 주요 키워드를 포함한 고유 제목 필요. |
| SEO-03 | Critical | h1 하나                  | ✅ | `<h1>` 1개 존재 (line 21). |
| SEO-04 | Critical | HTTPS 사용               | ✅ | 외부 리소스(`cdn.example.com/styles.css`, `example.com` 링크) 모두 HTTPS 사용. |
| SEO-05 | High     | meta description         | ❌ | `<meta name="description">` 태그 누락. 150-160자의 설명 추가 필요. |
| SEO-06 | High     | canonical URL            | ❌ | `<link rel="canonical">` 태그 누락. 중복 콘텐츠 방지를 위해 canonical URL 설정 필요. |
| SEO-07 | High     | 구조화 데이터 (JSON-LD)  | ❌ | `<script type="application/ld+json">` 없음. 페이지 유형에 맞는 JSON-LD 구조화 데이터 추가 권장. |
| SEO-08 | Medium   | 서술적 URL 구조          | ➖ | 단일 HTML 파일 분석으로 URL 구조 평가 불가. |
| SEO-09 | High     | DOCTYPE html 선언        | ✅ | `<!DOCTYPE html>` 선언 존재 (line 1). |
| SEO-10 | High     | charset UTF-8 최상단     | ✅ | `<meta charset="UTF-8" />` `<head>` 최상단에 위치 (line 4). |
| SEO-11 | High     | viewport meta 태그       | ✅ | `<meta name="viewport" content="width=device-width, initial-scale=1.0" />` 존재 (line 5). |

### Page Experience / Web Performance (18항목)

| 코드  | 영역   | 항목                               | 결과 | 발견된 문제 |
| ----- | ------ | ---------------------------------- | ---- | ----------- |
| WP-01 | CRP    | render-blocking script 없음        | ❌ | line 37-44: `<script>` 태그에 `defer`, `async`, `type="module"` 없이 인라인 스크립트가 `<body>` 끝에 위치. 인라인이므로 외부 fetch는 없으나, DOM 조작 코드가 동기적으로 실행되어 렌더링을 차단할 수 있음. `defer` 속성이 있는 외부 스크립트로 분리하거나 `DOMContentLoaded` 이벤트 내에서 실행하는 것을 권장. |
| WP-02 | CRP    | LCP fetchpriority + preload        | ❌ | hero.png 이미지(line 27)가 LCP 후보이나 `fetchpriority="high"` 속성 없음. `<link rel="preload" as="image" href="/public/hero.png" fetchpriority="high">` 추가 필요. |
| WP-03 | CRP    | Critical CSS 처리                  | ❌ | line 10: `<link rel="stylesheet" href="https://cdn.example.com/styles.css" />` — 외부 CSS가 `media` 속성 없이 동기적으로 로드되어 렌더링 차단. critical CSS를 인라인하고, 나머지는 비동기 로딩(`preload` + `onload` 패턴) 적용 필요. |
| WP-04 | 이미지 | img width/height 또는 aspect-ratio | ❌ | line 33: `<img src="/public/promo.png" alt="Promotional banner" />` — `width`/`height` 또는 `aspect-ratio` 누락. CLS(레이아웃 이동) 발생 위험. |
| WP-05 | 이미지 | loading="lazy"                     | ❌ | line 30: `<img src="/public/logo.png">` — below-fold 가능성 있는 이미지에 `loading="lazy"` 없음. line 33: `<img src="/public/promo.png">` — `loading="lazy"` 없음. LCP 이미지(hero.png)를 제외한 나머지 이미지에 `loading="lazy"` 추가 필요. |
| WP-06 | 이미지 | WebP/AVIF 포맷                     | ❌ | 모든 이미지가 `.png` 포맷 사용. `<picture>` 요소를 통한 WebP/AVIF 최신 포맷 제공 없음. 파일 크기 절감을 위해 WebP/AVIF 변환 권장. |
| WP-07 | JS     | 코드 스플리팅                      | ⚠️ | 동적 `import()` 표현식 없음. 현재 인라인 스크립트만 존재하여 코드 스플리팅이 적용되지 않음. 앱 규모가 커지면 route/component 기반 코드 스플리팅 도입 권장. |
| WP-08 | JS     | 트리 쉐이킹 패턴                   | ✅ | 외부 라이브러리 전체 import(`import _ from 'lodash'` 등) 패턴 발견되지 않음. |
| WP-09 | JS     | 레이아웃 스래싱 없음               | ✅ | 루프 내 레이아웃 속성 읽기/쓰기 혼합 패턴 없음. `getElementById` + `innerHTML` 단일 호출만 존재. |
| WP-10 | 폰트   | font-display 최적화                | ❌ | line 13-17: `@font-face`에서 `font-display` 속성 누락. `font-display: swap` (또는 `optional`/`fallback`) 추가 필요. 현재 상태에서는 폰트 로딩 중 텍스트가 보이지 않는 FOIT(Flash of Invisible Text) 발생. |
| WP-11 | 폰트   | 중요 폰트 preload                  | ❌ | `/fonts/custom.woff2` 폰트에 대한 `<link rel="preload" as="font" type="font/woff2" crossorigin>` 누락. 중요 폰트를 preload하여 로딩 시간 단축 필요. |
| WP-12 | LCP    | LCP 요소 초기 HTML 존재            | ✅ | hero.png 이미지가 초기 HTML에 직접 포함 (line 27). JS 의존적 렌더링 아님. |
| WP-13 | INP    | 이벤트 핸들러 즉각 피드백          | ➖ | 이벤트 핸들러(click 등) 바인딩 없음. 평가 대상 없음. |
| WP-14 | INP    | 무거운 연산 지연 처리              | ➖ | 동기적 무거운 연산(큰 루프 등) 없음. 평가 대상 없음. |
| WP-15 | INP    | React memo 활용                    | ➖ | React 프레임워크 사용하지 않음. 해당 없음. |
| WP-16 | CLS    | 뷰포트 위 동적 삽입 금지           | ✅ | `prepend()`, `insertBefore()` 등 뷰포트 위 동적 삽입 패턴 없음. |
| WP-17 | CLS    | 애니메이션 transform/opacity       | ➖ | CSS transition/animation 사용 없음. 평가 대상 없음. |
| WP-18 | CLS    | 동적 콘텐츠 공간 예약              | ➖ | `<iframe>`, `<video>`, 광고 슬롯 등 동적 콘텐츠 요소 없음. 해당 없음. |

### 수정 가이드

#### WP-01: render-blocking script

인라인 스크립트를 외부 파일로 분리하고 `defer` 속성 적용:

```html
<!-- 변경 전 (line 37-44) -->
<script>
  var label = document.getElementById("label");
  var userInput = location.hash.slice(1);
  if (label) { label.innerHTML = "Hello, " + userInput; }
</script>

<!-- 변경 후 -->
<script defer src="/js/label.js"></script>
```

참고: `innerHTML`에 사용자 입력(`location.hash`)을 직접 삽입하는 것은 XSS 보안 취약점이므로 `textContent` 사용을 강력 권장합니다.

#### WP-02: LCP fetchpriority + preload

`<head>`에 LCP 이미지 preload 추가:

```html
<link rel="preload" href="/public/hero.png" as="image" fetchpriority="high">
```

`<img>` 태그에도 fetchpriority 추가:

```html
<img src="/public/hero.png" alt="Hero banner" width="800" height="400" fetchpriority="high">
```

#### WP-03: Critical CSS 처리

외부 CSS를 비동기로 전환:

```html
<!-- Critical CSS 인라인 -->
<style>/* 위 fold에 필요한 최소 스타일 */</style>

<!-- 나머지 CSS 비동기 로딩 -->
<link rel="preload" href="https://cdn.example.com/styles.css" as="style"
      onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="https://cdn.example.com/styles.css"></noscript>
```

#### WP-04: img width/height (CLS 방지)

`promo.png` 이미지에 dimensions 추가:

```html
<!-- 변경 전 (line 33) -->
<img src="/public/promo.png" alt="Promotional banner" />

<!-- 변경 후 -->
<img src="/public/promo.png" alt="Promotional banner" width="800" height="400" loading="lazy">
```

#### WP-05: loading="lazy"

LCP 이미지가 아닌 이미지에 lazy loading 추가:

```html
<img src="/public/logo.png" width="120" height="40" loading="lazy" alt="Logo">
<img src="/public/promo.png" alt="Promotional banner" width="800" height="400" loading="lazy">
```

#### WP-06: WebP/AVIF 포맷

`<picture>` 요소로 최신 포맷 제공:

```html
<picture>
  <source type="image/avif" srcset="/public/hero.avif">
  <source type="image/webp" srcset="/public/hero.webp">
  <img src="/public/hero.png" alt="Hero banner" width="800" height="400" fetchpriority="high">
</picture>
```

#### WP-10: font-display 최적화

`@font-face`에 `font-display: swap` 추가:

```css
@font-face {
  font-family: "CustomFont";
  src: url("/fonts/custom.woff2") format("woff2");
  font-display: swap; /* 추가 */
}
```

#### WP-11: 중요 폰트 preload

`<head>`에 폰트 preload 추가:

```html
<link rel="preload" href="/fonts/custom.woff2" as="font" type="font/woff2" crossorigin>
```

#### SEO-05: meta description 추가

```html
<meta name="description" content="Welcome to Sample Page - your destination for quality content and services. Explore our offerings and discover what makes us different.">
```

#### SEO-06: canonical URL 추가

```html
<link rel="canonical" href="https://example.com/">
```

#### SEO-07: 구조화 데이터 추가

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "Sample Page",
  "url": "https://example.com/"
}
</script>
```
