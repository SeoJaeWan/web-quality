# Dashboard.tsx 종합 품질 검토

**대상 파일:** `features/web-sample/pages/dashboard.tsx`

---

## 1. 접근성 (Accessibility) 이슈

### 1-1. 아이콘 버튼에 접근 가능한 이름 없음 (심각도: 높음)

**위치:** 29~31행, 34~36행

두 개의 `<button>` 요소가 SVG 아이콘만 포함하고 있으며, `aria-label`, `aria-labelledby`, 또는 시각적으로 숨겨진 텍스트(`visually-hidden` 텍스트)가 전혀 없다. 스크린 리더 사용자는 이 버튼의 용도를 알 수 없다.

**WCAG 위반:** 4.1.2 Name, Role, Value (Level A)

**수정 방법:**
```tsx
<button aria-label="알림">
  <svg ...><circle ... /></svg>
</button>
<button aria-label="설정">
  <svg ...><rect ... /></svg>
</button>
```

### 1-2. SVG에 `role` 및 접근성 속성 누락 (심각도: 중간)

**위치:** 30행, 35행

장식용 SVG라면 `aria-hidden="true"`를 추가하여 보조 기술이 무시하도록 해야 하고, 의미 있는 SVG라면 `role="img"`와 `<title>` 요소를 부여해야 한다. 현재 상태에서는 스크린 리더가 SVG 내부 구조를 불필요하게 탐색할 수 있다.

**수정 방법 (장식용 아이콘인 경우):**
```tsx
<svg aria-hidden="true" width="16" height="16" viewBox="0 0 16 16">
  <circle cx="8" cy="8" r="8" />
</svg>
```

### 1-3. 동적 콘텐츠 변경 시 라이브 리전 미적용 (심각도: 중간)

**위치:** 17~19행, 45~47행

`setTimeout`으로 500ms 후 아이템 목록이 동적으로 삽입되지만, 해당 영역에 `aria-live` 속성이 없다. 스크린 리더 사용자는 콘텐츠가 변경되었다는 사실을 인지할 수 없다.

**수정 방법:**
```tsx
<section ref={containerRef} className="grid gap-4" aria-live="polite">
```

### 1-4. `nav` 요소에 접근 가능한 레이블 없음 (심각도: 낮음)

**위치:** 24행

페이지에 여러 `<nav>` 요소가 있을 수 있으므로, `aria-label`로 네비게이션의 목적을 명시하는 것이 좋다.

**수정 방법:**
```tsx
<nav aria-label="대시보드 네비게이션" className="mb-4">
```

### 1-5. 리스트 아이템에 key 누락 — 포커스 관리 영향 (심각도: 중간)

**위치:** 45~47행

`items.map()`에서 렌더링되는 `<div>` 요소에 `key` prop이 없다. React의 재조정(reconciliation) 과정에서 DOM 노드가 불필요하게 재생성되면, 포커스가 유실될 수 있다. 이는 키보드 사용자와 보조 기술 사용자 모두에게 영향을 준다.

**수정 방법:**
```tsx
{items.map((item) => (
  <div key={item} className="border p-2">{item}</div>
))}
```

---

## 2. 성능 (Performance) 이슈

### 2-1. 강제 동기 레이아웃 (Layout Thrashing) (심각도: 높음)

**위치:** 12~13행

`offsetHeight`를 읽은 직후 `style.minHeight`를 쓰고 있다. 이 패턴은 브라우저가 레이아웃을 두 번 계산하도록 강제하며, 특히 DOM이 복잡한 페이지에서 렌더링 성능을 심각하게 저하시킨다.

**수정 방법:** `requestAnimationFrame`을 사용하거나, 읽기/쓰기를 분리한다.
```tsx
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

더 나은 접근: CSS만으로 `min-height`를 관리하여 JavaScript 레이아웃 조작 자체를 제거한다.

### 2-2. Cumulative Layout Shift (CLS) 유발 (심각도: 높음)

**위치:** 17~19행

`setTimeout`으로 500ms 후 아이템 3개가 삽입되면서 레이아웃이 밀린다. 초기 렌더링 시 콘텐츠 영역의 크기가 예약되어 있지 않아 CLS 점수에 부정적 영향을 준다.

**수정 방법:**
- 서버 사이드 렌더링(SSR) 또는 정적 생성(SSG)으로 초기 데이터를 포함하여 렌더링한다.
- 클라이언트 로딩이 불가피한 경우, 스켈레톤 UI로 공간을 미리 확보한다.

```tsx
<section ref={containerRef} className="grid gap-4" style={{ minHeight: '200px' }}>
  {items.length === 0 ? (
    <div className="animate-pulse space-y-2">
      <div className="h-8 bg-gray-200 rounded" />
      <div className="h-8 bg-gray-200 rounded" />
      <div className="h-8 bg-gray-200 rounded" />
    </div>
  ) : (
    items.map((item) => (
      <div key={item} className="border p-2">{item}</div>
    ))
  )}
</section>
```

### 2-3. 이미지에 `loading="lazy"` 누락 (심각도: 중간)

**위치:** 50행

`<img>` 태그에 `loading="lazy"` 속성이 없다. 스크롤 아래(below-the-fold)에 위치한 이미지이므로 지연 로딩을 적용하면 초기 로드 시간과 대역폭을 절약할 수 있다.

**수정 방법:**
```tsx
<img src="/public/promo.png" alt="Promo" loading="lazy" className="mt-8" />
```

### 2-4. 이미지에 명시적 `width`/`height` 미지정 (심각도: 중간)

**위치:** 50행

`<img>` 태그에 `width`와 `height` 속성이 없다. 브라우저가 이미지 크기를 알 수 없으므로, 이미지 로드 완료 시 레이아웃이 변경(CLS)된다.

**수정 방법:**
```tsx
<img
  src="/public/promo.png"
  alt="Promo"
  loading="lazy"
  width={800}
  height={400}
  className="mt-8"
/>
```

### 2-5. key prop 누락으로 인한 불필요한 DOM 재생성 (심각도: 낮음)

**위치:** 45~47행

`key`가 없으면 React는 배열 인덱스를 기본 키로 사용하지만, 이는 목록 변경 시 불필요한 DOM 재생성과 상태 유실을 야기할 수 있다.

### 2-6. useEffect 내 setTimeout 정리 함수 누락 (심각도: 낮음)

**위치:** 9~20행

`useEffect` 안에서 `setTimeout`을 사용하지만 cleanup 함수에서 `clearTimeout`을 호출하지 않는다. 컴포넌트가 언마운트될 경우 메모리 누수 및 `setState on unmounted component` 경고가 발생할 수 있다.

**수정 방법:**
```tsx
useEffect(() => {
  // layout logic...

  const timerId = setTimeout(() => {
    setItems(["Dashboard", "Analytics", "Reports"]);
  }, 500);

  return () => clearTimeout(timerId);
}, []);
```

---

## 3. 긍정적 요소

| 항목 | 설명 |
|------|------|
| 시맨틱 HTML | `<main>`, `<nav>`, `<section>` 등 적절한 시맨틱 요소 사용 |
| 헤딩 계층 구조 | `<h1>` -> `<h2>` 순서가 올바르게 구성됨 |
| 이미지 alt 텍스트 | `<img>`에 `alt="Promo"`가 존재함 |
| 리스트 마크업 | 네비게이션 항목에 `<ul>/<li>` 사용 |

---

## 4. 이슈 요약

| 카테고리 | 심각도 높음 | 심각도 중간 | 심각도 낮음 |
|----------|:---------:|:---------:|:---------:|
| 접근성   | 1 | 3 | 1 |
| 성능     | 2 | 2 | 2 |
| **합계** | **3** | **5** | **3** |

**총 이슈 수:** 11건

---

## 5. 우선 수정 권장 순서

1. 아이콘 버튼에 `aria-label` 추가 (접근성, 높음)
2. Layout Thrashing 제거 또는 `requestAnimationFrame` 분리 (성능, 높음)
3. CLS 방지를 위한 스켈레톤 UI 또는 공간 예약 (성능, 높음)
4. 이미지에 `loading="lazy"` 및 `width`/`height` 추가 (성능, 중간)
5. SVG에 `aria-hidden="true"` 추가 (접근성, 중간)
6. 동적 콘텐츠 영역에 `aria-live` 적용 (접근성, 중간)
7. `key` prop 추가 (접근성+성능, 중간)
8. `setTimeout` cleanup 함수 추가 (성능, 낮음)
9. `<nav>`에 `aria-label` 추가 (접근성, 낮음)
