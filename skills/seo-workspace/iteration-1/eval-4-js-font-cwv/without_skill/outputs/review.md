# index.html 분석: JavaScript 로딩, 폰트 최적화, Core Web Vitals

## 1. JavaScript 로딩 방식 이슈

### 1-1. 인라인 스크립트가 `<body>` 끝에 위치하지만 `defer`/`async` 전략 부재

- **위치**: 37~44번째 줄 인라인 `<script>` 블록
- **문제**: 인라인 스크립트는 파서를 차단(parser-blocking)한다. 이 스크립트는 `<body>` 끝부분에 있어 렌더링 차단 영향은 비교적 적지만, 외부 스크립트라면 `defer` 또는 `async` 속성을 사용하는 것이 권장된다. 현재 외부 JS 파일을 로드하는 `<script src="...">` 태그는 없으므로 `defer`/`async`를 적용할 대상은 없지만, 향후 외부 스크립트 추가 시 반드시 고려해야 한다.

### 1-2. `innerHTML` 사용에 의한 XSS 취약점 및 성능 문제

- **위치**: 42번째 줄 `label.innerHTML = "Hello, " + userInput;`
- **문제**:
  - `location.hash`에서 가져온 사용자 입력을 검증 없이 `innerHTML`에 직접 삽입하고 있어 **XSS(Cross-Site Scripting) 공격에 취약**하다.
  - `innerHTML`은 DOM을 다시 파싱하므로 `textContent`보다 성능이 떨어진다.
- **권장 수정**: `textContent`를 사용하고, 사용자 입력은 반드시 sanitize 처리해야 한다.

```js
// 개선 예시
if (label) {
  label.textContent = "Hello, " + decodeURIComponent(userInput);
}
```

### 1-3. 렌더 차단(Render-Blocking) CSS

- **위치**: 10번째 줄 `<link rel="stylesheet" href="https://cdn.example.com/styles.css" />`
- **문제**: `<head>`에 동기 로드되는 외부 CSS는 렌더링을 차단한다. First Contentful Paint(FCP)가 지연된다.
- **권장 수정**:
  - 크리티컬 CSS는 `<style>` 태그로 인라인 처리
  - 비크리티컬 CSS는 `media="print" onload="this.media='all'"` 패턴이나 `rel="preload"`를 사용하여 비동기 로드

```html
<!-- 비동기 CSS 로딩 예시 -->
<link rel="preload" href="https://cdn.example.com/styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'" />
<noscript><link rel="stylesheet" href="https://cdn.example.com/styles.css" /></noscript>
```

---

## 2. 폰트 최적화 이슈

### 2-1. `font-display: swap` 누락

- **위치**: 13~17번째 줄 `@font-face` 선언
- **문제**: `font-display` 속성이 지정되지 않아 기본값인 `auto`가 적용된다. 대부분의 브라우저에서 이는 `block`과 유사하게 동작하며, 폰트가 로드될 때까지 텍스트가 보이지 않는 **FOIT(Flash of Invisible Text)** 현상이 발생한다.
- **Core Web Vitals 영향**: FCP와 LCP가 지연될 수 있다.
- **권장 수정**:

```css
@font-face {
  font-family: "CustomFont";
  src: url("/fonts/custom.woff2") format("woff2");
  font-display: swap;  /* 추가 필요 */
}
```

### 2-2. 폰트 프리로드(Preload) 누락

- **문제**: woff2 폰트 파일에 대한 `<link rel="preload">` 선언이 없다. 폰트는 CSS가 파싱된 후에야 다운로드가 시작되므로, 프리로드를 통해 더 일찍 다운로드를 시작할 수 있다.
- **권장 수정**:

```html
<link rel="preload" href="/fonts/custom.woff2" as="font" type="font/woff2" crossorigin />
```

### 2-3. 폰트 포맷 단일 제공

- **참고**: woff2만 제공하고 있는데, 이는 현대 브라우저에서 가장 효율적인 포맷이므로 적절하다. 다만, 매우 오래된 브라우저 지원이 필요한 경우 woff 폴백을 추가할 수 있다.

---

## 3. Core Web Vitals 이슈

### 3-1. LCP (Largest Contentful Paint) 관련

| 이슈 | 설명 | 심각도 |
|------|------|--------|
| 렌더 차단 CSS | 외부 CSS가 동기 로드되어 LCP 지연 | 높음 |
| font-display 미설정 | 폰트 로드 전까지 텍스트 비가시, LCP 요소가 텍스트인 경우 지연 | 높음 |
| Hero 이미지 프리로드 없음 | `/public/hero.png`(800x400)이 LCP 후보인데 프리로드가 없음 | 중간 |

- **Hero 이미지 개선 권장**:

```html
<link rel="preload" href="/public/hero.png" as="image" />
```

- 또한 hero 이미지에 `fetchpriority="high"` 속성을 추가하면 브라우저가 우선적으로 다운로드한다:

```html
<img src="/public/hero.png" alt="Hero banner" width="800" height="400" fetchpriority="high" />
```

### 3-2. CLS (Cumulative Layout Shift) 관련

| 이슈 | 설명 | 심각도 |
|------|------|--------|
| promo.png에 width/height 미설정 | 33번째 줄: `<img src="/public/promo.png" alt="Promotional banner" />`에 크기 속성이 없어 이미지 로드 시 레이아웃이 밀림 | 높음 |
| font-display 미설정 | 폰트 로드 후 시스템 폰트에서 커스텀 폰트로 전환 시 레이아웃 변동 가능 | 중간 |

- **promo.png 개선 권장**:

```html
<img src="/public/promo.png" alt="Promotional banner" width="600" height="300" />
```

### 3-3. FID / INP (Interaction to Next Paint) 관련

- 현재 페이지에 인터랙티브 요소가 거의 없어 FID/INP 문제는 크지 않다.
- 다만, 인라인 스크립트가 메인 스레드를 동기적으로 실행하므로, 스크립트가 복잡해질 경우 입력 지연이 발생할 수 있다.

### 3-4. FCP (First Contentful Paint) 관련

| 이슈 | 설명 | 심각도 |
|------|------|--------|
| 렌더 차단 CSS | `styles.css`가 로드 완료될 때까지 첫 페인트 불가 | 높음 |
| FOIT (폰트) | CustomFont 로드 전 텍스트 비가시 | 중간 |

---

## 4. 종합 요약 및 우선순위별 개선 권장사항

| 우선순위 | 항목 | 영향받는 지표 |
|----------|------|---------------|
| 1 (긴급) | `@font-face`에 `font-display: swap` 추가 | FCP, LCP, CLS |
| 2 (긴급) | promo.png에 `width`/`height` 속성 추가 | CLS |
| 3 (높음) | 외부 CSS 비동기 로딩 또는 크리티컬 CSS 인라인 처리 | FCP, LCP |
| 4 (높음) | Hero 이미지에 `<link rel="preload">` 및 `fetchpriority="high"` 추가 | LCP |
| 5 (높음) | 커스텀 폰트에 `<link rel="preload">` 추가 | FCP, LCP |
| 6 (중간) | `innerHTML`을 `textContent`로 변경 및 입력 검증 | 보안, INP |
| 7 (낮음) | 향후 외부 JS 추가 시 `defer`/`async` 사용 | FCP, INP |
