---
name: accessibility-review
description: Web accessibility/web standards review. Reviews changed code against KWCAG2.2 and generates HTML + CSV reports. Auto-detects changed files via git diff. Auto-runs Playwright checks (contrast, keyboard, ARIA) when playwright.config.ts exists. Responds to "접근성 검토", "a11y 체크", "웹표준 확인".
---

<Skill_Guide>
<Purpose>
After completing work, reviews changed web code against KWCAG2.2 (Korean Web Content Accessibility Guidelines) 33 items
and checks semantic HTML compliance, then generates HTML + CSV reports in Korean.
Same "post-work reviewer" position as codex-review.
</Purpose>

<Instructions>

## Reference Document

Must read before review:

```
.claude/skills/accessibility-review/references/kwcag22.md
```

- Full KWCAG2.2 33-item criteria table
- Each item includes: Compliance Criteria, Error Types, Details, Auto-Detection level, Detection Pattern, Fix Guide

---

## Step 1. Determine Review Scope

```bash
git diff --name-only HEAD
```

- Filter changed web files: `*.html`, `*.htm`, `*.tsx`, `*.jsx`, `*.ts`, `*.js`, `*.vue`, `*.svelte`, `*.css`, `*.scss`
- If changed web files exist → set those files as review targets
- If no changed web files → AskUserQuestion: "검토할 파일이나 작업 내용을 알려주세요."
- If user specifies a file/scope explicitly → use that instead

---

## Step 2. Load Criteria

Read the full `references/kwcag22.md`.

Identify the **Auto-Detection** level for each of the 33 items:

- `O`: Directly detectable via code pattern → inspect actively
- `△`: Requires Claude's contextual judgment → read and evaluate
- `X`: Requires actual runtime/visual verification → present as checklist

---

## Step 3. Code Review (per file)

Read the target file with Read, then **evaluate all 33 items simultaneously for each file**.
(Minimize repeated file reads)

### Auto-Detection (O) — Direct code inspection

| Item                                     | Detection Pattern                                       |
| ---------------------------------------- | ------------------------------------------------------- |
| 1. Alternative Text (대체 텍스트)        | `<img>` missing alt, `<input type="image">` missing alt |
| 7. Auto-play (자동 재생)                 | `autoplay` attribute used without control               |
| 11. Focus Visible (초점 표시)            | `outline: none/0` without replacement style             |
| 17. Skip Navigation (반복 영역 건너뛰기) | Missing skip nav link (`href="#main"`)                  |
| 25. Language of Page (기본 언어 표시)    | `<html>` missing `lang` attribute                       |
| 29. Label in Name (레이블 제공)          | `<input>` missing `<label>`, `aria-label`, or `title`   |
| 32. Parsing (마크업 오류)                | Duplicate `id`, invalid tag nesting                     |

### Contextual Judgment (△) — Claude interprets code meaning

| Item                                        | Evaluation Criteria                                                   |
| ------------------------------------------- | --------------------------------------------------------------------- |
| 1. Alt Text Quality (대체 텍스트 품질)      | Does alt text actually describe the image content?                    |
| 3. Table Structure (표의 구성)              | Is `<table>` data or layout? Appropriate `<caption>`/`<th>`?          |
| 10. Keyboard Access (키보드 사용)           | Non-interactive elements like `<div onClick>` lacking keyboard access |
| 13. Character Key Shortcuts (문자 단축키)   | Single-character key event handlers present                           |
| 18. Page Title (제목 제공)                  | `<title>` content appropriateness, heading hierarchy logic            |
| 19. Link Purpose (링크 텍스트)              | "더보기", "클릭", empty links, etc.                                   |
| 22. Pointer Cancellation (포인터 입력 취소) | `onMouseDown` immediate execution pattern                             |
| 23. Label and Name (레이블과 네임)          | Icon buttons missing `aria-label`                                     |
| 26. Change on Request (사용자 요구 실행)    | `<select onChange>` auto-navigation pattern                           |
| 28. Error Suggestion (오류 정정)            | Form validation missing error messages and focus management           |
| 33. Web App Accessibility (웹앱 접근성)     | Custom components missing ARIA role/state                             |

### Manual Verification (X) — Present as checklist

| Item                                 | Verification Method                                  |
| ------------------------------------ | ---------------------------------------------------- |
| 2. Captions (자막)                   | Check `<video>` for `<track>` or separate transcript |
| 6. Use of Color (색 구분)            | Directly check if color alone conveys information    |
| 8. Contrast (명도 대비)              | Measure with CCA tool or browser DevTools            |
| 9. Visual Presentation (콘텐츠 구분) | Directly check visual design                         |
| 15. Pause, Stop, Hide (정지 기능)    | Check auto-cycling content behavior                  |
| 16. Seizures (깜박임)                | Check for content flashing 3–50 times per second     |
| 20. Location (참조 위치)             | Check if e-publication document                      |
| 27. Help (도움 정보)                 | Check consistency of help/FAQ location across pages  |

---

### Semantic HTML Review (Web Standards)

Beyond KWCAG2.2, check whether HTML elements are used semantically.

#### Directly Detectable Patterns

| Check Item                    | Detection Pattern                          | Recommended Alternative                     |
| ----------------------------- | ------------------------------------------ | ------------------------------------------- |
| Presentational tags           | `<b>`, `<i>` used alone                    | `<strong>`, `<em>` (when meaningful) or CSS |
| Paragraph via line breaks     | Consecutive `<br><br>`                     | `<p>` tag                                   |
| Inline wrapping block content | `<span>` directly containing block content | `<div>` or semantic element                 |

#### Context-Dependent Patterns

| Check Item            | Evaluation Criteria                                                                |
| --------------------- | ---------------------------------------------------------------------------------- |
| Missing landmarks     | All `<div>` with no `<header>`, `<main>`, `<footer>`, `<nav>`                      |
| Section structure     | Independent content blocks using only `<div>` instead of `<article>` / `<section>` |
| Complementary content | Sidebar/related links area not using `<aside>`                                     |
| Interactive elements  | Clickable `<div>`/`<span>` → can it be replaced with `<button>` or `<a>`?          |
| List structure        | Repeated items as consecutive `<div>` → `<ul>`/`<ol>` + `<li>` recommended         |
| Form grouping         | `<div>`-wrapped form element group → `<fieldset>` + `<legend>` recommended         |
| Quotations            | Quote text not using `<blockquote>` / `<q>`                                        |
| Time/Date             | Date/time display not using `<time datetime="...">`                                |

> **Judgment rule:** Plain layout divs are allowed. Flag as △ only when a **semantically clear region** omits an appropriate semantic element.

---

## Step 4. Playwright 자동 검증

### 4-1. Playwright 환경 자동 감지

```bash
ls playwright.config.ts 2>/dev/null && echo "FOUND" || ls playwright.config.js 2>/dev/null && echo "FOUND" || echo "NOT_FOUND"
```

- **FOUND** → 4-2 ~ 4-5 실행 (항목 8, 10, 33 자동 검사)
- **NOT_FOUND** → 항목 8, 10, 33을 `판정불가 (Playwright 미설치)`로 분류하고 Step 5로 이동

### 4-2. URL 자동 결정

```bash
grep -E "baseURL|webServer" playwright.config.ts 2>/dev/null | head -5
```

결정 순서:
1. `playwright.config.ts` → `baseURL` 값 추출
2. 없으면 `webServer.url` 추출
3. `git diff --name-only HEAD`로 변경 파일에서 라우트 추론
   - `src/pages/Login.tsx` → `/login`
   - `src/pages/Dashboard.tsx` → `/dashboard`
   - `src/app/about/page.tsx` → `/about` (Next.js App Router)
4. 라우트 추론 실패 시 → baseURL만 사용 (홈페이지)
5. baseURL도 없으면 → `http://localhost:3000` 폴백

### 4-3. 항목 8: 명도 대비 자동 검사 (Playwright)

```javascript
browser_navigate({결정된 URL})

browser_evaluate(() => {
  const elements = document.querySelectorAll('p, h1, h2, h3, h4, h5, h6, a, button, label, span, li, td, th');
  return Array.from(elements).slice(0, 50).map(el => {
    const style = getComputedStyle(el);
    return {
      tag: el.tagName,
      text: el.textContent?.trim().slice(0, 30),
      color: style.color,
      background: style.backgroundColor,
      fontSize: style.fontSize,
      fontWeight: style.fontWeight
    };
  });
})
```

판정 기준:
- 일반 텍스트: 전경/배경 대비 **4.5:1 이상**
- 큰 텍스트 (18pt 이상 또는 14pt bold): **3:1 이상**

결과:
- 기준 미달 요소 발견 → `X` (어떤 요소인지 명시)
- 모두 통과 → `O`
- 색상 추출 불가 (투명 배경 등) → `△`

### 4-4. 항목 10: 키보드 접근성 자동 검사 (Playwright)

```
browser_snapshot()              → 초기 상태 기록

browser_press_key('Tab')        → 포커스 이동 1회
browser_snapshot()              → 포커스 확인

browser_press_key('Tab')        → 포커스 이동 2회
browser_snapshot()              → 포커스 확인

(최대 10회 반복)
```

판정 기준:
- Tab 이동 시 포커스가 시각적으로 이동하고 모든 인터랙티브 요소 접근 가능 → `O`
- 포커스 이동 없음 또는 포커스 트랩 발생 → `X`
- 일부 요소만 접근 가능 → `△`

### 4-5. 항목 33: 웹앱 접근성 자동 검사 (Playwright)

```
browser_snapshot()              → 인터랙션 전 스냅샷 (ARIA 상태 기록)

browser_click({첫 번째 인터랙티브 요소 ref})

browser_snapshot()              → 인터랙션 후 스냅샷 (ARIA 상태 변화 확인)
```

판정 기준:
- 인터랙션 후 `aria-expanded`, `aria-selected`, `aria-checked`, `aria-pressed` 등 상태 변화 → `O`
- 상태 변화 없음 (정적 ARIA) → `△`
- 인터랙티브 요소 없음 → `-`

### 4-6. 교차 검증

Playwright 결과가 정적 분석과 다를 경우 → **Playwright 결과 우선**.
리포트에 판정방식 `Playwright` 명시.

---

## Step 5. Classify Results

| Result     | Meaning                                            |
| ---------- | -------------------------------------------------- |
| `O`        | Pass: no violation found                           |
| `X`        | Fail: violation found (include filename:line)      |
| `△`        | Advisory: no violation but improvement recommended |
| `-`        | N/A: the relevant element does not exist           |
| `판정불가` | Playwright 미설치로 런타임 검증 불가               |

---

## Step 6. 리포트 생성 및 저장

동일한 검토 결과를 **2개 포맷**으로 저장한다.

### 저장 파일

- `.claude/reports/accessibility-YYYYMMDD.html` — 시각적 HTML 리포트
- `.claude/reports/accessibility-YYYYMMDD.csv` — 보고서/산출물용 CSV

같은 날짜 파일이 이미 존재하면 `-2`, `-3` 접미사를 붙인다.

### HTML 리포트 요건

- 결과별 색상: `O`(초록 #28a745), `X`(빨강 #dc3545), `△`(노랑 #ffc107), `-`(회색 #6c757d), `판정불가`(파랑 #6c8ebf)
- 구성: 요약 테이블 → 원칙별 상세 결과 → 시맨틱 HTML 검토 → 수정 가이드
- 언어: 한국어 / 스타일: 인라인 CSS만 (외부 의존 없음)
- 판정방식 컬럼: `정적분석` / `Playwright` / `판정불가`

### CSV 리포트 요건

- 헤더: `번호,항목명,원칙,결과,판정방식,발견된 문제,수정 가이드`
- 33개 KWCAG 항목 + 시맨틱 HTML 항목 전체 포함
- 특수문자 이스케이프: 쉼표·줄바꿈 포함 셀은 큰따옴표로 감싸고 내부 큰따옴표는 `""` 처리

---

## Step 7. Verify Results

1. Confirm all 33 KWCAG2.2 items have been evaluated — none skipped.
2. Confirm the Semantic HTML section (7 items) has been evaluated.
3. Every X result must include: KWCAG item number, filename + line number or pattern, concrete violation description.
4. Every △ result must include a specific improvement recommendation.
5. Items marked 판정불가 must state explicitly that playwright.config.ts was not found.
6. Confirm both `.claude/reports/accessibility-YYYYMMDD.html` and `.csv` have been written with correct filenames.
7. If any condition above is not met, do not claim completion — identify what is missing and resolve it.

</Instructions>

<Output_Format>

### HTML 리포트 템플릿

```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>웹 접근성 검토 리포트 — {YYYY-MM-DD}</title>
<style>
  body { font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif; max-width: 1200px; margin: 0 auto; padding: 24px; color: #333; line-height: 1.6; }
  h1 { border-bottom: 3px solid #333; padding-bottom: 8px; }
  h2 { border-left: 5px solid #555; padding-left: 12px; margin-top: 32px; }
  h3 { color: #444; }
  table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 0.9em; }
  th { background: #f5f5f5; padding: 10px 12px; border: 1px solid #ddd; text-align: left; white-space: nowrap; }
  td { padding: 10px 12px; border: 1px solid #ddd; vertical-align: top; }
  tr:hover td { background: #fafafa; }
  .result-O   { background: #d4edda; color: #155724; font-weight: bold; text-align: center; }
  .result-X   { background: #f8d7da; color: #721c24; font-weight: bold; text-align: center; }
  .result-tri { background: #fff3cd; color: #856404; font-weight: bold; text-align: center; }
  .result-na  { background: #e2e3e5; color: #383d41; text-align: center; }
  .result-unknown { background: #dce8f8; color: #1a4a8a; text-align: center; font-size: 0.85em; }
  .method-playwright { color: #0066cc; font-size: 0.8em; font-weight: bold; }
  .method-static     { color: #666; font-size: 0.8em; }
  .method-unknown    { color: #999; font-size: 0.8em; }
  .summary-pass { color: #155724; font-weight: bold; }
  .summary-fail { color: #721c24; font-weight: bold; }
  .fix-X   { background: #fff5f5; border-left: 4px solid #dc3545; border-radius: 0 4px 4px 0; padding: 16px; margin: 12px 0; }
  .fix-tri { background: #fffdf0; border-left: 4px solid #ffc107; border-radius: 0 4px 4px 0; padding: 16px; margin: 12px 0; }
  code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-family: monospace; font-size: 0.9em; }
  .meta { background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 4px; padding: 16px; margin-bottom: 24px; }
  .meta ul { list-style: none; margin: 0; padding: 0; }
  .meta li { margin: 4px 0; }
  .playwright-badge { display: inline-block; background: #0066cc; color: white; font-size: 0.75em; padding: 2px 8px; border-radius: 10px; margin-left: 8px; }
</style>
</head>
<body>

<h1>웹 접근성/웹표준 검토 리포트</h1>

<div class="meta">
<ul>
  <li><strong>날짜:</strong> {YYYY-MM-DD}</li>
  <li><strong>검토 파일:</strong> {변경된 파일 목록}</li>
  <li><strong>기준:</strong> KWCAG2.2 (한국지능정보사회진흥원, 2024.10) + 시맨틱 HTML (HTML Living Standard)</li>
  <li><strong>Playwright:</strong> {사용됨 <span class="playwright-badge">자동검사</span> / 미사용 — playwright.config.ts 없음}</li>
</ul>
</div>

<h2>요약</h2>
<table>
  <tr>
    <th>원칙</th><th>합격(O)</th><th>권고(△)</th><th>불합격(X)</th><th>해당없음(-)</th><th>판정불가</th><th>합격률</th>
  </tr>
  <tr><td>인식의 용이성 (9항목)</td><td class="summary-pass"></td><td></td><td class="summary-fail"></td><td></td><td></td><td></td></tr>
  <tr><td>운용의 용이성 (15항목)</td><td class="summary-pass"></td><td></td><td class="summary-fail"></td><td></td><td></td><td></td></tr>
  <tr><td>이해의 용이성 (7항목)</td><td class="summary-pass"></td><td></td><td class="summary-fail"></td><td></td><td></td><td></td></tr>
  <tr><td>견고성 (2항목)</td><td class="summary-pass"></td><td></td><td class="summary-fail"></td><td></td><td></td><td></td></tr>
  <tr style="font-weight:bold; background:#f5f5f5;">
    <td>전체 (33항목)</td><td class="summary-pass"></td><td></td><td class="summary-fail"></td><td></td><td></td><td><strong>--%</strong></td>
  </tr>
</table>

<h2>상세 결과</h2>

<h3>원칙 1. 인식의 용이성</h3>
<table>
  <tr><th>#</th><th>항목명</th><th>결과</th><th>판정방식</th><th>발견된 문제</th><th>수정 가이드</th></tr>
  <tr>
    <td>1</td><td>적절한 대체 텍스트</td>
    <td class="result-O">O</td>
    <td><span class="method-static">정적분석</span></td>
    <td></td><td></td>
  </tr>
  <!-- 항목 8 — Playwright 사용 시 -->
  <tr>
    <td>8</td><td>명도 대비</td>
    <td class="result-O">O</td>
    <td><span class="method-playwright">Playwright</span></td>
    <td></td><td></td>
  </tr>
  <!-- 항목 8 — playwright.config.ts 없을 때 -->
  <!--
  <tr>
    <td>8</td><td>명도 대비</td>
    <td class="result-unknown">판정불가</td>
    <td><span class="method-unknown">판정불가</span></td>
    <td>playwright.config.ts 없음</td><td>Playwright 설치 후 재검토</td>
  </tr>
  -->
</table>

<h3>원칙 2. 운용의 용이성</h3>
<table>
  <tr><th>#</th><th>항목명</th><th>결과</th><th>판정방식</th><th>발견된 문제</th><th>수정 가이드</th></tr>
  <!-- 항목 10: 키보드 접근성 (Playwright) -->
  <tr>
    <td>10</td><td>키보드 사용</td>
    <td class="result-X">X</td>
    <td><span class="method-playwright">Playwright</span></td>
    <td>Tab 포커스 이동 시 일부 요소 미접근</td>
    <td>인터랙티브 요소에 tabindex=0 및 :focus 스타일 추가</td>
  </tr>
</table>

<h3>원칙 3. 이해의 용이성</h3>
<table>
  <tr><th>#</th><th>항목명</th><th>결과</th><th>판정방식</th><th>발견된 문제</th><th>수정 가이드</th></tr>
</table>

<h3>원칙 4. 견고성</h3>
<table>
  <tr><th>#</th><th>항목명</th><th>결과</th><th>판정방식</th><th>발견된 문제</th><th>수정 가이드</th></tr>
  <!-- 항목 33: 웹앱 접근성 (Playwright) -->
  <tr>
    <td>33</td><td>웹 애플리케이션 접근성</td>
    <td class="result-tri">△</td>
    <td><span class="method-playwright">Playwright</span></td>
    <td>클릭 후 aria-expanded 상태 미변경</td>
    <td>동적 컴포넌트에 aria-expanded 상태 관리 추가</td>
  </tr>
</table>

<h2>시맨틱 HTML 검토</h2>
<table>
  <tr><th>검토 항목</th><th>결과</th><th>판정방식</th><th>발견된 문제</th><th>권고 수정</th></tr>
  <tr><td>랜드마크 요소 (header/main/footer/nav)</td><td class="result-O">O</td><td><span class="method-static">정적분석</span></td><td></td><td></td></tr>
  <tr><td>섹션 구조 (article/section/aside)</td><td class="result-O">O</td><td><span class="method-static">정적분석</span></td><td></td><td></td></tr>
  <tr><td>대화형 요소 (button/a vs div/span)</td><td class="result-O">O</td><td><span class="method-static">정적분석</span></td><td></td><td></td></tr>
  <tr><td>목록 구조 (ul/ol/li)</td><td class="result-O">O</td><td><span class="method-static">정적분석</span></td><td></td><td></td></tr>
  <tr><td>표현용 태그 (b/i → strong/em)</td><td class="result-na">-</td><td><span class="method-static">정적분석</span></td><td></td><td></td></tr>
  <tr><td>폼 그룹 (fieldset/legend)</td><td class="result-na">-</td><td><span class="method-static">정적분석</span></td><td></td><td></td></tr>
  <tr><td>기타 시맨틱 요소 (time/blockquote 등)</td><td class="result-na">-</td><td><span class="method-static">정적분석</span></td><td></td><td></td></tr>
</table>

<h2>수정 필요 항목</h2>

<h3>불합격 (X)</h3>
<!-- 없으면: <p>없음</p> -->
<div class="fix-X">
  <p><strong>항목 {N}. {항목명}</strong> — <code>{파일명}:{라인}</code></p>
  <p><strong>문제:</strong> {구체적인 코드 문제}</p>
  <p><strong>수정:</strong> <code>{구체적인 수정 코드}</code></p>
</div>

<h3>권고 (△)</h3>
<!-- 없으면: <p>없음</p> -->
<div class="fix-tri">
  <p><strong>항목 {N}. {항목명}</strong> (또는 <strong>시맨틱 HTML: {검토 항목}</strong>)</p>
  <p><strong>내용:</strong> {개선 권고 내용}</p>
</div>

</body>
</html>
```

---

### CSV 리포트 템플릿

```
번호,항목명,원칙,결과,판정방식,발견된 문제,수정 가이드
1,적절한 대체 텍스트,인식의 용이성,O,정적분석,,
2,자막 제공,인식의 용이성,-,정적분석,,
3,표의 구성,인식의 용이성,O,정적분석,,
4,색에 무관한 인식,인식의 용이성,-,정적분석,,
5,음성 정보 제공,인식의 용이성,-,정적분석,,
6,색 구분,인식의 용이성,-,정적분석,,
7,자동 재생,인식의 용이성,O,정적분석,,
8,명도 대비,인식의 용이성,O,Playwright,,
9,콘텐츠 구분,인식의 용이성,-,정적분석,,
10,키보드 사용,운용의 용이성,X,Playwright,"Tab 포커스 이동 시 일부 요소 미접근","인터랙티브 요소에 tabindex=0 및 :focus 스타일 추가"
11,초점 이동,운용의 용이성,O,정적분석,,
12,조작 가능,운용의 용이성,-,정적분석,,
13,문자 단축키,운용의 용이성,-,정적분석,,
14,충분한 시간,운용의 용이성,-,정적분석,,
15,정지 기능,운용의 용이성,-,정적분석,,
16,깜박임,운용의 용이성,-,정적분석,,
17,반복 영역 건너뛰기,운용의 용이성,O,정적분석,,
18,제목 제공,운용의 용이성,O,정적분석,,
19,링크 텍스트,운용의 용이성,O,정적분석,,
20,참조 위치,운용의 용이성,-,정적분석,,
21,기기 독립적 사용,운용의 용이성,-,정적분석,,
22,포인터 입력 취소,운용의 용이성,O,정적분석,,
23,레이블과 네임,운용의 용이성,O,정적분석,,
24,움직임 기반 작동,운용의 용이성,-,정적분석,,
25,기본 언어 표시,이해의 용이성,O,정적분석,,
26,사용자 요구 실행,이해의 용이성,O,정적분석,,
27,도움 정보,이해의 용이성,-,정적분석,,
28,오류 정정,이해의 용이성,△,정적분석,"에러 메시지 포커스 이동 없음","폼 오류 시 에러 요소로 포커스 이동 추가"
29,레이블 제공,이해의 용이성,O,정적분석,,
30,오류 방지,이해의 용이성,-,정적분석,,
31,일관된 내비게이션,이해의 용이성,-,정적분석,,
32,마크업 오류,견고성,O,정적분석,,
33,웹 애플리케이션 접근성,견고성,△,Playwright,"클릭 후 aria-expanded 미변경","동적 컴포넌트에 aria-expanded 상태 관리 추가"
시맨틱-1,랜드마크 요소,시맨틱 HTML,O,정적분석,,
시맨틱-2,섹션 구조,시맨틱 HTML,O,정적분석,,
시맨틱-3,대화형 요소,시맨틱 HTML,O,정적분석,,
시맨틱-4,목록 구조,시맨틱 HTML,O,정적분석,,
시맨틱-5,표현용 태그,시맨틱 HTML,-,정적분석,,
시맨틱-6,폼 그룹,시맨틱 HTML,-,정적분석,,
시맨틱-7,기타 시맨틱 요소,시맨틱 HTML,-,정적분석,,
```

</Output_Format>
</Skill_Guide>
