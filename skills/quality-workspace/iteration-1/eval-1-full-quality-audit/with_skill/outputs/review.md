# 종합 웹 품질 검토 결과 — 2026-03-10

검토 파일:
- `features/web-sample/pages/index.html`
- `features/web-sample/pages/dashboard.tsx`
- `features/web-sample/components/Card.tsx`

---

## Section A: 접근성 (Accessibility) — KWCAG2.2 33항목 + 시맨틱 HTML

---

### 원칙 1. 인식의 용이성 (Perceivable) — 9항목

| 번호 | 항목명 | 결과 | 판정방식 | 발견된 문제 |
|------|--------|------|----------|------------|
| 1 | 적절한 대체 텍스트 제공 | ❌ | 정적분석 | `index.html:30` — `<img src="/public/logo.png">` alt 속성 누락. 의미 있는 이미지(로고)에 대체 텍스트가 없음 |
| 2 | 자막 제공 | ➖ | 정적분석 | `<video>`, `<audio>` 요소 없음 — 해당 없음 |
| 3 | 표의 구성 | ➖ | 정적분석 | `<table>` 요소 없음 — 해당 없음 |
| 4 | 콘텐츠의 선형 구조 | ✅ | 정적분석 | DOM 순서와 논리적 순서가 일치함 |
| 5 | 명확한 지시 사항 제공 | ➖ | 정적분석 | 지시 사항 텍스트 없음 — 해당 없음 |
| 6 | 색에 무관한 콘텐츠 인식 | 🔵 판정불가 | 판정불가 | 시각적 디자인 확인 필요 — 런타임 검증 불가 |
| 7 | 자동 재생 금지 | ✅ | 정적분석 | `autoplay` 속성 및 `.play()` 자동 호출 패턴 없음 |
| 8 | 텍스트 콘텐츠의 명도 대비 | 🔵 판정불가 | 판정불가 | playwright.config.ts 없음 — 런타임 색상 대비 측정 불가. 코드에 명시적 color/background-color 선언도 없어 정적 분석으로도 판정 불가 |
| 9 | 콘텐츠 간의 구분 | 🔵 판정불가 | 판정불가 | 시각적 디자인 확인 필요 — 런타임 검증 불가 |

### 원칙 2. 운용의 용이성 (Operable) — 15항목

| 번호 | 항목명 | 결과 | 판정방식 | 발견된 문제 |
|------|--------|------|----------|------------|
| 10 | 키보드 사용 보장 | ❌ | 정적분석 | `Card.tsx:29` — `<div onClick={handleClick}>` 비대화형 요소에 onClick만 있고 `onKeyDown`, `role="button"`, `tabIndex` 없음. 키보드로 조작 불가 |
| 11 | 초점 이동과 표시 | ✅ | 정적분석 | `outline: none` 또는 `tabIndex={-1}` 남용 패턴 없음 |
| 12 | 조작 가능 | ⚠️ | 정적분석 | `dashboard.tsx:29-35` — SVG 아이콘 버튼의 터치 영역 크기가 16x16으로 명시. 최소 권장 크기(44x44px) 미달 가능성 |
| 13 | 문자 단축키 | ➖ | 정적분석 | 키보드 이벤트 핸들러 없음 — 해당 없음 |
| 14 | 응답시간 조절 | ➖ | 정적분석 | 시간제한 콘텐츠 없음 — 해당 없음 |
| 15 | 정지 기능 제공 | ➖ | 정적분석 | 자동 변경 콘텐츠 없음 — 해당 없음 |
| 16 | 깜박임과 번쩍임 사용 제한 | ➖ | 정적분석 | 깜박임 콘텐츠 없음 — 해당 없음 |
| 17 | 반복 영역 건너뛰기 | ❌ | 정적분석 | `index.html` — 건너뛰기 링크(`href="#main"`, `href="#content"` 등) 없음. `<main>` 랜드마크도 없어 스킵 내비게이션 미제공 |
| 18 | 제목 제공 | ⚠️ | 정적분석 | `index.html:6` — `<title>Sample Page</title>` 제목이 지나치게 일반적. 페이지 내용을 구체적으로 설명하는 제목 권장. 헤딩 계층(h1→h2→h3)은 각 파일에서 적절히 사용됨 |
| 19 | 적절한 링크 텍스트 | ✅ | 정적분석 | "About Us", "latest deals" 등 링크 텍스트가 용도를 명확히 설명 |
| 20 | 고정된 참조 위치 정보 | ➖ | 정적분석 | 전자출판문서 아님 — 해당 없음 |
| 21 | 단일 포인터 입력 지원 | ➖ | 정적분석 | 다중 포인터/경로 기반 동작 없음 — 해당 없음 |
| 22 | 포인터 입력 취소 | ✅ | 정적분석 | `onMouseDown`/`onPointerDown` 즉시 실행 패턴 없음. `onClick` 사용 중 |
| 23 | 레이블과 네임 | ❌ | 정적분석 | `dashboard.tsx:29-35` — 2개의 SVG 아이콘 버튼에 `aria-label` 없음. 스크린 리더 사용자가 버튼 용도를 알 수 없음 |
| 24 | 동작 기반 작동 | ➖ | 정적분석 | DeviceMotion/Orientation 이벤트 없음 — 해당 없음 |

### 원칙 3. 이해의 용이성 (Understandable) — 7항목

| 번호 | 항목명 | 결과 | 판정방식 | 발견된 문제 |
|------|--------|------|----------|------------|
| 25 | 기본 언어 표시 | ⚠️ | 정적분석 | `index.html:2` — `<html lang="en">` 선언 있음. 단, 한국어 서비스인 경우 `lang="ko"`로 변경 필요. TSX 파일은 프레임워크의 루트 HTML에서 설정 필요 |
| 26 | 사용자 요구에 따른 실행 | ✅ | 정적분석 | `window.open()` 자동 실행, `<select onChange>` 자동 이동 패턴 없음 |
| 27 | 찾기 쉬운 도움 정보 | ➖ | 정적분석 | 도움 정보 없음 — 해당 없음 (단일 페이지 검토) |
| 28 | 오류 정정 | ➖ | 정적분석 | 폼 요소 없음 — 해당 없음 |
| 29 | 레이블 제공 | ➖ | 정적분석 | `<input>`, `<textarea>`, `<select>` 요소 없음 — 해당 없음 |
| 30 | 접근 가능한 인증 | ➖ | 정적분석 | 인증 관련 코드 없음 — 해당 없음 |
| 31 | 반복 입력 정보 | ➖ | 정적분석 | 다단계 폼 없음 — 해당 없음 |

### 원칙 4. 견고성 (Robust) — 2항목

| 번호 | 항목명 | 결과 | 판정방식 | 발견된 문제 |
|------|--------|------|----------|------------|
| 32 | 마크업 오류 방지 | ❌ | 정적분석 | (1) `Card.tsx:27` — `id="card-item"` 하드코딩. Card 컴포넌트가 리스트에서 반복 렌더링되면 동일 id 중복 → HTML 유효성 위반. (2) `dashboard.tsx:46` — `items.map()` 에서 `key` prop 누락 → React 경고 및 잠재적 렌더링 오류 |
| 33 | 웹 애플리케이션 접근성 준수 | ⚠️ | 정적분석 | `Card.tsx` — `<div onClick>` 커스텀 클릭 요소에 `role`, `aria-*` 상태 속성 없음. `dashboard.tsx` — 아이콘 버튼이 기본 `<button>` 요소이므로 role은 불필요하나, 상태(pressed/expanded 등) 관리 없음. 개선 권장 |

---

### 시맨틱 HTML 검토

| 검토 항목 | 결과 | 발견된 문제 |
|-----------|------|------------|
| 프레젠테이션 태그 (`<b>`, `<i>` 단독) | ✅ | 사용 없음 |
| 줄바꿈으로 문단 대체 (`<br><br>`) | ✅ | 사용 없음 |
| 인라인 요소의 블록 콘텐츠 감싸기 | ✅ | 위반 없음 |
| 랜드마크 누락 | ❌ | `index.html` — `<header>`, `<main>`, `<footer>`, `<nav>` 등 랜드마크 요소 전혀 없음. `<body>` 아래 콘텐츠가 모두 비구조적으로 배치됨 |
| 섹션 구조 | ✅ | `dashboard.tsx` — `<main>`, `<nav>`, `<section>` 등 시맨틱 요소 적절히 사용 |
| 보완적 콘텐츠 (`<aside>`) | ➖ | 사이드바/관련 링크 영역 없음 |
| 대화형 요소 | ⚠️ | `Card.tsx:24-33` — 클릭 가능한 `<div>` → `<button>` 또는 `<a>`로 대체 권장 |
| 리스트 구조 | ✅ | `dashboard.tsx:26` — `<ul>` + `<li>` 적절히 사용 |
| 폼 그룹화 | ➖ | 폼 요소 없음 |
| 인용문 | ➖ | 인용 텍스트 없음 |
| 시간/날짜 | ➖ | 날짜/시간 표시 없음 |

---

## Section B: SEO & Web Performance — Technical SEO 11항목 + Page Experience 18항목

---

### Technical SEO (11항목)

| 코드 | 우선순위 | 항목 | 결과 | 발견된 문제 |
|------|----------|------|------|------------|
| SEO-01 | Critical | noindex 없음 | ✅ | `noindex` 메타 태그 없음 — 정상 |
| SEO-02 | Critical | title 태그 존재하고 고유 (50-60자) | ⚠️ | `index.html:6` — `<title>Sample Page</title>` (11자). 존재하지만 50-60자 권장 길이에 미달. 키워드 포함 및 서술적 제목 필요 |
| SEO-03 | Critical | 페이지당 h1 하나 | ✅ | `index.html` — h1 1개, `dashboard.tsx` — h1 1개. 각 페이지/컴포넌트 적절 |
| SEO-04 | Critical | HTTPS 사용 | ✅ | 모든 외부 리소스 URL이 `https://` 사용 (`https://cdn.example.com/styles.css`, `https://example.com/about` 등) |
| SEO-05 | High | meta description 존재 (150-160자) | ❌ | `index.html` — `<meta name="description">` 없음. 검색 결과 스니펫에 적절한 설명이 표시되지 않음 |
| SEO-06 | High | canonical URL 설정 | ❌ | `index.html` — `<link rel="canonical">` 없음. 중복 콘텐츠 문제 발생 가능 |
| SEO-07 | High | 구조화 데이터 (JSON-LD) | ❌ | `index.html` — `<script type="application/ld+json">` 없음. 리치 검색 결과 미지원 |
| SEO-08 | Medium | 서술적 URL 구조 | ✅ | href 속성의 URL이 서술적 경로 사용 (`/about`, `/deals`) |
| SEO-09 | High | DOCTYPE html 선언 | ✅ | `index.html:1` — `<!DOCTYPE html>` 정상 선언 |
| SEO-10 | High | charset UTF-8 head 최상단 | ✅ | `index.html:4` — `<meta charset="UTF-8">` head 내 첫 번째 요소로 위치 |
| SEO-11 | High | viewport meta 태그 | ✅ | `index.html:5` — `<meta name="viewport" content="width=device-width, initial-scale=1.0">` 정상 |

### Page Experience / Web Performance (18항목)

| 코드 | 영역 | 항목 | 결과 | 발견된 문제 |
|------|------|------|------|------------|
| WP-01 | CRP | render-blocking script 없음 | ❌ | `index.html:37-44` — `<script>` 태그에 `defer`/`async`/`type="module"` 없이 인라인 스크립트가 `<body>` 끝에 위치. 인라인이므로 심각도는 낮으나, `innerHTML` 사용이 파싱을 차단할 수 있음 |
| WP-02 | CRP | LCP fetchpriority + preload | ❌ | `index.html:27` — hero 이미지(`/public/hero.png`)에 `fetchpriority="high"` 없음. `<link rel="preload" as="image">` 도 없음. LCP 지연 원인 |
| WP-03 | CRP | Critical CSS 처리 | ❌ | `index.html:10` — `<link rel="stylesheet" href="https://cdn.example.com/styles.css">` 동기 로딩으로 렌더링 차단. `media` 속성이나 비동기 로딩 기법 미적용 |
| WP-04 | 이미지 | img width/height 또는 aspect-ratio | ❌ | (1) `index.html:33` — `<img src="/public/promo.png">` width/height 누락 → CLS 유발. (2) `dashboard.tsx:50` — `<img src="/public/promo.png">` width/height 누락 → CLS 유발 |
| WP-05 | 이미지 | loading="lazy" | ❌ | `dashboard.tsx:50` — below-fold 이미지(`/public/promo.png`)에 `loading="lazy"` 없음. 불필요한 초기 로딩 발생 |
| WP-06 | 이미지 | WebP/AVIF 포맷 | ⚠️ | 모든 이미지가 `.png` 포맷. `<picture>` 요소 미사용. WebP/AVIF 현대 포맷 전환 권장 |
| WP-07 | JS | 코드 스플리팅 | ➖ | 동적 `import()` 필요성이 있는 대규모 모듈 구조 아님. 현재 규모에서는 해당 없음 |
| WP-08 | JS | 트리 쉐이킹 패턴 | ✅ | `import _ from 'lodash'` 등 전체 라이브러리 임포트 없음. React에서 named import 사용 |
| WP-09 | JS | 레이아웃 스래싱 없음 | ❌ | `dashboard.tsx:12-13` — `offsetHeight` 읽기 직후 `style.minHeight` 쓰기 → 레이아웃 스래싱 (강제 리플로우 2회 발생). 읽기/쓰기를 분리해야 함 |
| WP-10 | 폰트 | font-display 최적화 | ❌ | `index.html:13-17` — `@font-face`에 `font-display` 속성 누락. 폰트 로딩 중 텍스트 비표시(FOIT) 발생 가능 |
| WP-11 | 폰트 | 중요 폰트 preload | ❌ | `index.html` — `/fonts/custom.woff2` 폰트 파일에 대한 `<link rel="preload" as="font">` 없음. 폰트 발견 지연 |
| WP-12 | LCP | LCP 요소 초기 HTML 존재 | ✅ | hero 이미지가 초기 HTML에 `<img>` 태그로 존재. JS 의존적 로딩 아님 |
| WP-13 | INP | 이벤트 핸들러 즉각 피드백 | ⚠️ | `Card.tsx:11-20` — `handleClick`에서 DOM 조작(`querySelector` + style 변경) 수행하나 즉각적 시각 피드백(loading 상태 등) 없음 |
| WP-14 | INP | 무거운 연산 지연 처리 | ✅ | 동기 무거운 연산 루프 없음 |
| WP-15 | INP | React memo 활용 | ⚠️ | `Card.tsx` — 리스트에서 반복 렌더링되는 컴포넌트이나 `React.memo` 미적용. 부모 리렌더링 시 불필요한 재렌더링 발생 가능 |
| WP-16 | CLS | 뷰포트 위 동적 삽입 금지 | ✅ | `prepend()`, `insertBefore()` 등 뷰포트 위 동적 삽입 패턴 없음 |
| WP-17 | CLS | 애니메이션 transform/opacity만 | ✅ | 레이아웃 속성(`height`, `width`, `top`, `left` 등) 애니메이션 없음 |
| WP-18 | CLS | 동적 콘텐츠 공간 예약 | ❌ | `dashboard.tsx:17-18` — `setTimeout`으로 500ms 후 동적 콘텐츠 삽입(`setItems`). 공간 예약(`min-height` 등) 없이 콘텐츠가 추가되어 CLS 유발 |

---

## 종합 요약

### 영역별 결과 집계

| 영역 | 총 항목 | ✅ Pass | ❌ Fail | ⚠️ Advisory | ➖ N/A | 🔵 판정불가 |
|------|---------|---------|---------|-------------|--------|-------------|
| 접근성 (KWCAG2.2 33항목) | 33 | 7 | 5 | 4 | 14 | 3 |
| 시맨틱 HTML | 11 | 5 | 1 | 1 | 4 | 0 |
| Technical SEO (11항목) | 11 | 7 | 3 | 1 | 0 | 0 |
| Web Performance (18항목) | 18 | 5 | 8 | 3 | 2 | 0 |
| **합계** | **73** | **24** | **17** | **9** | **20** | **3** |

---

## 수정 가이드 (❌ 항목)

### A-1. 적절한 대체 텍스트 제공 (KWCAG Item 1)

**파일:** `index.html:30`
**문제:** `<img src="/public/logo.png" width="120" height="40" />` — alt 속성 누락

**수정:**
```html
<img src="/public/logo.png" alt="사이트 로고" width="120" height="40" />
```

---

### A-10. 키보드 사용 보장 (KWCAG Item 10)

**파일:** `Card.tsx:24-33`
**문제:** `<div onClick={handleClick}>` — 비대화형 요소에 마우스 이벤트만 존재

**수정 (방법 1 — 시맨틱 요소 사용):**
```tsx
<button
  className={`rounded border p-4 ${className}`}
  onClick={handleClick}
>
```

**수정 (방법 2 — ARIA 보완):**
```tsx
<div
  role="button"
  tabIndex={0}
  className={`rounded border p-4 ${className}`}
  onClick={handleClick}
  onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') handleClick(); }}
>
```

---

### A-17. 반복 영역 건너뛰기 (KWCAG Item 17)

**파일:** `index.html`
**문제:** 건너뛰기 링크 및 `<main>` 랜드마크 없음

**수정:**
```html
<body>
  <a href="#main-content" class="skip-nav">본문 바로가기</a>
  <!-- nav, header 등 -->
  <main id="main-content">
    <h1>Welcome to the Sample Page</h1>
    <!-- 본문 콘텐츠 -->
  </main>
</body>
```
```css
.skip-nav {
  position: absolute;
  top: -40px;
  left: 0;
  z-index: 100;
}
.skip-nav:focus {
  top: 0;
}
```

---

### A-23. 레이블과 네임 (KWCAG Item 23)

**파일:** `dashboard.tsx:29-35`
**문제:** SVG 아이콘 버튼 2개에 `aria-label` 없음

**수정:**
```tsx
<button aria-label="설정">
  <svg width="16" height="16" viewBox="0 0 16 16"><circle cx="8" cy="8" r="8" /></svg>
</button>

<button aria-label="메뉴">
  <svg width="16" height="16" viewBox="0 0 16 16"><rect width="16" height="16" /></svg>
</button>
```

---

### A-32. 마크업 오류 방지 (KWCAG Item 32)

**파일:** `Card.tsx:27`, `dashboard.tsx:46`

**문제 1 — 중복 id:**
```tsx
// 수정 전
id="card-item"

// 수정 후: props로 고유 id 전달하거나 id 속성 제거
id={`card-${title.toLowerCase().replace(/\s+/g, '-')}`}
```

**문제 2 — key 누락:**
```tsx
// 수정 전
{items.map((item) => (
  <div className="border p-2">{item}</div>
))}

// 수정 후
{items.map((item) => (
  <div key={item} className="border p-2">{item}</div>
))}
```

---

### 시맨틱 HTML — 랜드마크 누락

**파일:** `index.html`
**문제:** `<body>` 아래에 `<header>`, `<main>`, `<footer>` 등 랜드마크 요소 없음

**수정:**
```html
<body>
  <header>
    <h1>Welcome to the Sample Page</h1>
    <nav>
      <a href="https://example.com/about">About Us</a>
    </nav>
  </header>
  <main>
    <img src="/public/hero.png" alt="Hero banner" width="800" height="400" />
    <!-- 본문 콘텐츠 -->
  </main>
</body>
```

---

### SEO-05. meta description 누락

**파일:** `index.html`
**문제:** `<meta name="description">` 태그 없음

**수정:**
```html
<meta name="description" content="Sample Page에서 제공하는 서비스를 확인하세요. 최신 딜과 다양한 정보를 만나보실 수 있습니다.">
```

---

### SEO-06. canonical URL 누락

**파일:** `index.html`
**문제:** `<link rel="canonical">` 없음

**수정:**
```html
<link rel="canonical" href="https://example.com/">
```

---

### SEO-07. 구조화 데이터 (JSON-LD) 누락

**파일:** `index.html`
**문제:** 구조화 데이터 없음

**수정:**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "Sample Page",
  "url": "https://example.com/",
  "description": "Sample Page 서비스 소개"
}
</script>
```

---

### WP-01. render-blocking script

**파일:** `index.html:37-44`
**문제:** 인라인 스크립트에서 `innerHTML` 사용 (XSS 위험 + 파서 차단)

**수정:**
```html
<script defer>
  var label = document.getElementById("label");
  var userInput = location.hash.slice(1);
  if (label) {
    label.textContent = "Hello, " + userInput;  // innerHTML 대신 textContent 사용
  }
</script>
```

---

### WP-02. LCP fetchpriority + preload 누락

**파일:** `index.html:27`
**문제:** hero 이미지에 LCP 최적화 미적용

**수정:**
```html
<!-- head 내에 추가 -->
<link rel="preload" href="/public/hero.png" as="image" fetchpriority="high">

<!-- img 태그 수정 -->
<img src="/public/hero.png" alt="Hero banner" width="800" height="400" fetchpriority="high" loading="eager">
```

---

### WP-03. Critical CSS 처리

**파일:** `index.html:10`
**문제:** 외부 CSS 동기 로딩으로 렌더링 차단

**수정:**
```html
<!-- Critical CSS 인라인 -->
<style>/* above-fold 핵심 스타일 */</style>

<!-- 나머지 CSS 비동기 로딩 -->
<link rel="preload" href="https://cdn.example.com/styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="https://cdn.example.com/styles.css"></noscript>
```

---

### WP-04. img width/height 누락 (CLS)

**파일:** `index.html:33`, `dashboard.tsx:50`
**문제:** 이미지에 width/height 속성 없음 → CLS 유발

**수정:**
```html
<!-- index.html -->
<img src="/public/promo.png" alt="Promotional banner" width="800" height="300" />

<!-- dashboard.tsx -->
<img src="/public/promo.png" alt="Promo" className="mt-8" width="800" height="300" loading="lazy" />
```

---

### WP-05. loading="lazy" 누락

**파일:** `dashboard.tsx:50`
**문제:** below-fold 이미지에 lazy loading 미적용

**수정:**
```tsx
<img src="/public/promo.png" alt="Promo" className="mt-8" loading="lazy" width="800" height="300" />
```

---

### WP-09. 레이아웃 스래싱

**파일:** `dashboard.tsx:12-13`
**문제:** `offsetHeight` 읽기 → `style.minHeight` 쓰기 연속 실행으로 강제 리플로우

**수정:**
```tsx
useEffect(() => {
  if (containerRef.current) {
    // 읽기와 쓰기를 분리
    const h = containerRef.current.offsetHeight;
    requestAnimationFrame(() => {
      if (containerRef.current) {
        containerRef.current.style.minHeight = h + "px";
      }
    });
  }
}, []);
```

---

### WP-10. font-display 누락

**파일:** `index.html:13-17`
**문제:** `@font-face`에 `font-display` 선언 없음 → FOIT 발생

**수정:**
```css
@font-face {
  font-family: "CustomFont";
  src: url("/fonts/custom.woff2") format("woff2");
  font-display: swap;
}
```

---

### WP-11. 중요 폰트 preload 누락

**파일:** `index.html`
**문제:** 커스텀 폰트에 대한 preload 없음

**수정:**
```html
<link rel="preload" href="/fonts/custom.woff2" as="font" type="font/woff2" crossorigin>
```

---

### WP-18. 동적 콘텐츠 공간 예약 없음

**파일:** `dashboard.tsx:17-18`
**문제:** `setTimeout` 후 동적으로 아이템 삽입. 공간 예약 없어 CLS 유발

**수정:**
```tsx
<section ref={containerRef} className="grid gap-4" style={{ minHeight: '200px' }}>
  <h2 className="text-lg font-semibold">Overview</h2>
  {items.map((item) => (
    <div key={item} className="border p-2">{item}</div>
  ))}
  <img src="/public/promo.png" alt="Promo" className="mt-8" loading="lazy" width="800" height="300" />
</section>
```

---

## 추가 보안 관련 소견 (참고)

| 파일 | 위치 | 문제 |
|------|------|------|
| `index.html` | :42 | `innerHTML` + `location.hash` 사용 → **DOM-based XSS 취약점**. `textContent` 또는 DOMPurify 사용 권장 |
| `Card.tsx` | :12 | `console.log` 프로덕션 코드에 잔존. 빌드 시 제거 필요 |
| `Card.tsx` | :17 | `document.querySelector` 전역 DOM 쿼리 → React ref 패턴으로 대체 권장 |
