# SEO Review Report

**Reviewed files:**
- `features/web-sample/pages/index.html`
- `features/web-sample/pages/dashboard.tsx`

---

## 1. index.html

### 1-1. Meta Description 누락 (Critical)
- **위치:** `<head>` 섹션
- **문제:** `<meta name="description" content="...">` 태그가 없음.
- **영향:** 검색 엔진 결과 페이지(SERP)에서 페이지 설명이 자동 생성되며, 클릭률(CTR)이 저하될 수 있음.
- **권장 조치:** 페이지 내용을 요약하는 150~160자 이내의 meta description을 추가할 것.

```html
<meta name="description" content="Sample Page - 주요 서비스와 최신 딜을 확인하세요." />
```

### 1-2. Title 태그 비구체적 (Major)
- **위치:** 6번째 줄 `<title>Sample Page</title>`
- **문제:** "Sample Page"는 페이지 내용을 설명하지 못하는 일반적인 제목임.
- **영향:** 검색 엔진이 페이지의 주제를 파악하기 어렵고, SERP에서 사용자 관심을 끌기 어려움.
- **권장 조치:** 핵심 키워드를 포함하는 구체적이고 고유한 제목으로 변경할 것 (50~60자 이내).

### 1-3. 구조화된 데이터(JSON-LD) 누락 (Major)
- **위치:** `<head>` 또는 `<body>` 내
- **문제:** Schema.org 기반의 JSON-LD 구조화 데이터가 없음.
- **영향:** 리치 스니펫(별점, FAQ, 브레드크럼 등) 표시 기회를 놓침. 검색 엔진이 페이지 콘텐츠의 의미를 정확히 이해하기 어려움.
- **권장 조치:** 페이지 유형에 맞는 JSON-LD 스크립트를 추가할 것 (예: WebPage, Organization 등).

### 1-4. 이미지 alt 속성 누락 (Major)
- **위치:** 30번째 줄 `<img src="/public/logo.png" width="120" height="40" />`
- **문제:** `alt` 속성이 없어 검색 엔진이 이미지 내용을 인식할 수 없음.
- **영향:** 이미지 검색 노출 기회 상실, 접근성 저하 (스크린 리더 사용 불가).
- **권장 조치:** 이미지의 내용을 설명하는 `alt` 속성을 추가할 것.

```html
<img src="/public/logo.png" alt="회사 로고" width="120" height="40" />
```

### 1-5. 이미지 width/height 누락 (Minor)
- **위치:** 33번째 줄 `<img src="/public/promo.png" alt="Promotional banner" />`
- **문제:** `width`와 `height` 속성이 없어 브라우저가 레이아웃 공간을 미리 확보하지 못함.
- **영향:** CLS(Cumulative Layout Shift) 증가로 Core Web Vitals 점수 하락, 간접적으로 SEO 순위에 부정적 영향.
- **권장 조치:** 이미지의 실제 크기에 맞는 `width`와 `height` 속성을 추가할 것.

### 1-6. Canonical URL 누락 (Major)
- **위치:** `<head>` 섹션
- **문제:** `<link rel="canonical" href="...">` 태그가 없음.
- **영향:** 중복 콘텐츠 문제 발생 가능. 동일 페이지가 여러 URL로 접근될 때 검색 엔진이 대표 URL을 판단하지 못함.
- **권장 조치:** 해당 페이지의 대표 URL을 canonical 태그로 지정할 것.

### 1-7. Open Graph / Twitter 메타 태그 누락 (Minor)
- **위치:** `<head>` 섹션
- **문제:** `og:title`, `og:description`, `og:image`, `twitter:card` 등의 소셜 미디어 메타 태그가 없음.
- **영향:** SNS 공유 시 미리보기가 제대로 표시되지 않아 소셜 트래픽 유입이 감소할 수 있음.
- **권장 조치:** Open Graph 및 Twitter Card 메타 태그를 추가할 것.

### 1-8. 렌더 블로킹 CSS (Minor - SEO 간접 영향)
- **위치:** 10번째 줄 `<link rel="stylesheet" href="https://cdn.example.com/styles.css" />`
- **문제:** 외부 CSS가 동기적으로 로드되어 렌더링을 차단함.
- **영향:** 페이지 로딩 속도 저하로 Core Web Vitals(LCP) 점수 하락, SEO 순위에 간접적 악영향.
- **권장 조치:** Critical CSS는 인라인으로, 나머지는 `media` 속성이나 비동기 로딩으로 처리할 것.

### 1-9. font-display: swap 미설정 (Minor - SEO 간접 영향)
- **위치:** 13~17번째 줄 `@font-face` 선언
- **문제:** `font-display: swap`이 설정되지 않아 폰트 로딩 중 텍스트가 보이지 않을 수 있음 (FOIT).
- **영향:** LCP 지연 및 사용자 경험 저하, Core Web Vitals 점수에 부정적 영향.
- **권장 조치:** `font-display: swap;`을 추가할 것.

### 1-10. robots.txt / sitemap 참조 없음 (Info)
- **문제:** 이 HTML 파일 자체의 문제는 아니나, 사이트 전체적으로 `robots.txt`와 `sitemap.xml`이 적절히 구성되어 있는지 확인이 필요함.

---

## 2. dashboard.tsx

### 2-1. 페이지 레벨 메타 태그 미설정 (Critical)
- **위치:** 컴포넌트 전체
- **문제:** React 컴포넌트에서 `<title>`, `<meta name="description">` 등 SEO 관련 head 태그를 설정하지 않음. `react-helmet`, `next/head` 등의 솔루션이 사용되지 않고 있음.
- **영향:** 검색 엔진이 페이지 제목과 설명을 인식하지 못함. SPA(Single Page Application)에서 특히 치명적.
- **권장 조치:** `react-helmet-async` 또는 프레임워크의 Head 관리 기능을 사용하여 페이지별 title, description을 설정할 것.

### 2-2. SSR/SSG 지원 여부 불명확 (Critical)
- **위치:** 컴포넌트 전체
- **문제:** 순수 클라이언트 사이드 렌더링(CSR)으로 보이며, 서버 사이드 렌더링(SSR) 또는 정적 사이트 생성(SSG) 여부가 불분명함. `useEffect`와 `setTimeout`으로 콘텐츠를 동적으로 주입하고 있음.
- **영향:** 검색 엔진 크롤러(특히 Googlebot 외)가 JavaScript 실행 없이는 콘텐츠를 인덱싱하지 못할 수 있음. 핵심 콘텐츠("Dashboard", "Analytics", "Reports")가 초기 HTML에 포함되지 않음.
- **권장 조치:** Next.js의 `getServerSideProps`/`getStaticProps` 또는 유사 SSR 프레임워크를 도입하여 중요 콘텐츠가 초기 HTML에 포함되도록 할 것.

### 2-3. 이미지 loading="lazy" 미사용 (Minor)
- **위치:** 50번째 줄 `<img src="/public/promo.png" alt="Promo" className="mt-8" />`
- **문제:** 페이지 하단(below-fold)의 이미지에 `loading="lazy"`가 설정되지 않음.
- **영향:** 불필요한 초기 로드로 인해 페이지 속도 저하, LCP에 간접적 영향.
- **권장 조치:** below-fold 이미지에 `loading="lazy"`를 추가할 것.

### 2-4. 이미지 width/height 미설정 (Minor)
- **위치:** 50번째 줄 `<img>` 태그
- **문제:** `width`와 `height` 속성이 없어 CLS 발생 가능.
- **영향:** Core Web Vitals의 CLS 점수 하락으로 SEO 순위에 간접적 악영향.
- **권장 조치:** 명시적인 `width`, `height` 속성 또는 CSS aspect-ratio를 사용할 것.

### 2-5. 동적 콘텐츠 삽입에 의한 CLS (Minor)
- **위치:** 17~18번째 줄 `setTimeout` 내 `setItems`
- **문제:** 500ms 지연 후 항목이 삽입되면서 레이아웃이 변경됨. 크기가 예약되지 않은 상태.
- **영향:** CLS 증가로 Core Web Vitals 점수 저하.
- **권장 조치:** 콘텐츠 영역에 최소 높이를 미리 확보하거나, SSR로 초기 데이터를 포함시킬 것.

### 2-6. 시맨틱 구조 (Positive)
- `<main>`, `<nav>`, `<section>` 등 시맨틱 HTML 태그를 적절히 사용하고 있음.
- 헤딩 계층 구조(`h1` -> `h2`)가 올바르게 설정됨.

---

## Summary Table

| # | File | Issue | Severity | Category |
|---|------|-------|----------|----------|
| 1 | index.html | Meta description 누락 | Critical | On-page SEO |
| 2 | index.html | Title 태그 비구체적 | Major | On-page SEO |
| 3 | index.html | JSON-LD 구조화 데이터 누락 | Major | Structured Data |
| 4 | index.html | 이미지 alt 속성 누락 | Major | Image SEO / Accessibility |
| 5 | index.html | 이미지 width/height 누락 | Minor | Core Web Vitals (CLS) |
| 6 | index.html | Canonical URL 누락 | Major | Technical SEO |
| 7 | index.html | Open Graph / Twitter 메타 태그 누락 | Minor | Social SEO |
| 8 | index.html | 렌더 블로킹 CSS | Minor | Core Web Vitals (LCP) |
| 9 | index.html | font-display: swap 미설정 | Minor | Core Web Vitals (LCP) |
| 10 | dashboard.tsx | 페이지 레벨 메타 태그 미설정 | Critical | On-page SEO |
| 11 | dashboard.tsx | SSR/SSG 미지원 (CSR only) | Critical | Crawlability |
| 12 | dashboard.tsx | 이미지 loading="lazy" 미사용 | Minor | Core Web Vitals |
| 13 | dashboard.tsx | 이미지 width/height 미설정 | Minor | Core Web Vitals (CLS) |
| 14 | dashboard.tsx | 동적 콘텐츠에 의한 CLS | Minor | Core Web Vitals (CLS) |

**Critical: 3 / Major: 4 / Minor: 7**
