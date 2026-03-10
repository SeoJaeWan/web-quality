# KWCAG 2.2 접근성 검토 보고서

## 검토 대상 파일
1. `features/web-sample/pages/index.html`
2. `features/web-sample/pages/dashboard.tsx`
3. `features/web-sample/components/Card.tsx`

---

## 1. index.html 접근성 검토

### 1.1 [심각] 대체 텍스트 누락 (KWCAG 2.2 - 1.1.1 적절한 대체 텍스트 제공)
- **위치**: 30행 `<img src="/public/logo.png" width="120" height="40" />`
- **문제**: `alt` 속성이 완전히 누락되어 있음. 스크린 리더 사용자가 이미지의 의미를 파악할 수 없으며, 파일명이 그대로 읽힐 수 있음.
- **수정 방안**: 이미지의 목적에 맞는 대체 텍스트를 제공해야 함. 로고 이미지라면 `alt="사이트 로고"` 등을 추가. 장식 이미지라면 `alt=""`로 명시적 빈 값을 설정.

```html
<!-- 수정 예시 -->
<img src="/public/logo.png" alt="사이트 로고" width="120" height="40" />
```

### 1.2 [경고] 링크 텍스트의 구체성 부족 (KWCAG 2.2 - 2.4.4 링크 목적)
- **위치**: 35행 `<a href="https://example.com/deals">latest deals</a>`
- **문제**: "latest deals"라는 링크 텍스트는 맥락 없이도 목적을 어느 정도 파악할 수 있으나, 한국어 서비스의 경우 적절한 한국어 텍스트를 제공해야 함. 현재 영문 텍스트로 구성되어 있어 한국어 사용자에게 접근성 문제가 될 수 있음.
- **참고**: `lang="en"` 설정이 되어 있으므로 영문 페이지 자체는 문제없으나, 한국 사용자 대상 서비스라면 `lang="ko"` 및 한국어 콘텐츠 제공 필요.

### 1.3 [경고] innerHTML을 통한 동적 콘텐츠 삽입 (KWCAG 2.2 - 4.2.1 웹 애플리케이션 접근성)
- **위치**: 37~44행 스크립트 블록
- **문제**: `innerHTML`로 사용자 입력(`location.hash`)을 그대로 삽입. XSS 보안 문제 외에도, 동적으로 삽입된 콘텐츠가 스크린 리더에 적절히 전달되지 않을 수 있음. `aria-live` 영역 없이 동적 콘텐츠가 갱신되면 보조 기술 사용자가 변경 사항을 인지하지 못함.
- **수정 방안**: `textContent` 사용 및 `aria-live="polite"` 영역 내에서 콘텐츠 갱신.

```html
<span id="label" aria-live="polite"></span>
<script>
  var label = document.getElementById("label");
  var userInput = decodeURIComponent(location.hash.slice(1));
  if (label) {
    label.textContent = "Hello, " + userInput;
  }
</script>
```

### 1.4 [정보] 페이지 구조 관련 (KWCAG 2.2 - 2.4.1 반복 영역 건너뛰기, 1.3.1 정보와 관계)
- **문제**: `<body>` 내에 `<header>`, `<main>`, `<footer>` 등의 랜드마크 요소가 없음. 스크린 리더 사용자가 페이지 구조를 파악하거나 반복 영역을 건너뛰기 어려움.
- **수정 방안**: 시맨틱 HTML5 랜드마크 요소 사용 및 "본문 바로가기(skip navigation)" 링크 추가.

---

## 2. dashboard.tsx 접근성 검토

### 2.1 [심각] 아이콘 버튼에 접근 가능한 이름 없음 (KWCAG 2.2 - 1.1.1 적절한 대체 텍스트 제공, 4.1.2 이름/역할/값)
- **위치**: 29~31행, 34~36행의 `<button>` 요소
- **문제**: SVG 아이콘만 포함된 버튼에 `aria-label`, `aria-labelledby`, 또는 텍스트가 전혀 없음. 스크린 리더는 이 버튼을 "버튼"으로만 읽으며, 사용자는 버튼의 기능을 알 수 없음.
- **수정 방안**: 각 버튼에 `aria-label`을 추가하고, SVG에 `aria-hidden="true"`를 설정.

```tsx
<button aria-label="알림">
  <svg aria-hidden="true" width="16" height="16" viewBox="0 0 16 16">
    <circle cx="8" cy="8" r="8" />
  </svg>
</button>
```

### 2.2 [경고] SVG 요소에 role 및 대체 텍스트 없음 (KWCAG 2.2 - 1.1.1 적절한 대체 텍스트 제공)
- **위치**: 30행, 35행의 `<svg>` 요소
- **문제**: SVG 요소에 `role="img"` 또는 `<title>` 요소가 없음. 보조 기술이 SVG 콘텐츠를 올바르게 해석하지 못할 수 있음. 아이콘이 장식용이면 `aria-hidden="true"` 필요.
- **수정 방안**: 부모 버튼에 `aria-label`이 있는 경우 SVG에 `aria-hidden="true"` 추가.

### 2.3 [경고] 동적 콘텐츠 로딩 시 접근성 알림 없음 (KWCAG 2.2 - 4.2.1 웹 애플리케이션 접근성)
- **위치**: 17~19행 `setTimeout`을 통한 아이템 로딩
- **문제**: 500ms 후 동적으로 콘텐츠가 삽입되나, `aria-live` 영역이 없어 스크린 리더 사용자가 새 콘텐츠의 등장을 인지하지 못함.
- **수정 방안**: 동적 콘텐츠 영역에 `aria-live="polite"` 추가 또는 로딩 상태를 `aria-busy`로 표시.

```tsx
<section ref={containerRef} className="grid gap-4" aria-live="polite" aria-busy={items.length === 0}>
```

### 2.4 [경고] 리스트 아이템에 key 속성 누락 (KWCAG 2.2 - 간접 영향)
- **위치**: 46행 `items.map((item) => (<div ...>))`
- **문제**: React `key` prop이 없으면 DOM 재조정 시 포커스가 예기치 않게 이동할 수 있어, 키보드 및 보조 기술 사용자에게 혼란을 줄 수 있음.
- **수정 방안**: 고유한 `key` prop 추가.

```tsx
{items.map((item, index) => (
  <div key={item} className="border p-2">{item}</div>
))}
```

### 2.5 [정보] nav 요소에 aria-label 없음 (KWCAG 2.2 - 1.3.1 정보와 관계)
- **위치**: 24행 `<nav className="mb-4">`
- **문제**: 페이지 내 여러 `<nav>` 요소가 있을 경우 각각을 구별할 수 있는 `aria-label` 또는 `aria-labelledby`가 필요. 현재는 하나이므로 큰 문제는 아니나, 확장성을 위해 권장.

---

## 3. Card.tsx 접근성 검토

### 3.1 [심각] 클릭 가능한 div 요소 - 키보드 접근 불가 (KWCAG 2.2 - 2.1.1 키보드 접근성, 4.1.2 이름/역할/값)
- **위치**: 24~33행 `<div onClick={handleClick}>`
- **문제**: `<div>` 요소에 `onClick` 핸들러가 있으나, `role`, `tabIndex`, `onKeyDown`/`onKeyPress` 등이 없음. 키보드 사용자는 이 요소에 포커스를 이동하거나 활성화할 수 없음. 이는 KWCAG 2.2의 키보드 접근성 원칙을 명백히 위반함.
- **수정 방안**:
  - 방법 1 (권장): `<button>` 또는 `<a>` 등 네이티브 인터랙티브 요소로 변경.
  - 방법 2: `role="button"`, `tabIndex={0}`, `onKeyDown` 핸들러 추가.

```tsx
// 방법 2 예시
<div
  id={`card-item-${title}`}
  className={`rounded border p-4 ${className}`}
  onClick={handleClick}
  onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); handleClick(); }}}
  role="button"
  tabIndex={0}
>
```

### 3.2 [심각] 중복 ID (KWCAG 2.2 - 4.1.1 마크업 오류 방지)
- **위치**: 27행 `id="card-item"`
- **문제**: Card 컴포넌트가 리스트에서 여러 번 렌더링되면 동일한 `id="card-item"`이 여러 개 생성됨. HTML 명세상 ID는 고유해야 하며, 중복 ID는 보조 기술의 요소 참조를 깨뜨림. `aria-labelledby`, `aria-describedby` 등이 중복 ID를 참조하면 잘못된 요소와 연결될 수 있음.
- **수정 방안**: 고유한 ID를 생성하거나 ID를 제거.

```tsx
// props로 고유 ID를 전달하거나, title 기반으로 생성
id={`card-item-${title.toLowerCase().replace(/\s+/g, '-')}`}
```

### 3.3 [경고] 클릭 가능 요소에 포커스 표시 없음 (KWCAG 2.2 - 2.4.7 포커스 표시)
- **위치**: 24~33행의 `<div>` 요소
- **문제**: 클릭 가능한 요소에 포커스가 가능해지더라도(tabIndex 추가 시), 포커스 시 시각적 표시(outline 등)가 CSS에 정의되어 있는지 확인 필요. Tailwind CSS의 기본 스타일이 `outline-none`을 적용하는 경우가 있어 포커스 표시가 사라질 수 있음.
- **수정 방안**: `focus:outline` 또는 `focus:ring` 등의 Tailwind 클래스 추가.

```tsx
className={`rounded border p-4 focus:outline-2 focus:outline-blue-500 ${className}`}
```

### 3.4 [경고] 인터랙티브 요소의 역할 미정의 (KWCAG 2.2 - 4.1.2 이름/역할/값)
- **위치**: 24행 `<div>`
- **문제**: 클릭 동작이 있는 `<div>`에 WAI-ARIA role이 없음. 보조 기술이 이 요소를 일반 텍스트 영역으로 인식하여, 사용자가 인터랙션이 가능하다는 것을 알 수 없음.

---

## 요약 (심각도별)

| 심각도 | 개수 | 주요 항목 |
|--------|------|-----------|
| 심각 | 4 | alt 누락, 아이콘 버튼 이름 없음, 키보드 접근 불가 div, 중복 ID |
| 경고 | 6 | SVG 대체 텍스트, 동적 콘텐츠 알림, key 누락, 포커스 표시, 역할 미정의, 링크 텍스트 |
| 정보 | 2 | 랜드마크 구조, nav aria-label |

## KWCAG 2.2 원칙별 위반 요약

### 원칙 1: 인식의 용이성
| 지침 | 위반 사항 | 파일 |
|------|-----------|------|
| 1.1.1 적절한 대체 텍스트 | img alt 누락 | index.html |
| 1.1.1 적절한 대체 텍스트 | 아이콘 버튼 텍스트 없음 | dashboard.tsx |
| 1.3.1 정보와 관계 | 랜드마크 구조 부재 | index.html |

### 원칙 2: 운용의 용이성
| 지침 | 위반 사항 | 파일 |
|------|-----------|------|
| 2.1.1 키보드 접근성 | 클릭 가능 div 키보드 접근 불가 | Card.tsx |
| 2.4.7 포커스 표시 | 인터랙티브 요소 포커스 표시 미확인 | Card.tsx |

### 원칙 3: 이해의 용이성
- 현재 검토 범위에서 주요 위반 없음.

### 원칙 4: 견고성
| 지침 | 위반 사항 | 파일 |
|------|-----------|------|
| 4.1.1 마크업 오류 방지 | 중복 ID | Card.tsx |
| 4.1.2 이름/역할/값 | 아이콘 버튼 이름 없음, div role 미정의 | dashboard.tsx, Card.tsx |
| 4.2.1 웹 앱 접근성 | 동적 콘텐츠 aria-live 없음 | index.html, dashboard.tsx |
