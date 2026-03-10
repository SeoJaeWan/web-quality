# Card.tsx 접근성 검토 결과 (KWCAG 2.2 기준)

**대상 파일:** `features/web-sample/components/Card.tsx`

---

## 발견된 접근성 문제

### 1. 키보드 접근성 미비 (KWCAG 2.2 - 7.1.1 키보드 사용 보장)

**심각도:** 높음

`<div>` 요소에 `onClick` 핸들러가 있지만 키보드로 조작할 수 없다.

- `<div>`는 기본적으로 포커스를 받을 수 없는 비대화형 요소이다.
- `tabIndex` 속성이 없어 Tab 키로 접근이 불가능하다.
- `onKeyDown` 또는 `onKeyUp` 핸들러가 없어 Enter/Space 키로 클릭 동작을 실행할 수 없다.

**해결 방안:**
- `tabIndex={0}`을 추가하고, `onKeyDown` 핸들러에서 Enter/Space 키 입력 시 `handleClick`을 호출한다.
- 또는 `<div>` 대신 `<button>` 요소를 사용한다.

```tsx
// 방법 1: tabIndex + onKeyDown 추가
<div
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleClick();
    }
  }}
  ...
>
```

---

### 2. 대화형 요소에 역할(role) 미지정 (KWCAG 2.2 - 7.1.1 키보드 사용 보장 / 7.3.1 적절한 역할 부여)

**심각도:** 높음

클릭 가능한 `<div>` 요소에 `role` 속성이 없어 보조 기술(스크린 리더 등)이 이 요소의 용도를 파악할 수 없다.

- 사용자가 이 요소가 상호작용 가능한 요소임을 인지할 수 없다.

**해결 방안:**
- `role="button"`을 추가하거나, 시맨틱 HTML 요소(`<button>`, `<a>`)를 사용한다.

```tsx
<div role="button" ...>
```

---

### 3. 중복 ID 사용 (KWCAG 2.2 - 7.3.1 마크업 오류 방지)

**심각도:** 높음

`id="card-item"`이 하드코딩되어 있어, Card 컴포넌트가 목록 등에서 여러 번 렌더링될 경우 동일한 ID가 페이지에 중복 존재하게 된다.

- 중복 ID는 HTML 명세 위반이며, 보조 기술이 특정 요소를 올바르게 참조하지 못하는 원인이 된다.
- `aria-labelledby`, `aria-describedby` 등 ID 참조 기반 속성이 오작동할 수 있다.

**해결 방안:**
- 고유한 ID를 생성하거나(예: `useId()` 훅 사용), 불필요한 경우 `id` 속성을 제거한다.

```tsx
const id = React.useId();
// ...
<div id={`card-item-${id}`} ...>
```

---

### 4. 포커스 스타일 미제공 (KWCAG 2.2 - 7.1.2 초점 이동과 표시)

**심각도:** 중간

클릭 가능한 요소에 포커스를 추가하더라도, 현재 코드에서는 포커스 시 시각적 표시(focus indicator)에 대한 스타일이 정의되어 있지 않다.

- 키보드 사용자가 현재 포커스 위치를 시각적으로 확인할 수 없다.

**해결 방안:**
- CSS 클래스 또는 Tailwind 유틸리티로 포커스 스타일을 추가한다.

```tsx
className={`rounded border p-4 focus:outline-2 focus:outline-blue-500 ${className}`}
```

---

### 5. 인식 가능한 이름(Accessible Name) 부재 (KWCAG 2.2 - 7.3.1 적절한 역할 부여)

**심각도:** 중간

대화형 역할을 하는 `<div>`에 `aria-label` 또는 `aria-labelledby`가 없다. `title` prop이 `<h3>` 내부에 텍스트로 존재하지만, 보조 기술이 `<div>` 자체의 접근 가능한 이름으로 이를 연결하지 못한다.

**해결 방안:**
- `aria-label` 또는 `aria-labelledby`를 사용하여 접근 가능한 이름을 명시적으로 지정한다.

```tsx
<div
  role="button"
  aria-labelledby={`card-title-${id}`}
  ...
>
  <h3 id={`card-title-${id}`}>{title}</h3>
```

---

### 6. 직접 DOM 조작으로 인한 보조 기술 미반영 (KWCAG 2.2 - 7.3.1 마크업 오류 방지)

**심각도:** 낮음

`handleClick` 내부에서 `document.querySelector(".card-highlight")`로 직접 DOM을 조작하여 배경색을 변경하고 있다.

- 이 변경은 React 상태를 통하지 않으므로, 보조 기술에 상태 변경이 전달되지 않는다.
- 시각적 변경만 일어나며 스크린 리더 사용자에게는 아무런 피드백이 없다.

**해결 방안:**
- React `useState`를 사용하여 상태 기반으로 스타일을 관리하고, 필요 시 `aria-live` 영역이나 시각적 변경에 대한 텍스트 피드백을 제공한다.

---

## 요약

| # | 문제 | KWCAG 2.2 관련 지침 | 심각도 |
|---|------|---------------------|--------|
| 1 | 키보드 접근 불가 | 7.1.1 키보드 사용 보장 | 높음 |
| 2 | role 속성 미지정 | 7.1.1 / 7.3.1 적절한 역할 부여 | 높음 |
| 3 | 중복 ID | 7.3.1 마크업 오류 방지 | 높음 |
| 4 | 포커스 표시 없음 | 7.1.2 초점 이동과 표시 | 중간 |
| 5 | 접근 가능한 이름 없음 | 7.3.1 적절한 역할 부여 | 중간 |
| 6 | DOM 직접 조작 | 7.3.1 마크업 오류 방지 | 낮음 |
