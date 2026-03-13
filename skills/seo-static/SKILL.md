---
name: seo-static
description: Static code analysis for Technical SEO (11 items) and Web Performance (18 items). Reads source files and evaluates SEO meta tags, HTML compatibility, image optimization, JS patterns, font loading, and Core Web Vitals code patterns without requiring a dev server or browser. Called by the seo orchestrator or usable standalone. Use when asked for static-only SEO analysis without Lighthouse verification.
model: sonnet
context: fork
agent: general-purpose
---

<Skill_Guide>
<Purpose>
Evaluates web source code against Technical SEO (11 items) and Page Experience/Web Performance (18 items)
using static analysis only. No dev server or browser required — works purely from reading source code.

Core Web Vitals are Google search ranking signals, so performance directly impacts SEO.
This skill treats them as a unified concern from a code pattern perspective.
</Purpose>

<Instructions>

## Reference Document

Read before review:

```
references/guide.md
```

Contains: Technical SEO, On-page SEO, Structured data templates, Web Performance optimization,
Core Web Vitals (LCP, INP, CLS) patterns, Framework quick fixes.

---

## Input

This skill accepts a list of target files. When called by the SEO orchestrator,
the file list is passed directly. For standalone use, determine scope via:

```bash
git diff --name-only HEAD
```

Filter to web files: `*.html`, `*.htm`, `*.tsx`, `*.jsx`, `*.ts`, `*.js`, `*.vue`, `*.svelte`, `*.css`, `*.scss`

---

## Code Review (per file)

Read each target file, then evaluate **all 29 items simultaneously** per file to minimize repeated reads.

### Technical SEO — Critical

| Code   | Item                               | Detection Pattern                                          |
| ------ | ---------------------------------- | ---------------------------------------------------------- |
| SEO-01 | noindex 없음                       | `<meta name="robots" content="noindex"` on important pages |
| SEO-02 | title 태그 존재하고 고유 (50-60자) | `<title>` presence and character length                    |
| SEO-03 | 페이지당 h1 하나                   | count `<h1>` tags (must be exactly 1)                      |
| SEO-04 | HTTPS 사용                         | resource URLs use `https://`                               |

### Technical SEO — High Priority

| Code   | Item                              | Detection Pattern                              |
| ------ | --------------------------------- | ---------------------------------------------- |
| SEO-05 | meta description 존재 (150-160자) | `<meta name="description"` presence and length |
| SEO-06 | canonical URL 설정                | `<link rel="canonical"` present                |
| SEO-07 | 구조화 데이터 (JSON-LD)           | `<script type="application/ld+json"` present   |

### Technical SEO — Medium Priority

| Code   | Item            | Detection Pattern                |
| ------ | --------------- | -------------------------------- |
| SEO-08 | 서술적 URL 구조 | minimal query parameters in href |

### HTML Compatibility (SEO Foundation)

| Code   | Item                      | Detection Pattern                    |
| ------ | ------------------------- | ------------------------------------ |
| SEO-09 | DOCTYPE html 선언         | `<!DOCTYPE html>` present            |
| SEO-10 | charset UTF-8 head 최상단 | `<meta charset` position in `<head>` |
| SEO-11 | viewport meta 태그        | `<meta name="viewport"` present      |

### Page Experience — Critical Rendering Path

| Code  | Item                               | Detection Pattern                                                  |
| ----- | ---------------------------------- | ------------------------------------------------------------------ |
| WP-01 | render-blocking script 없음        | `<script src=` without `defer`/`async`/`type="module"`             |
| WP-02 | LCP 이미지 fetchpriority + preload | `fetchpriority="high"` and `<link rel="preload" as="image"`        |
| WP-03 | Critical CSS 처리                  | render-blocking `<link rel="stylesheet"` without `media` attribute |

### Page Experience — Image Optimization

| Code  | Item                                          | Detection Pattern                                          |
| ----- | --------------------------------------------- | ---------------------------------------------------------- |
| WP-04 | img width/height 또는 aspect-ratio (CLS 방지) | `<img` without both `width`+`height` or `aspect-ratio` CSS |
| WP-05 | loading="lazy" (below-fold)                   | `<img` without `loading="lazy"` for non-LCP images         |
| WP-06 | 현대 이미지 포맷 (WebP/AVIF)                  | `<picture>` element, `.webp`, `.avif` extensions           |

### Page Experience — JavaScript

| Code  | Item                 | Detection Pattern                                         |
| ----- | -------------------- | --------------------------------------------------------- |
| WP-07 | 코드 스플리팅        | dynamic `import(` expressions present                     |
| WP-08 | 트리 쉐이킹 패턴     | `import _ from 'lodash'` or similar whole-library imports |
| WP-09 | 레이아웃 스래싱 없음 | mixed read/write of layout properties in loops            |

### Page Experience — Font

| Code  | Item                             | Detection Pattern                                                                             |
| ----- | -------------------------------- | --------------------------------------------------------------------------------------------- |
| WP-10 | font-display 최적화 (block 금지) | `@font-face` without `font-display: swap\|optional\|fallback`, or using `font-display: block` |
| WP-11 | 중요 폰트 preload                | `<link rel="preload" as="font"` for critical fonts                                            |

### Page Experience — LCP (target <= 2.5s)

| Code  | Item                      | Detection Pattern                                                     |
| ----- | ------------------------- | --------------------------------------------------------------------- |
| WP-12 | LCP 요소 초기 HTML에 존재 | hero/LCP image rendered via `useEffect(() => { fetch(` — JS-dependent |

### Page Experience — INP (target <= 200ms)

| Code  | Item                           | Detection Pattern                                                       |
| ----- | ------------------------------ | ----------------------------------------------------------------------- |
| WP-13 | 이벤트 핸들러 즉각 시각 피드백 | click handlers without immediate visual state change                    |
| WP-14 | 무거운 연산 지연 처리          | synchronous heavy loops; absence of `requestIdleCallback` or Web Worker |
| WP-15 | React memo 활용                | expensive components without `React.memo()` or `useMemo`                |

### Page Experience — CLS (target <= 0.1)

| Code  | Item                           | Detection Pattern                                             |
| ----- | ------------------------------ | ------------------------------------------------------------- |
| WP-16 | 뷰포트 위 동적 삽입 금지       | `prepend(`, `insertBefore(` above viewport                    |
| WP-17 | 애니메이션 transform/opacity만 | CSS `transition: height\|width\|top\|left\|margin\|padding`   |
| WP-18 | 동적 콘텐츠 공간 예약          | `<iframe>`, `<video>`, ad slots without reserved `min-height` |

---

## Output Format

Return results as a JSON array. Each item:

```json
{
  "id": "SEO-01",
  "name": "noindex 없음",
  "priority": "Critical",
  "result": "✅",
  "verdict_method": "정적분석",
  "issue": "",
  "fix_guide": ""
}
```

Classification:
- `✅` Pass: no violation found
- `❌` Fail: violation found (include filename:line)
- `⚠️` Advisory: improvement recommended
- `➖` N/A: relevant element does not exist

All items must have `verdict_method: "정적분석"`.

</Instructions>
</Skill_Guide>
