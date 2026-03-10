---
name: seo
description: SEO + Web Performance review covering Technical SEO (11 items) and Page Experience/Core Web Vitals (18 items). web-quality-reviewer를 통해 실행됩니다. 직접 트리거 불가.
model: sonnet
context: fork
agent: web-quality-reviewer
---

<Skill_Guide>
<Purpose>
Reviews changed web code for search engine optimization and web performance issues.
Covers two areas: Technical SEO (crawlability, on-page elements, structured data,
HTML compatibility) and Page Experience (loading performance, image optimization,
JavaScript efficiency, font loading, Core Web Vitals — LCP, INP, CLS).

Core Web Vitals are Google search ranking signals, so performance directly impacts SEO.
This skill treats them as a unified concern.
</Purpose>

<Instructions>

## Reference Document

Must read before review:

  references/guide.md (relative to this skill directory)

Contains: Technical SEO, On-page SEO, Structured data templates, Web Performance optimization,
Core Web Vitals (LCP, INP, CLS) patterns, Framework quick fixes.

---

## Step 1. Review Scope

이 스킬이 web-quality-audit 오케스트레이터를 통해 실행된 경우,
전달받은 파일 목록을 그대로 사용합니다. Step 2로 진행하세요.

단독 실행 시에만 아래를 수행:

```bash
git diff --name-only HEAD
```

- Filter web files: `*.html`, `*.htm`, `*.tsx`, `*.jsx`, `*.ts`, `*.js`, `*.vue`, `*.svelte`, `*.css`, `*.scss`
- Changed files exist → use as review targets
- No changed files → AskUserQuestion: "검토할 파일이나 작업 내용을 알려주세요."
- User specifies scope explicitly → use that instead

---

## Step 2. Load Reference Guide

Read `references/guide.md (relative to this skill directory)` in full before proceeding.

---

## Step 3. Static Analysis

Read each target file. Evaluate all items below.

### Technical SEO — Critical

| Code | Item | Detection Pattern |
|------|------|------------------|
| SEO-01 | noindex 없음 | `<meta name="robots" content="noindex"` on important pages |
| SEO-02 | title 태그 존재하고 고유 (50-60자) | `<title>` presence and character length |
| SEO-03 | 페이지당 h1 하나 | count `<h1>` tags (must be exactly 1) |
| SEO-04 | HTTPS 사용 | resource URLs use `https://` |

### Technical SEO — High Priority

| Code | Item | Detection Pattern |
|------|------|------------------|
| SEO-05 | meta description 존재 (150-160자) | `<meta name="description"` presence and length |
| SEO-06 | canonical URL 설정 | `<link rel="canonical"` present |
| SEO-07 | 구조화 데이터 (JSON-LD) | `<script type="application/ld+json"` present |

### Technical SEO — Medium Priority

| Code | Item | Detection Pattern |
|------|------|------------------|
| SEO-08 | 서술적 URL 구조 | minimal query parameters in href |

### HTML Compatibility (SEO 기반 요소)

| Code | Item | Detection Pattern |
|------|------|------------------|
| SEO-09 | DOCTYPE html 선언 | `<!DOCTYPE html>` present |
| SEO-10 | charset UTF-8 head 최상단 | `<meta charset` position in `<head>` |
| SEO-11 | viewport meta 태그 | `<meta name="viewport"` present |

### Page Experience — Critical Rendering Path

| Code | Item | Detection Pattern |
|------|------|------------------|
| WP-01 | render-blocking script 없음 | `<script src=` without `defer`/`async`/`type="module"` |
| WP-02 | LCP 이미지 fetchpriority + preload | `fetchpriority="high"` and `<link rel="preload" as="image"` |
| WP-03 | Critical CSS 처리 | render-blocking `<link rel="stylesheet"` without `media` attribute |

### Page Experience — Image Optimization

| Code | Item | Detection Pattern |
|------|------|------------------|
| WP-04 | img width/height 또는 aspect-ratio (CLS 방지) | `<img` without both `width`+`height` or `aspect-ratio` CSS |
| WP-05 | loading="lazy" (below-fold) | `<img` without `loading="lazy"` for non-LCP images |
| WP-06 | 현대 이미지 포맷 (WebP/AVIF) | `<picture>` element, `.webp`, `.avif` extensions |

### Page Experience — JavaScript

| Code | Item | Detection Pattern |
|------|------|------------------|
| WP-07 | 코드 스플리팅 | dynamic `import(` expressions present |
| WP-08 | 트리 쉐이킹 패턴 | `import _ from 'lodash'` or similar whole-library imports |
| WP-09 | 레이아웃 스래싱 없음 | mixed read/write of layout properties in loops |

### Page Experience — Font

| Code | Item | Detection Pattern |
|------|------|------------------|
| WP-10 | font-display 최적화 (block 금지) | `@font-face` without `font-display: swap\|optional\|fallback`, or using `font-display: block` |
| WP-11 | 중요 폰트 preload | `<link rel="preload" as="font"` for critical fonts |

### Page Experience — LCP (target ≤ 2.5s)

| Code | Item | Detection Pattern |
|------|------|------------------|
| WP-12 | LCP 요소 초기 HTML에 존재 | hero/LCP image rendered via `useEffect(() => { fetch(` — JS-dependent |

### Page Experience — INP (target ≤ 200ms)

| Code | Item | Detection Pattern |
|------|------|------------------|
| WP-13 | 이벤트 핸들러 즉각 시각 피드백 | click handlers without immediate visual state change |
| WP-14 | 무거운 연산 지연 처리 | synchronous heavy loops; absence of `requestIdleCallback` or Web Worker |
| WP-15 | React memo 활용 | expensive components without `React.memo()` or `useMemo` |

### Page Experience — CLS (target ≤ 0.1)

| Code | Item | Detection Pattern |
|------|------|------------------|
| WP-16 | 뷰포트 위 동적 삽입 금지 | `prepend(`, `insertBefore(` above viewport |
| WP-17 | 애니메이션 transform/opacity만 | CSS `transition: height\|width\|top\|left\|margin\|padding` |
| WP-18 | 동적 콘텐츠 공간 예약 | `<iframe>`, `<video>`, ad slots without reserved `min-height` |

---

## Step 4. Report Results

Present findings as a markdown checklist table:

| Code | Area | Item | Result | Issue Found |
|------|------|------|--------|-------------|

Result values: ✅ Pass / ❌ Fail / ⚠️ Advisory / ➖ N/A

---

## Step 5. Verify Results

1. Confirm every item (SEO-01 through SEO-11, WP-01 through WP-18) has been evaluated — none skipped.
2. Every ❌ must include: filename, line number or code pattern, concrete issue description.
3. Every ⚠️ must include a specific improvement recommendation.
4. If any item could not be evaluated, mark ➖ and state reason.
5. If zero ❌ items found, state explicitly: "All evaluated items pass."

</Instructions>

<Output_Format>
## SEO & Web Performance 검토 결과 — {YYYY-MM-DD}

검토 파일: {파일 목록}

### Technical SEO (11항목)

| 코드 | 우선순위 | 항목 | 결과 | 발견된 문제 |
|------|---------|------|------|------------|
| SEO-01 | Critical | noindex 없음 | ✅/❌/⚠️/➖ | |
| SEO-02 | Critical | title 태그 존재하고 고유 | ✅/❌/⚠️/➖ | |
| SEO-03 | Critical | h1 하나 | ✅/❌/⚠️/➖ | |
| SEO-04 | Critical | HTTPS 사용 | ✅/❌/⚠️/➖ | |
| SEO-05 | High | meta description | ✅/❌/⚠️/➖ | |
| SEO-06 | High | canonical URL | ✅/❌/⚠️/➖ | |
| SEO-07 | High | 구조화 데이터 (JSON-LD) | ✅/❌/⚠️/➖ | |
| SEO-08 | Medium | 서술적 URL 구조 | ✅/❌/⚠️/➖ | |
| SEO-09 | High | DOCTYPE html 선언 | ✅/❌/⚠️/➖ | |
| SEO-10 | High | charset UTF-8 최상단 | ✅/❌/⚠️/➖ | |
| SEO-11 | High | viewport meta 태그 | ✅/❌/⚠️/➖ | |

### Page Experience / Web Performance (18항목)

| 코드 | 영역 | 항목 | 결과 | 발견된 문제 |
|------|------|------|------|------------|
| WP-01 | CRP | render-blocking script 없음 | ✅/❌/⚠️/➖ | |
| WP-02 | CRP | LCP fetchpriority + preload | ✅/❌/⚠️/➖ | |
| WP-03 | CRP | Critical CSS 처리 | ✅/❌/⚠️/➖ | |
| WP-04 | 이미지 | img width/height 또는 aspect-ratio | ✅/❌/⚠️/➖ | |
| WP-05 | 이미지 | loading="lazy" | ✅/❌/⚠️/➖ | |
| WP-06 | 이미지 | WebP/AVIF 포맷 | ✅/❌/⚠️/➖ | |
| WP-07 | JS | 코드 스플리팅 | ✅/❌/⚠️/➖ | |
| WP-08 | JS | 트리 쉐이킹 패턴 | ✅/❌/⚠️/➖ | |
| WP-09 | JS | 레이아웃 스래싱 없음 | ✅/❌/⚠️/➖ | |
| WP-10 | 폰트 | font-display 최적화 | ✅/❌/⚠️/➖ | |
| WP-11 | 폰트 | 중요 폰트 preload | ✅/❌/⚠️/➖ | |
| WP-12 | LCP | LCP 요소 초기 HTML 존재 | ✅/❌/⚠️/➖ | |
| WP-13 | INP | 이벤트 핸들러 즉각 피드백 | ✅/❌/⚠️/➖ | |
| WP-14 | INP | 무거운 연산 지연 처리 | ✅/❌/⚠️/➖ | |
| WP-15 | INP | React memo 활용 | ✅/❌/⚠️/➖ | |
| WP-16 | CLS | 뷰포트 위 동적 삽입 금지 | ✅/❌/⚠️/➖ | |
| WP-17 | CLS | 애니메이션 transform/opacity | ✅/❌/⚠️/➖ | |
| WP-18 | CLS | 동적 콘텐츠 공간 예약 | ✅/❌/⚠️/➖ | |

### 수정 가이드

{❌ 항목별 구체적 수정 방법}
</Output_Format>
</Skill_Guide>
