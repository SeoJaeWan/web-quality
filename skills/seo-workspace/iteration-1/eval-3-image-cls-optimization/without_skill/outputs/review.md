# Image Optimization & Rendering Performance Review

**Target files:**
- `features/web-sample/pages/dashboard.tsx`
- `features/web-sample/components/Card.tsx`

---

## 1. CLS (Cumulative Layout Shift) Issues

### 1-1. Image without explicit width/height (Critical)

**File:** `dashboard.tsx` line 50

```tsx
<img src="/public/promo.png" alt="Promo" className="mt-8" />
```

**Problem:**
- `width`와 `height` 속성이 지정되지 않아 브라우저가 이미지를 다운로드하기 전까지 공간을 예약할 수 없다. 이미지가 로드되는 순간 레이아웃이 밀리면서 CLS가 발생한다.

**Fix:**
```tsx
<img
  src="/public/promo.png"
  alt="Promo"
  width={800}
  height={400}
  className="mt-8 w-full h-auto"
/>
```
- 명시적 `width`/`height`를 설정하면 브라우저가 aspect ratio를 미리 계산하여 공간을 확보한다.
- CSS로 `w-full h-auto`를 적용하면 반응형 크기 조절이 가능하면서도 레이아웃 안정성을 유지할 수 있다.

### 1-2. Dynamic content insertion without size reservation (Critical)

**File:** `dashboard.tsx` lines 16-19

```tsx
setTimeout(() => {
  setItems(["Dashboard", "Analytics", "Reports"]);
}, 500);
```

**Problem:**
- 500ms 지연 후 콘텐츠가 삽입되면서 이미지와 그 아래 요소들이 밀려난다. 이는 CLS의 대표적인 원인이다.
- 초기 렌더링 시 `items`가 빈 배열이므로 해당 영역의 높이가 0이다가, 콘텐츠가 추가되면서 레이아웃이 변경된다.

**Fix:**
- `min-height`를 CSS로 미리 지정하거나, skeleton/placeholder UI를 사용하여 콘텐츠 영역의 크기를 예약한다.
- 가능하다면 SSR 또는 초기 상태에서 데이터를 즉시 로드하여 지연 삽입을 피한다.

```tsx
<section ref={containerRef} className="grid gap-4" style={{ minHeight: '200px' }}>
  {items.length === 0 && <SkeletonPlaceholder />}
  {items.map((item) => (
    <div key={item} className="border p-2">{item}</div>
  ))}
</section>
```

---

## 2. Image Loading Optimization Issues

### 2-1. Below-the-fold image without lazy loading (High)

**File:** `dashboard.tsx` line 50

```tsx
<img src="/public/promo.png" alt="Promo" className="mt-8" />
```

**Problem:**
- `className="mt-8"`과 페이지 구조상 이 이미지는 fold 아래에 위치할 가능성이 높다. 그러나 `loading="lazy"`가 없으므로 페이지 초기 로드 시 즉시 다운로드를 시작한다.
- 사용자가 보지 않는 이미지를 미리 로드하면 초기 로딩 시간(LCP)이 늘어나고 대역폭이 낭비된다.

**Fix:**
```tsx
<img
  src="/public/promo.png"
  alt="Promo"
  loading="lazy"
  decoding="async"
  width={800}
  height={400}
  className="mt-8 w-full h-auto"
/>
```
- `loading="lazy"`: 뷰포트에 가까워질 때만 로드한다.
- `decoding="async"`: 이미지 디코딩이 메인 스레드를 차단하지 않도록 한다.

### 2-2. No modern image format usage (Medium)

**File:** `dashboard.tsx` line 50

**Problem:**
- `.png` 형식만 사용하고 있다. WebP나 AVIF 같은 차세대 포맷을 사용하면 동일 품질 대비 파일 크기를 30-50% 줄일 수 있다.

**Fix:**
- `<picture>` 요소를 사용하여 포맷 폴백을 제공한다.

```tsx
<picture>
  <source srcSet="/public/promo.avif" type="image/avif" />
  <source srcSet="/public/promo.webp" type="image/webp" />
  <img
    src="/public/promo.png"
    alt="Promo"
    loading="lazy"
    decoding="async"
    width={800}
    height={400}
    className="mt-8 w-full h-auto"
  />
</picture>
```

### 2-3. No responsive image srcSet (Medium)

**Problem:**
- 단일 이미지 소스만 제공하고 있어 모바일 디바이스에서도 데스크톱 크기의 이미지를 다운로드한다.

**Fix:**
```tsx
<img
  src="/public/promo.png"
  srcSet="/public/promo-480.png 480w, /public/promo-800.png 800w, /public/promo-1200.png 1200w"
  sizes="(max-width: 600px) 480px, (max-width: 1024px) 800px, 1200px"
  alt="Promo"
  loading="lazy"
  decoding="async"
  width={800}
  height={400}
  className="mt-8 w-full h-auto"
/>
```

### 2-4. Next.js Image component not used (Medium)

**Problem:**
- 이 프로젝트가 Next.js 기반이라면 `next/image`의 `<Image>` 컴포넌트를 사용하는 것이 권장된다. 자동으로 lazy loading, 반응형 크기 조절, WebP 변환, width/height 기반 aspect ratio 예약 등을 처리해준다.

**Fix:**
```tsx
import Image from "next/image";

<Image
  src="/public/promo.png"
  alt="Promo"
  width={800}
  height={400}
  className="mt-8"
  placeholder="blur"
  blurDataURL="data:image/png;base64,..."
/>
```

---

## 3. Rendering Performance Issues

### 3-1. Layout thrashing in useEffect (High)

**File:** `dashboard.tsx` lines 10-13

```tsx
const h = containerRef.current.offsetHeight; // forces reflow
containerRef.current.style.minHeight = h + "px"; // triggers another reflow
```

**Problem:**
- `offsetHeight` 읽기(layout read)와 `style.minHeight` 쓰기(layout write)를 연속적으로 수행하면 forced synchronous layout(강제 동기 리플로우)이 발생한다.
- 이 패턴이 루프 안에서 반복되면 심각한 성능 저하를 초래한다.

**Fix:**
- `requestAnimationFrame`을 사용하여 읽기와 쓰기를 분리한다.
- 또는 CSS만으로 `min-height`를 처리할 수 있다면 JS를 제거한다.

```tsx
useEffect(() => {
  if (containerRef.current) {
    const el = containerRef.current;
    // batch read
    const h = el.offsetHeight;
    // defer write to next frame
    requestAnimationFrame(() => {
      el.style.minHeight = h + "px";
    });
  }
}, []);
```

### 3-2. Missing key prop on list items (Medium)

**File:** `dashboard.tsx` lines 45-47

```tsx
{items.map((item) => (
  <div className="border p-2">{item}</div>
))}
```

**Problem:**
- `key` prop이 없으면 React가 리스트 변경 시 효율적인 diffing을 수행할 수 없다. 불필요한 DOM 재생성이 발생하여 렌더링 성능이 저하된다.

**Fix:**
```tsx
{items.map((item) => (
  <div key={item} className="border p-2">{item}</div>
))}
```

### 3-3. Card component: DOM query instead of ref (Low)

**File:** `Card.tsx` lines 17-20

```tsx
const el = document.querySelector(".card-highlight");
if (el) {
  (el as HTMLElement).style.background = "yellow";
}
```

**Problem:**
- `document.querySelector`는 전체 DOM을 탐색하므로 성능 비효율적이다. 또한 Card가 여러 개 렌더링될 경우 의도하지 않은 첫 번째 `.card-highlight` 요소만 변경된다.

**Fix:**
- `useRef`를 사용하여 해당 요소에 직접 접근한다.

```tsx
const highlightRef = useRef<HTMLDivElement>(null);

const handleClick = () => {
  if (highlightRef.current) {
    highlightRef.current.style.background = "yellow";
  }
};

// JSX
<div ref={highlightRef} className="card-highlight">{children}</div>
```

---

## Summary

| # | Issue | Severity | Category |
|---|-------|----------|----------|
| 1-1 | Image without width/height (CLS) | Critical | CLS |
| 1-2 | Dynamic content without size reservation (CLS) | Critical | CLS |
| 2-1 | No lazy loading on below-fold image | High | Loading |
| 2-2 | No modern image format (WebP/AVIF) | Medium | Loading |
| 2-3 | No responsive srcSet | Medium | Loading |
| 2-4 | Native img instead of Next.js Image | Medium | Loading |
| 3-1 | Layout thrashing in useEffect | High | Rendering |
| 3-2 | Missing key prop on list items | Medium | Rendering |
| 3-3 | DOM query instead of ref in Card | Low | Rendering |
