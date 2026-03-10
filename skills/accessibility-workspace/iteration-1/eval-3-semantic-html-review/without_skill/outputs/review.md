# index.html 시맨틱 HTML 및 접근성 검토 결과

**대상 파일:** `features/web-sample/pages/index.html`

---

## 1. 시맨틱 HTML 준수 여부

### 1.1 문서 구조 (Document Structure)

| 항목 | 상태 | 설명 |
|------|------|------|
| `<!DOCTYPE html>` 선언 | 양호 | HTML5 doctype이 올바르게 선언되어 있음 |
| `<html lang>` 속성 | 양호 | `lang="en"` 지정됨. 다만 한국어 페이지라면 `lang="ko"`로 변경 필요 |
| `<meta charset>` | 양호 | UTF-8 문자셋 지정됨 |
| `<meta viewport>` | 양호 | 반응형 뷰포트 설정 포함 |
| `<title>` | 양호 | 제목 태그 존재. 다만 "Sample Page"는 페이지 내용을 구체적으로 설명하지 못함 |

### 1.2 시맨틱 랜드마크 요소 부재 (Critical)

페이지에 시맨틱 랜드마크 요소가 전혀 사용되지 않고 있음. `<body>` 내부에 모든 콘텐츠가 구조화 없이 나열되어 있음.

**누락된 시맨틱 요소:**

- **`<header>`**: 페이지 헤더 영역이 정의되지 않음. `<h1>`과 네비게이션 링크를 `<header>`로 감싸야 함.
- **`<nav>`**: "About Us" 링크가 네비게이션 역할을 하지만 `<nav>` 요소로 감싸져 있지 않음.
- **`<main>`**: 주요 콘텐츠 영역이 `<main>` 태그로 구분되지 않음. 스크린 리더 사용자가 본문 콘텐츠로 바로 이동하기 어려움.
- **`<footer>`**: 푸터 영역 없음.
- **`<section>` 또는 `<article>`**: 콘텐츠가 논리적 섹션으로 구분되지 않음.

**권장 구조:**

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
    <p>Check out our <a href="https://example.com/deals">latest deals</a>.</p>
  </main>
  <footer>
    <!-- 푸터 콘텐츠 -->
  </footer>
</body>
```

### 1.3 제목 체계 (Heading Hierarchy)

- `<h1>` 태그가 1개 존재하며, 이는 적절함.
- 다만 하위 제목(`<h2>`, `<h3>` 등)이 전혀 없어 콘텐츠의 계층 구조가 표현되지 않음.

---

## 2. 접근성 (Accessibility) 검토

### 2.1 이미지 대체 텍스트

| 이미지 | alt 속성 | 상태 | 비고 |
|--------|----------|------|------|
| `/public/hero.png` | `alt="Hero banner"` | 양호 | 대체 텍스트 존재. 다만 더 구체적인 설명이 바람직함 |
| `/public/logo.png` | 없음 | **오류** | alt 속성이 완전히 누락됨. WCAG 1.1.1 (비텍스트 콘텐츠) 위반 |
| `/public/promo.png` | `alt="Promotional banner"` | 양호 | 대체 텍스트 존재 |

**logo.png 수정 권장:**
```html
<img src="/public/logo.png" alt="회사 로고" width="120" height="40" />
```
로고가 순수 장식용이라면 `alt=""`로 빈 문자열을 지정하여 스크린 리더가 건너뛰도록 해야 함.

### 2.2 링크 접근성

| 링크 | 상태 | 비고 |
|------|------|------|
| `<a href="https://example.com/about">About Us</a>` | 양호 | 링크 텍스트가 목적지를 설명함 |
| `<a href="https://example.com/deals">latest deals</a>` | 양호 | 링크 텍스트가 의미 있음 |

- 두 링크 모두 의미 있는 텍스트를 포함하고 있어 양호함.
- 외부 링크에 대해 `target="_blank"` 사용 시 `rel="noopener noreferrer"` 추가를 권장하지만, 현재 새 탭 열기가 없으므로 해당 없음.

### 2.3 키보드 접근성

- 별도의 인터랙티브 위젯이 없어 기본 키보드 접근성에 큰 문제는 없음.
- `tabindex` 관련 이슈 없음.
- 다만 **건너뛰기 링크(skip navigation link)**가 없음. 키보드 사용자가 반복 콘텐츠를 건너뛰고 본문으로 이동할 수 있는 방법이 없음.

### 2.4 스크립트 접근성 이슈

```javascript
label.innerHTML = "Hello, " + userInput;
```

- `innerHTML`을 사용하여 동적으로 콘텐츠를 변경하고 있음.
- 스크린 리더 사용자에게 콘텐츠 변경을 알리는 `aria-live` 영역이 설정되지 않음.
- `location.hash`에서 가져온 사용자 입력을 그대로 삽입하므로 XSS 취약점이 존재함. `textContent`를 사용해야 함.

### 2.5 폰트 접근성

- `@font-face`에 `font-display: swap`이 없어 커스텀 폰트 로딩 중 텍스트가 보이지 않을 수 있음 (FOIT - Flash of Invisible Text). 저시력 사용자나 느린 네트워크 환경에서 콘텐츠 접근이 지연됨.

---

## 3. 문제 요약 및 심각도

### 심각 (Critical)

1. **`alt` 속성 누락** (`/public/logo.png`) - WCAG 1.1.1 위반. 스크린 리더가 파일명을 읽어주어 사용자 경험을 저하시킴.
2. **시맨틱 랜드마크 요소 부재** - `<header>`, `<nav>`, `<main>`, `<footer>` 없음. 보조 기술 사용자가 페이지 구조를 파악하기 어려움.

### 주요 (Major)

3. **건너뛰기 링크 없음** - WCAG 2.4.1 (블록 건너뛰기) 위반. 키보드 사용자의 탐색 효율성 저하.
4. **`innerHTML` 사용으로 인한 동적 콘텐츠 접근성 미비** - `aria-live` 영역 없이 DOM 조작 발생.
5. **`font-display: swap` 누락** - 폰트 로딩 중 텍스트 비가시성으로 콘텐츠 접근 지연.

### 경미 (Minor)

6. **`<meta name="description">` 누락** - 접근성 직접 영향은 없으나 검색 결과에서의 페이지 설명 부재.
7. **제목 계층 구조 불충분** - `<h1>` 이후 하위 제목 없음.
8. **이미지 `width`/`height` 누락** (`promo.png`) - 레이아웃 변동(CLS)으로 인한 사용성 저하 가능.

---

## 4. 개선 권장사항 요약

1. 모든 `<img>` 태그에 의미 있는 `alt` 속성을 추가하거나, 장식용 이미지는 `alt=""`를 지정할 것.
2. `<header>`, `<nav>`, `<main>`, `<footer>` 등 시맨틱 랜드마크 요소를 사용하여 페이지 구조를 명확히 할 것.
3. 페이지 상단에 `<a href="#main-content" class="skip-link">본문 바로가기</a>` 건너뛰기 링크를 추가할 것.
4. `innerHTML` 대신 `textContent`를 사용하고, 동적 콘텐츠 영역에 `aria-live="polite"`를 적용할 것.
5. `@font-face`에 `font-display: swap`을 추가할 것.
6. 모든 이미지에 `width`와 `height` 속성을 명시할 것.
7. 콘텐츠 구조에 맞는 하위 제목 태그(`<h2>`, `<h3>`)를 사용할 것.
