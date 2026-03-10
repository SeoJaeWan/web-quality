## SEO & Web Performance 검토 결과 — 2026-03-10

검토 파일: `features/web-sample/pages/index.html`

### Technical SEO (11항목)

| 코드   | 우선순위 | 항목                     | 결과 | 발견된 문제 |
| ------ | -------- | ------------------------ | ---- | ----------- |
| SEO-01 | Critical | noindex 없음             | ✅ | `<meta name="robots" content="noindex"` 태그 없음. 정상적으로 인덱싱 가능. |
| SEO-02 | Critical | title 태그 존재하고 고유 | ❌ | `<title>Sample Page</title>` (11자) — 50-60자 권장 범위에 크게 미달. 제목이 너무 일반적이며 키워드가 없음. |
| SEO-03 | Critical | h1 하나                  | ✅ | `<h1>Welcome to the Sample Page</h1>` 하나만 존재. |
| SEO-04 | Critical | HTTPS 사용               | ✅ | 외부 리소스(`https://cdn.example.com/styles.css`, `https://example.com/about`, `https://example.com/deals`) 모두 HTTPS 사용. 로컬 리소스(`/public/hero.png` 등)는 상대 경로로 문제 없음. |
| SEO-05 | High     | meta description         | ❌ | `<meta name="description"` 태그가 완전히 누락됨. 7행 주석에도 명시: `<!-- BAD: no meta description -->`. 150-160자의 고유한 설명 필요. |
| SEO-06 | High     | canonical URL            | ❌ | `<link rel="canonical"` 태그 누락. 중복 콘텐츠 문제 발생 가능. |
| SEO-07 | High     | 구조화 데이터 (JSON-LD)  | ❌ | `<script type="application/ld+json"` 완전히 누락. 8행 주석에도 명시: `<!-- BAD: no JSON-LD structured data -->`. 리치 결과(rich results) 표시 불가. |
| SEO-08 | Medium   | 서술적 URL 구조          | ✅ | 링크 href 값이 서술적 경로 사용 (`/about`, `/deals`). 불필요한 쿼리 파라미터 없음. |
| SEO-09 | High     | DOCTYPE html 선언        | ✅ | 1행에 `<!DOCTYPE html>` 정상 선언. |
| SEO-10 | High     | charset UTF-8 최상단     | ✅ | `<head>` 내 첫 번째 요소로 `<meta charset="UTF-8" />` 선언 (4행). |
| SEO-11 | High     | viewport meta 태그       | ✅ | `<meta name="viewport" content="width=device-width, initial-scale=1.0" />` 정상 설정 (5행). |

### Page Experience / Web Performance (18항목)

| 코드  | 영역   | 항목                               | 결과 | 발견된 문제 |
| ----- | ------ | ---------------------------------- | ---- | ----------- |
| WP-01 | CRP    | render-blocking script 없음        | ❌ | 37-44행: `<script>` 태그에 `defer`, `async`, `type="module"` 없이 인라인 스크립트 사용. body 끝에 위치하여 영향은 제한적이나, 외부 스크립트로 분리 후 `defer` 적용 권장. |
| WP-02 | CRP    | LCP fetchpriority + preload        | ❌ | hero.png(27행)이 LCP 후보이나 `fetchpriority="high"` 미설정, `<link rel="preload" as="image">` 미설정. |
| WP-03 | CRP    | Critical CSS 처리                  | ❌ | 10행: `<link rel="stylesheet" href="https://cdn.example.com/styles.css" />` — `media` 속성 없이 렌더 블로킹 외부 CSS. Critical CSS 인라인 후 나머지는 비동기 로드 권장. |
| WP-04 | 이미지 | img width/height 또는 aspect-ratio | ❌ | 33행: `<img src="/public/promo.png" alt="Promotional banner" />` — `width`/`height` 및 `aspect-ratio` 모두 누락. CLS 유발 위험. |
| WP-05 | 이미지 | loading="lazy"                     | ❌ | 30행 logo.png, 33행 promo.png — LCP가 아닌 이미지에 `loading="lazy"` 미적용. below-fold 이미지는 지연 로딩 필요. |
| WP-06 | 이미지 | WebP/AVIF 포맷                     | ❌ | 모든 이미지가 `.png` 포맷 사용 (hero.png, logo.png, promo.png). `<picture>` 요소 없음. WebP/AVIF 현대 포맷 미사용. |
| WP-07 | JS     | 코드 스플리팅                      | ➖ | 정적 HTML 페이지로 동적 `import()` 해당 없음. |
| WP-08 | JS     | 트리 쉐이킹 패턴                   | ➖ | 외부 라이브러리 import 없음. 해당 없음. |
| WP-09 | JS     | 레이아웃 스래싱 없음               | ✅ | 인라인 스크립트에서 레이아웃 속성 읽기/쓰기 혼합 루프 없음. |
| WP-10 | 폰트   | font-display 최적화                | ❌ | 13-17행: `@font-face`에서 `font-display` 속성 누락. 16행 주석에도 명시: `/* missing: font-display: swap */`. FOIT(보이지 않는 텍스트) 발생 위험. |
| WP-11 | 폰트   | 중요 폰트 preload                  | ❌ | `/fonts/custom.woff2` 폰트에 대한 `<link rel="preload" as="font">` 미설정. |
| WP-12 | LCP    | LCP 요소 초기 HTML 존재            | ✅ | hero.png 이미지가 초기 HTML에 직접 포함됨 (JS 의존 렌더링 아님). |
| WP-13 | INP    | 이벤트 핸들러 즉각 피드백          | ➖ | 이벤트 핸들러 바인딩 없음. 해당 없음. |
| WP-14 | INP    | 무거운 연산 지연 처리              | ➖ | 무거운 동기 연산 없음. 해당 없음. |
| WP-15 | INP    | React memo 활용                    | ➖ | React 미사용. 해당 없음. |
| WP-16 | CLS    | 뷰포트 위 동적 삽입 금지           | ✅ | `prepend()`, `insertBefore()` 사용 없음. `innerHTML` 사용은 있으나 기존 요소 내용 교체로 레이아웃 시프트 위험 낮음. |
| WP-17 | CLS    | 애니메이션 transform/opacity       | ➖ | CSS transition/animation 미사용. 해당 없음. |
| WP-18 | CLS    | 동적 콘텐츠 공간 예약              | ➖ | `<iframe>`, `<video>`, 광고 슬롯 없음. 해당 없음. |

### 수정 가이드

#### SEO-02: title 태그 개선 (Critical)

**파일:** `index.html`, 6행
**현재:** `<title>Sample Page</title>` (11자)
**문제:** 제목이 너무 짧고 일반적. 검색 키워드 미포함.

```html
<!-- 수정 전 -->
<title>Sample Page</title>

<!-- 수정 후 (예시) -->
<title>Premium Widgets for Sale | Free Shipping | Example Store</title>
```

- 50-60자로 작성
- 주요 키워드를 앞쪽에 배치
- 페이지마다 고유한 제목 사용

---

#### SEO-05: meta description 추가 (High)

**파일:** `index.html`, `<head>` 내 (6행 이후)
**현재:** 완전히 누락

```html
<!-- 추가 -->
<meta name="description" content="Shop premium widgets with free shipping. Browse our latest deals and promotions. Rated 4.9/5 by thousands of satisfied customers. Order today!">
```

- 150-160자로 작성
- 주요 키워드 자연스럽게 포함
- 행동 유도 문구(CTA) 포함
- 페이지마다 고유한 설명 작성

---

#### SEO-06: canonical URL 추가 (High)

**파일:** `index.html`, `<head>` 내
**현재:** 완전히 누락

```html
<!-- 추가 -->
<link rel="canonical" href="https://example.com/">
```

- 중복 콘텐츠 이슈 방지
- 절대 URL 사용 (프로토콜 포함)
- 자기 참조(self-referencing) canonical 권장

---

#### SEO-07: 구조화 데이터 (JSON-LD) 추가 (High)

**파일:** `index.html`, `<head>` 내 또는 `</body>` 직전
**현재:** 완전히 누락

홈페이지이므로 Organization 스키마 적용 권장:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Example Store",
  "url": "https://example.com",
  "logo": "https://example.com/public/logo.png",
  "sameAs": [
    "https://twitter.com/example",
    "https://linkedin.com/company/example"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+1-555-123-4567",
    "contactType": "customer service"
  }
}
</script>
```

- [Google Rich Results Test](https://search.google.com/test/rich-results)로 검증
- 페이지 유형에 맞는 스키마 타입 선택 (WebSite, Organization, Product 등)

---

#### WP-01: 인라인 스크립트 개선

**파일:** `index.html`, 37-44행
**문제:** 인라인 `<script>` 블록이 `defer`/`async` 없이 사용됨.

```html
<!-- 수정 전 -->
<script>
  var label = document.getElementById("label");
  ...
</script>

<!-- 수정 후: 외부 파일로 분리 + defer -->
<script defer src="/js/main.js"></script>
```

---

#### WP-02: LCP 이미지 최적화

**파일:** `index.html`, 27행

```html
<!-- 수정 전 -->
<img src="/public/hero.png" alt="Hero banner" width="800" height="400" />

<!-- 수정 후 -->
<img src="/public/hero.webp" alt="Hero banner" width="800" height="400" fetchpriority="high" />

<!-- head 내 추가 -->
<link rel="preload" href="/public/hero.webp" as="image" fetchpriority="high">
```

---

#### WP-03: Critical CSS 인라인 + 비동기 로드

**파일:** `index.html`, 10행

```html
<!-- 수정 전 -->
<link rel="stylesheet" href="https://cdn.example.com/styles.css" />

<!-- 수정 후 -->
<style>/* above-fold critical CSS 인라인 */</style>
<link rel="preload" href="https://cdn.example.com/styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="https://cdn.example.com/styles.css"></noscript>
```

---

#### WP-04: 이미지 크기 지정 (CLS 방지)

**파일:** `index.html`, 33행

```html
<!-- 수정 전 -->
<img src="/public/promo.png" alt="Promotional banner" />

<!-- 수정 후 -->
<img src="/public/promo.png" alt="Promotional banner" width="600" height="300" loading="lazy" />
```

---

#### WP-05: 비LCP 이미지에 lazy loading 적용

**파일:** `index.html`, 30행, 33행

```html
<!-- logo.png -->
<img src="/public/logo.png" width="120" height="40" alt="Site logo" loading="lazy" />

<!-- promo.png -->
<img src="/public/promo.png" alt="Promotional banner" width="600" height="300" loading="lazy" />
```

---

#### WP-06: 현대 이미지 포맷 사용

모든 `.png` 이미지를 WebP/AVIF로 변환하고 `<picture>` 요소 사용:

```html
<picture>
  <source type="image/avif" srcset="/public/hero.avif">
  <source type="image/webp" srcset="/public/hero.webp">
  <img src="/public/hero.png" alt="Hero banner" width="800" height="400" fetchpriority="high">
</picture>
```

---

#### WP-10: font-display 추가

**파일:** `index.html`, 13-17행

```css
/* 수정 전 */
@font-face {
  font-family: "CustomFont";
  src: url("/fonts/custom.woff2") format("woff2");
}

/* 수정 후 */
@font-face {
  font-family: "CustomFont";
  src: url("/fonts/custom.woff2") format("woff2");
  font-display: swap;
}
```

---

#### WP-11: 폰트 preload 추가

**파일:** `index.html`, `<head>` 내

```html
<link rel="preload" href="/fonts/custom.woff2" as="font" type="font/woff2" crossorigin>
```
