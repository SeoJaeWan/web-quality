## SEO & Web Performance 검토 결과 — 2026-03-10

검토 파일:
- `features/web-sample/pages/index.html`
- `features/web-sample/pages/dashboard.tsx`
- `features/web-sample/components/Card.tsx`

### Technical SEO (11항목)

| 코드   | 우선순위 | 항목                     | 결과 | 발견된 문제 |
| ------ | -------- | ------------------------ | ---- | ----------- |
| SEO-01 | Critical | noindex 없음             | ✅ | `index.html`에 `noindex` 메타 태그 없음. 정상적으로 인덱싱 가능 |
| SEO-02 | Critical | title 태그 존재하고 고유 | ❌ | `index.html` 2행: `<title>Sample Page</title>` — 12자로 50-60자 권장 범위에 미달. 키워드 없이 지나치게 일반적인 제목. `dashboard.tsx`, `Card.tsx`는 컴포넌트이므로 title 설정 불가 (페이지 셸에서 설정 필요) |
| SEO-03 | Critical | h1 하나                  | ✅ | `index.html`: `<h1>` 1개 (21행). `dashboard.tsx`: `<h1>` 1개 (25행). 각 페이지별 정확히 1개 |
| SEO-04 | Critical | HTTPS 사용               | ✅ | 모든 외부 리소스 URL이 `https://` 사용 (`index.html` 10행 CDN CSS, 24행/35행 링크). 이미지는 상대 경로 사용 |
| SEO-05 | High     | meta description         | ❌ | `index.html`: `<meta name="description">` 태그 없음 (7행 주석으로 인지하고 있으나 미구현) |
| SEO-06 | High     | canonical URL            | ❌ | `index.html`: `<link rel="canonical">` 태그 없음. 중복 콘텐츠 문제 발생 가능 |
| SEO-07 | High     | 구조화 데이터 (JSON-LD)  | ❌ | `index.html`: `<script type="application/ld+json">` 없음 (8행 주석으로 인지하고 있으나 미구현) |
| SEO-08 | Medium   | 서술적 URL 구조          | ✅ | 링크 href가 서술적 경로 사용: `/about`, `/deals`. 쿼리 파라미터 없음 |
| SEO-09 | High     | DOCTYPE html 선언        | ✅ | `index.html` 1행: `<!DOCTYPE html>` 정상 선언 |
| SEO-10 | High     | charset UTF-8 최상단     | ✅ | `index.html` 4행: `<meta charset="UTF-8">` — `<head>` 내 첫 번째 요소로 올바르게 배치 |
| SEO-11 | High     | viewport meta 태그       | ✅ | `index.html` 5행: `<meta name="viewport" content="width=device-width, initial-scale=1.0">` 정상 |

### Page Experience / Web Performance (18항목)

| 코드  | 영역   | 항목                               | 결과 | 발견된 문제 |
| ----- | ------ | ---------------------------------- | ---- | ----------- |
| WP-01 | CRP    | render-blocking script 없음        | ❌ | `index.html` 37-44행: `<script>` 태그에 `defer`/`async`/`type="module"` 없이 인라인 스크립트가 `<body>` 내에 동기적으로 실행됨. 파서 블로킹 발생 |
| WP-02 | CRP    | LCP fetchpriority + preload        | ❌ | `index.html` 27행: 히어로 이미지 `<img src="/public/hero.png">` 에 `fetchpriority="high"` 없음. `<link rel="preload" as="image">` 도 없음 |
| WP-03 | CRP    | Critical CSS 처리                  | ❌ | `index.html` 10행: `<link rel="stylesheet" href="https://cdn.example.com/styles.css">` — 렌더 블로킹 외부 CSS. `media` 속성이나 비동기 로딩 패턴 없음. Critical CSS 인라인 처리 필요 |
| WP-04 | 이미지 | img width/height 또는 aspect-ratio | ❌ | `index.html` 33행: `<img src="/public/promo.png" alt="Promotional banner">` — `width`/`height` 속성 없음, CLS 유발. `dashboard.tsx` 50행: `<img src="/public/promo.png">` — `width`/`height` 없음 |
| WP-05 | 이미지 | loading="lazy"                     | ❌ | `index.html` 33행: below-fold 이미지 `promo.png`에 `loading="lazy"` 없음. `dashboard.tsx` 50행: below-fold 이미지에 `loading="lazy"` 없음 |
| WP-06 | 이미지 | WebP/AVIF 포맷                     | ⚠️ | 모든 이미지가 `.png` 포맷 사용. `<picture>` 요소나 `.webp`/`.avif` 확장자 없음. WebP/AVIF로 전환하면 이미지 크기를 30-50% 절감 가능 |
| WP-07 | JS     | 코드 스플리팅                      | ⚠️ | `dashboard.tsx`, `Card.tsx`에 `import()` 동적 임포트 표현식 없음. 앱 규모가 커지면 route 기반 코드 스플리팅 권장 (예: `React.lazy(() => import('./Dashboard'))`) |
| WP-08 | JS     | 트리 쉐이킹 패턴                   | ✅ | 전체 라이브러리를 통째로 import하는 패턴 없음 (`import _ from 'lodash'` 등 미발견). React import만 사용 |
| WP-09 | JS     | 레이아웃 스래싱 없음               | ❌ | `dashboard.tsx` 11-13행: `useEffect` 내에서 `offsetHeight` 읽기 직후 `style.minHeight` 쓰기 — layout thrashing 발생. 읽기와 쓰기를 분리하거나 `ResizeObserver` 사용 필요 |
| WP-10 | 폰트   | font-display 최적화                | ❌ | `index.html` 13-17행: `@font-face` 선언에 `font-display` 속성 없음. FOIT(Flash of Invisible Text) 발생 가능. `font-display: swap` 또는 `optional` 추가 필요 |
| WP-11 | 폰트   | 중요 폰트 preload                  | ❌ | `index.html`: `<link rel="preload" as="font">` 없음. `/fonts/custom.woff2` 폰트를 preload하면 폰트 로딩 지연 감소 |
| WP-12 | LCP    | LCP 요소 초기 HTML 존재            | ⚠️ | `index.html`의 히어로 이미지는 초기 HTML에 존재하여 양호. 그러나 `dashboard.tsx` 17-19행: `setTimeout`으로 콘텐츠(`items`)를 500ms 지연 로딩 — LCP 요소가 JS 의존적일 수 있음 |
| WP-13 | INP    | 이벤트 핸들러 즉각 피드백          | ❌ | `Card.tsx` 11-20행: `handleClick`에서 `console.log` + DOM 조회 + 스타일 변경 수행하지만 즉각적인 시각 피드백(로딩 상태, 버튼 활성화 등) 없음. 사용자에게 인터랙션 응답이 보이지 않음 |
| WP-14 | INP    | 무거운 연산 지연 처리              | ➖ | 현재 코드에 무거운 동기 연산(대량 루프 등) 없음. 해당 없음 |
| WP-15 | INP    | React memo 활용                    | ⚠️ | `Card.tsx`: 리스트 내에서 반복 렌더링될 수 있는 컴포넌트이나 `React.memo()` 미적용. `Dashboard` 컴포넌트에서 `items` 상태 변경 시 모든 자식이 리렌더링됨. 규모가 커지면 성능 영향 가능 |
| WP-16 | CLS    | 뷰포트 위 동적 삽입 금지           | ✅ | `prepend()`, `insertBefore()` 등 뷰포트 상단에 동적 삽입하는 패턴 없음 |
| WP-17 | CLS    | 애니메이션 transform/opacity       | ➖ | CSS 애니메이션/트랜지션 선언 없음. 해당 없음 |
| WP-18 | CLS    | 동적 콘텐츠 공간 예약              | ❌ | `dashboard.tsx` 17-19행: `setTimeout`으로 `items` 배열을 동적으로 삽입하지만, 해당 영역에 `min-height` 등 공간 예약 없음. 콘텐츠 로딩 시 레이아웃 시프트 발생 |

### 수정 가이드

#### SEO-02: title 태그 최적화
**파일:** `index.html` 6행
```html
<!-- 현재 -->
<title>Sample Page</title>

<!-- 수정 -->
<title>Sample Page - Your Primary Keyword | Brand Name</title>
```
50-60자 범위 내에서 주요 키워드를 포함한 고유하고 서술적인 제목으로 변경하세요.

#### SEO-05: meta description 추가
**파일:** `index.html` — `<head>` 내에 추가
```html
<meta name="description" content="150-160자 범위의 페이지 내용을 요약하는 설명. 주요 키워드를 자연스럽게 포함하고 행동 유도 문구를 넣으세요.">
```

#### SEO-06: canonical URL 추가
**파일:** `index.html` — `<head>` 내에 추가
```html
<link rel="canonical" href="https://yourdomain.com/">
```

#### SEO-07: JSON-LD 구조화 데이터 추가
**파일:** `index.html` — `<head>` 또는 `<body>` 끝에 추가
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "Sample Page",
  "url": "https://yourdomain.com/"
}
</script>
```

#### WP-01: render-blocking 스크립트 제거
**파일:** `index.html` 37-44행
인라인 스크립트를 외부 파일로 분리하고 `defer` 속성 추가하거나, DOMContentLoaded 이벤트 내로 래핑하세요.
```html
<script defer src="/js/app.js"></script>
```
또는 `<body>` 하단에 위치시키되, `innerHTML` 사용은 XSS 위험이 있으므로 `textContent`로 변경을 강력 권장합니다.

#### WP-02: LCP 이미지 최적화
**파일:** `index.html` 27행 및 `<head>` 내
```html
<!-- head에 preload 추가 -->
<link rel="preload" href="/public/hero.png" as="image" fetchpriority="high">

<!-- img 태그에 fetchpriority 추가 -->
<img src="/public/hero.png" alt="Hero banner" width="800" height="400" fetchpriority="high">
```

#### WP-03: Critical CSS 비동기 로딩
**파일:** `index.html` 10행
```html
<!-- Critical CSS를 인라인으로 -->
<style>/* above-fold에 필요한 최소 CSS */</style>

<!-- 나머지 CSS는 비동기 로딩 -->
<link rel="preload" href="https://cdn.example.com/styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="https://cdn.example.com/styles.css"></noscript>
```

#### WP-04: 이미지 width/height 추가
**파일:** `index.html` 33행
```html
<img src="/public/promo.png" alt="Promotional banner" width="800" height="400">
```
**파일:** `dashboard.tsx` 50행
```html
<img src="/public/promo.png" alt="Promo" width="800" height="400" className="mt-8" />
```

#### WP-05: below-fold 이미지에 lazy loading 추가
**파일:** `index.html` 33행
```html
<img src="/public/promo.png" alt="Promotional banner" width="800" height="400" loading="lazy">
```
**파일:** `dashboard.tsx` 50행
```tsx
<img src="/public/promo.png" alt="Promo" width="800" height="400" loading="lazy" className="mt-8" />
```

#### WP-09: layout thrashing 수정
**파일:** `dashboard.tsx` 10-14행
```tsx
useEffect(() => {
  if (containerRef.current) {
    const h = containerRef.current.offsetHeight;
    // requestAnimationFrame으로 쓰기를 분리
    requestAnimationFrame(() => {
      if (containerRef.current) {
        containerRef.current.style.minHeight = h + "px";
      }
    });
  }
}, []);
```
또는 `ResizeObserver`를 사용하여 반응형으로 처리하세요.

#### WP-10: font-display 추가
**파일:** `index.html` 13-17행
```css
@font-face {
  font-family: "CustomFont";
  src: url("/fonts/custom.woff2") format("woff2");
  font-display: swap;
}
```

#### WP-11: 폰트 preload 추가
**파일:** `index.html` — `<head>` 내 상단에 추가
```html
<link rel="preload" href="/fonts/custom.woff2" as="font" type="font/woff2" crossorigin>
```

#### WP-13: 이벤트 핸들러에 즉각 시각 피드백 추가
**파일:** `Card.tsx` 11-20행
```tsx
const handleClick = () => {
  // 즉각적인 시각 피드백 제공
  const el = document.querySelector(".card-highlight");
  if (el) {
    (el as HTMLElement).style.background = "yellow";
  }
  // 비필수 작업은 지연 처리
  requestIdleCallback(() => {
    console.log("Card clicked:", title);
  });
};
```
더 나은 방법: `useState`로 클릭 상태를 관리하고 `useRef`로 DOM 접근하세요.

#### WP-18: 동적 콘텐츠 공간 예약
**파일:** `dashboard.tsx` 41행
```tsx
<section ref={containerRef} className="grid gap-4" style={{ minHeight: '200px' }}>
```
콘텐츠가 로딩되기 전에 최소 높이를 지정하여 레이아웃 시프트를 방지하세요.

### 요약

| 구분 | ✅ Pass | ❌ Fail | ⚠️ Advisory | ➖ N/A |
|------|---------|---------|-------------|--------|
| Technical SEO (11) | 7 | 4 | 0 | 0 |
| Web Performance (18) | 2 | 10 | 4 | 2 |
| **합계 (29)** | **9** | **14** | **4** | **2** |

주요 개선 영역:
1. **On-page SEO 메타데이터 부재** (SEO-02, 05, 06, 07) — title 최적화, description, canonical, JSON-LD 모두 추가 필요
2. **Critical Rendering Path 전반** (WP-01~03) — render-blocking 리소스 최적화 시급
3. **이미지 최적화** (WP-04~06) — 크기 속성, lazy loading, 현대 포맷 도입
4. **폰트 로딩** (WP-10~11) — font-display와 preload 적용
5. **CLS 방지** (WP-18) — 동적 콘텐츠 영역에 공간 예약
