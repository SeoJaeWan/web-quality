# 종합 웹 품질 검토 결과

**검토일:** 2026-03-10
**검토 대상:** `features/web-sample/pages/dashboard.tsx`
**검토 영역:** 접근성 (KWCAG2.2 33항목 + 시맨틱 HTML) / SEO & 웹 성능 (29항목)
**중점 요청:** 접근성 및 성능 이슈 상세 검토

---

## 요약

| 영역 | 총 항목 | ✅ Pass | ❌ Fail | ⚠️ Advisory | ➖ N/A | 🔵 판정불가 |
|------|---------|---------|---------|-------------|--------|-------------|
| 접근성 (KWCAG2.2) | 33 | 17 | 3 | 2 | 11 | 0 |
| 시맨틱 HTML | 7 | 5 | 0 | 2 | 0 | 0 |
| Technical SEO | 11 | 1 | 0 | 0 | 10 | 0 |
| Web Performance | 18 | 6 | 5 | 3 | 4 | 0 |

---

# Section A: 접근성 (Accessibility)

## KWCAG2.2 33항목 검토

### 원칙 1. 인식의 용이성 (Perceivable)

| 번호 | 항목명 | 결과 | 판정방식 | 발견된 문제 |
|------|--------|------|----------|-------------|
| 1 | 적절한 대체 텍스트 | ✅ | 정적분석 | `<img src="/public/promo.png" alt="Promo">` — alt 속성 존재. 다만 "Promo"가 이미지 내용을 충분히 설명하는지 맥락에 따라 검토 필요 |
| 2 | 자막 제공 | ➖ | 정적분석 | `<video>`, `<audio>` 요소 없음 |
| 3 | 표의 구성 | ➖ | 정적분석 | `<table>` 요소 없음 |
| 4 | 콘텐츠의 선형 구조 | ✅ | 정적분석 | DOM 순서가 논리적: `<nav>` → `<section>`, 시각적 순서와 일치 |
| 5 | 명확한 지시 사항 | ➖ | 정적분석 | 지시 사항에 해당하는 텍스트 없음 |
| 6 | 색에 무관한 콘텐츠 인식 | ➖ | 정적분석 | 색상만으로 정보를 구분하는 패턴 없음 |
| 7 | 자동 재생 금지 | ✅ | 정적분석 | `autoplay` 속성이나 `.play()` 자동 호출 없음 |
| 8 | 텍스트 콘텐츠의 명도 대비 | 🔵 판정불가 | 판정불가 | Tailwind CSS 유틸리티 클래스 사용 — 실제 색상값은 런타임에 결정되므로 정적 분석으로 대비율 계산 불가. Playwright 환경 없음 |
| 9 | 콘텐츠 간의 구분 | ➖ | 정적분석 | 시각적 디자인 검증 필요 (코드상 `border`, `gap`, `p-2` 등 사용으로 구분 시도는 확인) |

### 원칙 2. 운용의 용이성 (Operable)

| 번호 | 항목명 | 결과 | 판정방식 | 발견된 문제 |
|------|--------|------|----------|-------------|
| 10 | 키보드 사용 보장 | ✅ | 정적분석 | `<button>` 요소 사용으로 키보드 접근 가능. 비대화형 요소에 onClick 없음 |
| 11 | 초점 이동과 표시 | ✅ | 정적분석 | `outline: none` 패턴 없음, 초점 트랩 없음. Tailwind 기본 포커스 스타일 유지 |
| 12 | 조작 가능 | ⚠️ | 정적분석 | SVG 아이콘 버튼(29-31행, 33-36행)에 명시적 크기 지정이 `width="16" height="16"`으로 16px. 버튼 자체에 padding이 명시되지 않아 터치 타겟이 최소 기준(44px) 미달 가능성 |
| 13 | 문자 단축키 | ➖ | 정적분석 | 키보드 이벤트 핸들러 없음 |
| 14 | 응답시간 조절 | ✅ | 정적분석 | `setTimeout` 사용하나 세션 타임아웃이 아닌 데이터 로딩 시뮬레이션 용도 |
| 15 | 정지 기능 제공 | ➖ | 정적분석 | 자동 변경 콘텐츠 없음 |
| 16 | 깜박임과 번쩍임 | ➖ | 정적분석 | 깜박임 애니메이션 없음 |
| 17 | 반복 영역 건너뛰기 | ⚠️ | 정적분석 | Skip navigation 링크 없음. 단일 페이지 컴포넌트이므로 레이아웃 단에서 제공될 수 있으나, 이 파일 단독으로는 확인 불가. 레이아웃에서 제공하지 않는다면 추가 필요 |
| 18 | 제목 제공 | ✅ | 정적분석 | `<h1>Dashboard</h1>` → `<h2>Overview</h2>` 계층 구조 올바름 |
| 19 | 적절한 링크 텍스트 | ➖ | 정적분석 | `<a>` 요소 없음 |
| 20 | 고정된 참조 위치 정보 | ➖ | 정적분석 | 전자출판문서 아님 |
| 21 | 단일 포인터 입력 지원 | ➖ | 정적분석 | 다중 포인터/경로 기반 동작 없음 |
| 22 | 포인터 입력 취소 | ✅ | 정적분석 | `onMouseDown`/`onPointerDown` 직접 실행 패턴 없음 |
| 23 | 레이블과 네임 | ❌ | 정적분석 | **[상세 아래]** 아이콘 버튼에 접근 가능한 이름 없음 |
| 24 | 동작 기반 작동 | ➖ | 정적분석 | `DeviceMotionEvent`/`DeviceOrientationEvent` 없음 |

### 원칙 3. 이해의 용이성 (Understandable)

| 번호 | 항목명 | 결과 | 판정방식 | 발견된 문제 |
|------|--------|------|----------|-------------|
| 25 | 기본 언어 표시 | ✅ | 정적분석 | 컴포넌트 파일이므로 `<html lang>` 은 상위 문서에서 설정. 컴포넌트 내에서 lang 관련 이슈 없음 |
| 26 | 사용자 요구에 따른 실행 | ✅ | 정적분석 | 자동 새 창, `window.open()`, `<select onChange>` 자동 이동 없음 |
| 27 | 찾기 쉬운 도움 정보 | ➖ | 정적분석 | 도움 정보 관련 요소 없음 (해당 없음) |
| 28 | 오류 정정 | ✅ | 정적분석 | 폼 입력 요소 없음 |
| 29 | 레이블 제공 | ✅ | 정적분석 | `<input>`, `<textarea>`, `<select>` 요소 없음 |
| 30 | 접근 가능한 인증 | ✅ | 정적분석 | 인증 과정 없음 |
| 31 | 반복 입력 정보 | ✅ | 정적분석 | 다단계 폼 없음 |

### 원칙 4. 견고성 (Robust)

| 번호 | 항목명 | 결과 | 판정방식 | 발견된 문제 |
|------|--------|------|----------|-------------|
| 32 | 마크업 오류 방지 | ❌ | 정적분석 | **[상세 아래]** 리스트 렌더링에 `key` prop 누락 |
| 33 | 웹 애플리케이션 접근성 | ❌ | 정적분석 | **[상세 아래]** 아이콘 전용 버튼에 ARIA 속성 없음 |

---

### 시맨틱 HTML 검토 (7항목)

| 항목 | 결과 | 평가 |
|------|------|------|
| 프레젠테이셔널 태그 사용 | ✅ | `<b>`, `<i>` 단독 사용 없음 |
| 줄바꿈으로 문단 구성 | ✅ | 연속 `<br>` 없음 |
| 인라인 요소가 블록 감싸기 | ✅ | `<span>`이 블록 콘텐츠 감싸는 패턴 없음 |
| 랜드마크 요소 | ✅ | `<main>`, `<nav>`, `<section>` 올바르게 사용 |
| 섹션 구조 | ✅ | `<section>` 사용으로 적절한 구조 |
| 인터랙티브 요소 | ⚠️ | 아이콘 버튼은 `<button>` 사용하여 적절하나, 접근 가능한 이름(aria-label) 부재 |
| 리스트 구조 | ⚠️ | 동적 아이템(items.map)이 `<div>` 로 렌더링됨. 반복 항목이므로 `<ul>` + `<li>` 구조가 더 적합 |

---

### 접근성 ❌ 항목 상세 및 수정 가이드

#### ❌ Item 23. 레이블과 네임 — 아이콘 버튼에 접근 가능한 이름 없음

**위치:** `dashboard.tsx:29-31`, `dashboard.tsx:33-36`

**문제:** 두 개의 `<button>` 내부에 SVG 아이콘만 존재하고, `aria-label`이나 텍스트가 없어 스크린 리더 사용자가 버튼의 용도를 알 수 없음.

```tsx
// ❌ 현재 코드
<button>
  <svg width="16" height="16" viewBox="0 0 16 16"><circle cx="8" cy="8" r="8" /></svg>
</button>

// ✅ 수정 방법
<button aria-label="알림">
  <svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="8" /></svg>
</button>
```

**영향도:** 높음. 스크린 리더 사용자에게 버튼이 "버튼"으로만 읽히며, 실제 기능을 전혀 파악할 수 없음.

---

#### ❌ Item 32. 마크업 오류 방지 — key prop 누락

**위치:** `dashboard.tsx:45-47`

**문제:** `items.map()` 리스트 렌더링에서 `key` prop이 없음. React에서 key 누락은 리스트 업데이트 시 비효율적 재렌더링과 상태 버그를 유발할 수 있음.

```tsx
// ❌ 현재 코드
{items.map((item) => (
  <div className="border p-2">{item}</div>
))}

// ✅ 수정 방법 — 고유한 key 제공
{items.map((item) => (
  <div key={item} className="border p-2">{item}</div>
))}
```

**영향도:** 중간. 현재 정적 데이터라 큰 문제는 없으나, 동적 데이터에서는 렌더링 버그로 이어질 수 있음.

---

#### ❌ Item 33. 웹 애플리케이션 접근성 — 아이콘 버튼 ARIA 부재

**위치:** `dashboard.tsx:29-36`

**문제:** 커스텀 아이콘 버튼에 `aria-label`이 없어 보조 기술이 버튼의 역할을 전달할 수 없음. Item 23과 관련되나, 이 항목은 WAI-ARIA 상태/속성 제공 측면에서 평가.

```tsx
// ✅ 수정 방법
<button aria-label="설정">
  <svg aria-hidden="true" ...>...</svg>
</button>
```

---

# Section B: SEO & 웹 성능 (SEO & Web Performance)

## Technical SEO (11항목)

> 참고: dashboard.tsx는 React 컴포넌트 파일로, HTML 문서 수준의 `<head>`, `<title>`, `<meta>` 등은 포함하지 않음.
> 이들 항목은 Next.js/Vite 등 프레임워크 레이아웃이나 index.html에서 관리되므로 컴포넌트 단독으로는 해당 없음(N/A)으로 판정.

| 코드 | 우선순위 | 항목 | 결과 | 발견된 문제 |
|------|----------|------|------|-------------|
| SEO-01 | Critical | noindex 없음 | ➖ | 컴포넌트 파일 — meta 태그 없음 (상위 문서에서 관리) |
| SEO-02 | Critical | title 태그 존재하고 고유 | ➖ | 컴포넌트 파일 — title 없음 (상위 문서에서 관리) |
| SEO-03 | Critical | h1 하나 | ✅ | `<h1>Dashboard</h1>` 하나만 존재. 올바름 |
| SEO-04 | Critical | HTTPS 사용 | ➖ | 외부 리소스 URL이 상대경로(`/public/promo.png`)로 프로토콜 미지정 |
| SEO-05 | High | meta description | ➖ | 컴포넌트 파일 — 해당 없음 |
| SEO-06 | High | canonical URL | ➖ | 컴포넌트 파일 — 해당 없음 |
| SEO-07 | High | 구조화 데이터 (JSON-LD) | ➖ | 컴포넌트 파일 — 해당 없음 |
| SEO-08 | Medium | 서술적 URL 구조 | ➖ | URL 구조는 라우터 설정에 의존 |
| SEO-09 | High | DOCTYPE html 선언 | ➖ | 컴포넌트 파일 — 해당 없음 |
| SEO-10 | High | charset UTF-8 최상단 | ➖ | 컴포넌트 파일 — 해당 없음 |
| SEO-11 | High | viewport meta 태그 | ➖ | 컴포넌트 파일 — 해당 없음 |

---

## Page Experience / Web Performance (18항목)

| 코드 | 영역 | 항목 | 결과 | 발견된 문제 |
|------|------|------|------|-------------|
| WP-01 | CRP | render-blocking script 없음 | ➖ | `<script>` 태그 직접 사용 없음 (번들러가 관리) |
| WP-02 | CRP | LCP fetchpriority + preload | ⚠️ | `<img src="/public/promo.png">` — LCP 후보일 경우 `fetchpriority="high"` 및 preload 없음. below-fold 이미지이므로 현재 큰 문제 아님 |
| WP-03 | CRP | Critical CSS 처리 | ➖ | Tailwind 유틸리티 사용, 별도 stylesheet 링크 없음 |
| WP-04 | 이미지 | img width/height 또는 aspect-ratio | ❌ | **[상세 아래]** `<img>` 에 width/height 속성 및 aspect-ratio 없음 |
| WP-05 | 이미지 | loading="lazy" | ❌ | **[상세 아래]** below-fold 이미지에 `loading="lazy"` 없음 |
| WP-06 | 이미지 | WebP/AVIF 포맷 | ⚠️ | `.png` 포맷 사용. WebP/AVIF 변환 및 `<picture>` 요소 사용 권장 |
| WP-07 | JS | 코드 스플리팅 | ⚠️ | 이 파일에 `dynamic import()` 없음. 규모에 따라 코드 스플리팅 고려 필요 |
| WP-08 | JS | 트리 쉐이킹 패턴 | ✅ | 전체 라이브러리를 통째로 임포트하는 패턴 없음. `React`에서 필요한 훅만 named import |
| WP-09 | JS | 레이아웃 스래싱 없음 | ❌ | **[상세 아래]** useEffect 내에서 레이아웃 읽기/쓰기 혼합 |
| WP-10 | 폰트 | font-display 최적화 | ➖ | `@font-face` 선언 없음 (Tailwind/시스템 폰트 사용 추정) |
| WP-11 | 폰트 | 중요 폰트 preload | ➖ | 커스텀 폰트 사용 없음 |
| WP-12 | LCP | LCP 요소 초기 HTML 존재 | ✅ | `<h1>Dashboard</h1>` 은 초기 HTML에 존재. 이미지는 below-fold이므로 LCP 후보가 아닐 가능성 높음 |
| WP-13 | INP | 이벤트 핸들러 즉각 피드백 | ✅ | 버튼에 복잡한 이벤트 핸들러 없음 |
| WP-14 | INP | 무거운 연산 지연 처리 | ✅ | 무거운 동기 연산 없음 |
| WP-15 | INP | React memo 활용 | ✅ | 현재 컴포넌트가 단순하여 memo 필요성 낮음 |
| WP-16 | CLS | 뷰포트 위 동적 삽입 금지 | ✅ | `prepend`, `insertBefore` 사용 없음 |
| WP-17 | CLS | 애니메이션 transform/opacity | ➖ | CSS 애니메이션/트랜지션 없음 |
| WP-18 | CLS | 동적 콘텐츠 공간 예약 | ❌ | **[상세 아래]** setTimeout으로 동적 콘텐츠 삽입 시 공간 미예약 |

---

### 웹 성능 ❌ 항목 상세 및 수정 가이드

#### ❌ WP-04. img width/height 미지정 (CLS 위험)

**위치:** `dashboard.tsx:50`

**문제:** `<img src="/public/promo.png" alt="Promo" className="mt-8" />` 에 `width`, `height` 속성이 없음. 이미지 로딩 시 브라우저가 공간을 예약하지 못해 레이아웃 시프트(CLS)가 발생함.

```tsx
// ❌ 현재 코드
<img src="/public/promo.png" alt="Promo" className="mt-8" />

// ✅ 수정 방법 1: width/height 명시
<img src="/public/promo.png" alt="Promo" width={800} height={400} className="mt-8" />

// ✅ 수정 방법 2: aspect-ratio CSS 사용
<img src="/public/promo.png" alt="Promo" className="mt-8" style={{ aspectRatio: '2/1', width: '100%' }} />
```

**CLS 영향:** 높음. 이미지 크기를 모르는 상태에서 로드되면 하단 콘텐츠가 밀려남.

---

#### ❌ WP-05. below-fold 이미지에 loading="lazy" 없음

**위치:** `dashboard.tsx:50`

**문제:** `className="mt-8"` 로 배치된 이미지는 below-fold일 가능성이 높으나, `loading="lazy"` 가 없어 페이지 초기 로딩 시 불필요한 이미지까지 즉시 다운로드됨.

```tsx
// ❌ 현재 코드
<img src="/public/promo.png" alt="Promo" className="mt-8" />

// ✅ 수정 방법
<img
  src="/public/promo.png"
  alt="Promo"
  loading="lazy"
  decoding="async"
  width={800}
  height={400}
  className="mt-8"
/>
```

**LCP 영향:** 초기 페이지 로드에 불필요한 네트워크 대역폭을 소비하여 실제 LCP 요소의 로딩을 지연시킬 수 있음.

---

#### ❌ WP-09. 레이아웃 스래싱 (Layout Thrashing)

**위치:** `dashboard.tsx:11-13`

**문제:** `useEffect` 내에서 `offsetHeight` (레이아웃 읽기) 직후 `style.minHeight` (레이아웃 쓰기)를 수행함. 이는 브라우저에게 강제 리플로우(forced reflow)를 유발하고, 연속 호출 시 레이아웃 스래싱으로 이어져 렌더링 성능을 크게 저하시킴.

```tsx
// ❌ 현재 코드
useEffect(() => {
  if (containerRef.current) {
    const h = containerRef.current.offsetHeight; // 강제 리플로우
    containerRef.current.style.minHeight = h + "px"; // 또 다른 리플로우 트리거
  }
}, []);

// ✅ 수정 방법 1: requestAnimationFrame으로 쓰기 분리
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

// ✅ 수정 방법 2: CSS로 해결 (min-height를 CSS에서 직접 지정)
// <section className="grid gap-4 min-h-[200px]">
```

**INP/렌더링 영향:** 중간~높음. 현재 단일 요소라 영향이 제한적이나, 이 패턴이 반복되면 심각한 성능 저하로 이어짐.

---

#### ❌ WP-18. 동적 콘텐츠 공간 미예약 (CLS 위험)

**위치:** `dashboard.tsx:17-19`

**문제:** `setTimeout(() => setItems([...]), 500)` 으로 500ms 후 콘텐츠가 동적으로 삽입됨. 초기 렌더링 시 items가 빈 배열이므로 공간이 0이고, 500ms 후 3개의 `<div>` 가 삽입되면서 레이아웃 시프트 발생.

```tsx
// ❌ 현재 코드
const [items, setItems] = useState<string[]>([]);
// ...
setTimeout(() => {
  setItems(["Dashboard", "Analytics", "Reports"]);
}, 500);

// ✅ 수정 방법 1: 컨테이너에 최소 높이 예약
<section ref={containerRef} className="grid gap-4" style={{ minHeight: '200px' }}>

// ✅ 수정 방법 2: 스켈레톤/플레이스홀더 UI 제공
{items.length === 0 ? (
  <div className="border p-2 animate-pulse bg-gray-200 h-10" />
  <div className="border p-2 animate-pulse bg-gray-200 h-10" />
  <div className="border p-2 animate-pulse bg-gray-200 h-10" />
) : (
  items.map((item) => <div key={item} className="border p-2">{item}</div>)
)}

// ✅ 수정 방법 3: 초기값 제공 (가능한 경우)
const [items, setItems] = useState(["Dashboard", "Analytics", "Reports"]);
```

**CLS 영향:** 높음. 500ms 지연 후 콘텐츠 삽입은 사용자가 이미 페이지를 보고 있는 시점에 레이아웃이 변경되어 CLS 점수에 직접적으로 악영향.

---

## 종합 소견

### 접근성 주요 이슈 (중점 요청 항목)

1. **아이콘 버튼 접근성 (Item 23, 33):** 가장 시급한 접근성 이슈. SVG 아이콘만 포함된 2개의 버튼에 `aria-label`이 없어 스크린 리더 사용자가 버튼 기능을 전혀 파악할 수 없음. 즉시 수정 필요.

2. **key prop 누락 (Item 32):** React 리스트 렌더링 기본 규칙 위반. 현재 단순 데이터이나 향후 동적 데이터에서 문제 발생 가능.

3. **터치 타겟 크기 (Item 12):** 아이콘 버튼의 SVG가 16x16px로 모바일 터치 타겟 최소 기준(44x44px)에 미달할 수 있음.

### 성능 주요 이슈 (중점 요청 항목)

1. **CLS 이중 위험:** 두 가지 CLS 원인이 동시에 존재함.
   - 이미지 `width`/`height` 미지정 (WP-04)
   - 동적 콘텐츠 500ms 지연 삽입 시 공간 미예약 (WP-18)
   이 두 요소가 합산되면 CLS 0.1 기준을 쉽게 초과할 수 있음.

2. **레이아웃 스래싱 (WP-09):** `offsetHeight` 읽기 후 즉시 `style.minHeight` 쓰기 패턴은 강제 리플로우를 유발. 현재 단일 요소라 영향은 제한적이나, 안티패턴으로서 즉시 수정 권장.

3. **이미지 최적화 미흡 (WP-05, WP-06):** `loading="lazy"` 누락으로 초기 로드 시 불필요한 리소스 다운로드. PNG 포맷 사용으로 WebP/AVIF 대비 파일 크기 비효율.

### 우선순위별 수정 권장

| 우선순위 | 항목 | 예상 효과 |
|----------|------|-----------|
| 🔴 긴급 | 아이콘 버튼에 `aria-label` 추가 (Item 23, 33) | 스크린 리더 접근성 확보 |
| 🔴 긴급 | `<img>` 에 `width`/`height` + `loading="lazy"` 추가 (WP-04, WP-05) | CLS 개선 + 초기 로드 최적화 |
| 🟠 높음 | 동적 콘텐츠에 공간 예약 또는 스켈레톤 UI (WP-18) | CLS 0.1 이하 달성 |
| 🟠 높음 | 레이아웃 스래싱 수정 — rAF 분리 또는 CSS 대체 (WP-09) | 렌더링 성능 개선 |
| 🟡 중간 | `key` prop 추가 (Item 32) | React 렌더링 정확성 확보 |
| 🟡 중간 | 이미지 WebP/AVIF 포맷 전환 (WP-06) | 파일 크기 30-50% 절감 |
| 🔵 낮음 | 아이콘 버튼 터치 타겟 크기 확대 (Item 12) | 모바일 사용성 개선 |
| 🔵 낮음 | 동적 아이템을 `<ul>` + `<li>` 구조로 변경 | 시맨틱 HTML 개선 |
