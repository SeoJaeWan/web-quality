## SEO & Web Performance 검토 결과 — 2026-03-10

검토 파일: `features/web-sample/pages/dashboard.tsx`, `features/web-sample/components/Card.tsx`

### Technical SEO (11항목)

| 코드   | 우선순위 | 항목                     | 결과 | 발견된 문제 |
| ------ | -------- | ------------------------ | ---- | ----------- |
| SEO-01 | Critical | noindex 없음             | ➖   | 컴포넌트 파일로 `<meta>` 태그 확인 불가. 페이지 레이아웃/루트에서 설정 필요. |
| SEO-02 | Critical | title 태그 존재하고 고유 | ➖   | 컴포넌트 파일로 `<title>` 태그 미확인. 루트 레이아웃에서 설정 필요. |
| SEO-03 | Critical | h1 하나                  | ✅   | `dashboard.tsx` 라인 25에 `<h1>` 1개 존재. |
| SEO-04 | Critical | HTTPS 사용               | ⚠️   | `dashboard.tsx` 라인 50: `src="/public/promo.png"` — 상대 경로 사용. HTTPS 위반은 아니지만 `/public/` 접두사가 포함된 경로는 빌드 도구에 따라 문제 발생 가능. |
| SEO-05 | High     | meta description         | ➖   | 컴포넌트 파일로 확인 불가. |
| SEO-06 | High     | canonical URL            | ➖   | 컴포넌트 파일로 확인 불가. |
| SEO-07 | High     | 구조화 데이터 (JSON-LD)  | ➖   | 컴포넌트 파일로 확인 불가. |
| SEO-08 | Medium   | 서술적 URL 구조          | ➖   | URL 라우팅 설정이 대상 파일에 포함되지 않음. |
| SEO-09 | High     | DOCTYPE html 선언        | ➖   | 컴포넌트 파일로 확인 불가. |
| SEO-10 | High     | charset UTF-8 최상단     | ➖   | 컴포넌트 파일로 확인 불가. |
| SEO-11 | High     | viewport meta 태그       | ➖   | 컴포넌트 파일로 확인 불가. |

### Page Experience / Web Performance (18항목)

| 코드  | 영역   | 항목                               | 결과 | 발견된 문제 |
| ----- | ------ | ---------------------------------- | ---- | ----------- |
| WP-01 | CRP    | render-blocking script 없음        | ➖   | HTML 파일이 아닌 React 컴포넌트 파일이라 `<script src>` 태그 직접 확인 불가. |
| WP-02 | CRP    | LCP fetchpriority + preload        | ⚠️   | `dashboard.tsx` 라인 50: `<img src="/public/promo.png">` — 이 이미지가 LCP 후보일 경우 `fetchpriority="high"`와 preload 링크가 누락됨. 현재 hero 이미지나 LCP 대상 이미지에 대한 fetchpriority 설정 없음. |
| WP-03 | CRP    | Critical CSS 처리                  | ➖   | CSS 파일이 대상에 포함되지 않아 확인 불가. Tailwind 클래스 사용 중. |
| WP-04 | 이미지 | img width/height 또는 aspect-ratio | ❌   | **`dashboard.tsx` 라인 50**: `<img src="/public/promo.png" alt="Promo" className="mt-8" />` — `width`, `height` 속성 및 `aspect-ratio` CSS가 모두 없음. 이미지 로딩 시 레이아웃 이동(CLS) 발생. |
| WP-05 | 이미지 | loading="lazy"                     | ❌   | **`dashboard.tsx` 라인 50**: below-fold 이미지(`className="mt-8"` 사용, 하단 배치)에 `loading="lazy"` 미적용. 불필요한 초기 로딩으로 성능 저하. |
| WP-06 | 이미지 | WebP/AVIF 포맷                     | ❌   | **`dashboard.tsx` 라인 50**: `.png` 포맷 사용. `<picture>` 요소 없음. WebP/AVIF 등 현대 포맷 미사용으로 파일 크기 비효율. |
| WP-07 | JS     | 코드 스플리팅                      | ⚠️   | 두 파일 모두 `dynamic import()` 표현식 없음. 대시보드 페이지가 커질 경우 코드 스플리팅 도입 권장. |
| WP-08 | JS     | 트리 쉐이킹 패턴                   | ✅   | `lodash` 등 전체 라이브러리 임포트 패턴 없음. `React`만 named import로 사용 중. |
| WP-09 | JS     | 레이아웃 스래싱 없음               | ❌   | **`dashboard.tsx` 라인 11-13**: `useEffect` 내에서 `offsetHeight` 읽기(reflow 강제) 직후 `style.minHeight` 쓰기(추가 reflow 유발). 전형적 레이아웃 스래싱 패턴. |
| WP-10 | 폰트   | font-display 최적화                | ➖   | `@font-face` 선언이 대상 파일에 없음. Tailwind 기본 설정에 의존. |
| WP-11 | 폰트   | 중요 폰트 preload                  | ➖   | 폰트 preload 태그 확인 불가 (HTML head 영역이 대상 범위 밖). |
| WP-12 | LCP    | LCP 요소 초기 HTML 존재            | ❌   | **`dashboard.tsx` 라인 17-19**: `useEffect` + `setTimeout`으로 메인 콘텐츠 아이템(`items`)을 500ms 후 설정. LCP 요소가 JavaScript 실행에 의존하여 초기 HTML에 포함되지 않음. 서버 사이드 렌더링 또는 초기 데이터 주입 필요. |
| WP-13 | INP    | 이벤트 핸들러 즉각 피드백          | ⚠️   | **`Card.tsx` 라인 11-20**: `handleClick`에서 DOM 조작(`style.background = "yellow"`)을 수행하지만 버튼의 시각적 상태 변경(loading 표시 등)이 없음. 즉각적 시각 피드백 추가 권장. |
| WP-14 | INP    | 무거운 연산 지연 처리              | ✅   | 현재 파일에서 동기적 무거운 연산 루프 없음. |
| WP-15 | INP    | React memo 활용                    | ⚠️   | **`Card.tsx`**: 리스트에서 반복 렌더링될 수 있는 `Card` 컴포넌트에 `React.memo()` 미적용. 부모 리렌더링 시 불필요한 재렌더링 발생 가능. |
| WP-16 | CLS    | 뷰포트 위 동적 삽입 금지           | ❌   | **`dashboard.tsx` 라인 17-19**: `setTimeout`으로 `setItems`를 호출하여 뷰포트 상단의 `<section>` 내에 동적으로 3개 아이템 삽입. 공간 예약 없이 콘텐츠가 추가되면서 아래 요소들이 밀려남 → CLS 발생. |
| WP-17 | CLS    | 애니메이션 transform/opacity       | ✅   | CSS 애니메이션에서 `height`, `width`, `top`, `left`, `margin`, `padding` 전환 사용 없음. |
| WP-18 | CLS    | 동적 콘텐츠 공간 예약              | ❌   | **`dashboard.tsx` 라인 41-51**: `items`가 비어 있다가 500ms 후 채워지는데, `<section>` 영역에 `min-height` 등 공간 예약이 없음. 이미지(`promo.png`)도 dimension 없이 렌더링되어 공간 미예약. |

### 수정 가이드

#### WP-04 (❌) img width/height 누락 — CLS 방지

**파일**: `dashboard.tsx` 라인 50

```tsx
// Before
<img src="/public/promo.png" alt="Promo" className="mt-8" />

// After — width/height 명시 또는 aspect-ratio 사용
<img
  src="/public/promo.png"
  alt="Promo"
  width={800}
  height={400}
  className="mt-8"
/>
// 또는 CSS로:
<img
  src="/public/promo.png"
  alt="Promo"
  className="mt-8"
  style={{ aspectRatio: '2/1', width: '100%' }}
/>
```

#### WP-05 (❌) loading="lazy" 누락

**파일**: `dashboard.tsx` 라인 50

```tsx
// Before
<img src="/public/promo.png" alt="Promo" className="mt-8" />

// After — below-fold 이미지에 lazy loading 적용
<img
  src="/public/promo.png"
  alt="Promo"
  width={800}
  height={400}
  loading="lazy"
  decoding="async"
  className="mt-8"
/>
```

#### WP-06 (❌) 현대 이미지 포맷 미사용

**파일**: `dashboard.tsx` 라인 50

```tsx
// After — <picture> 요소로 WebP/AVIF 우선 제공
<picture>
  <source srcSet="/public/promo.avif" type="image/avif" />
  <source srcSet="/public/promo.webp" type="image/webp" />
  <img
    src="/public/promo.png"
    alt="Promo"
    width={800}
    height={400}
    loading="lazy"
    decoding="async"
    className="mt-8"
  />
</picture>
```

#### WP-09 (❌) 레이아웃 스래싱

**파일**: `dashboard.tsx` 라인 11-13

```tsx
// Before — 읽기/쓰기 혼합
useEffect(() => {
  if (containerRef.current) {
    const h = containerRef.current.offsetHeight;
    containerRef.current.style.minHeight = h + "px";
  }
}, []);

// After — requestAnimationFrame으로 읽기/쓰기 분리
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

또는 CSS `min-height`를 직접 지정하여 JavaScript 의존 제거 권장.

#### WP-12 (❌) LCP 요소가 JS에 의존

**파일**: `dashboard.tsx` 라인 17-19

```tsx
// Before — setTimeout으로 클라이언트에서 데이터 설정
useEffect(() => {
  setTimeout(() => {
    setItems(["Dashboard", "Analytics", "Reports"]);
  }, 500);
}, []);

// After — 초기값으로 데이터 제공 (SSR 또는 초기 상태)
const [items, setItems] = useState<string[]>(["Dashboard", "Analytics", "Reports"]);
```

실제 API 호출이 필요한 경우 `getServerSideProps`(Next.js) 또는 서버 컴포넌트를 사용하여 초기 HTML에 콘텐츠 포함.

#### WP-16 (❌) 뷰포트 위 동적 삽입으로 인한 CLS

**파일**: `dashboard.tsx` 라인 17-19, 41-47

위 WP-12 수정과 동일 — 초기 데이터를 서버에서 제공하거나 `useState` 초기값으로 설정하면 동적 삽입 자체가 사라져 CLS 방지.

만약 동적 로딩이 필수적인 경우:

```tsx
// 콘텐츠 영역에 min-height 예약
<section ref={containerRef} className="grid gap-4" style={{ minHeight: '200px' }}>
```

#### WP-18 (❌) 동적 콘텐츠 공간 미예약

**파일**: `dashboard.tsx` 라인 41-51

```tsx
// Before — 공간 예약 없이 동적 콘텐츠 + 이미지
<section ref={containerRef} className="grid gap-4">
  <h2>Overview</h2>
  {items.map((item) => <div className="border p-2">{item}</div>)}
  <img src="/public/promo.png" alt="Promo" className="mt-8" />
</section>

// After — 아이템 영역과 이미지 모두 공간 예약
<section ref={containerRef} className="grid gap-4" style={{ minHeight: '300px' }}>
  <h2>Overview</h2>
  {items.map((item, index) => (
    <div key={item} className="border p-2">{item}</div>
  ))}
  <img
    src="/public/promo.png"
    alt="Promo"
    width={800}
    height={400}
    loading="lazy"
    decoding="async"
    className="mt-8"
  />
</section>
```
