---
name: web-performance
description: Optimize web performance and Core Web Vitals (LCP, INP, CLS). web-quality-reviewer를 통해 실행됩니다. 직접 트리거 불가.
model: sonnet
context: fork
agent: web-quality-reviewer
---

<Skill_Guide>
<Purpose>
Reviews changed web code for loading performance issues and Core Web Vitals
anti-patterns covering the critical rendering path, image optimization,
JavaScript efficiency, font loading, LCP, INP, and CLS.
Runs as a standalone review and outputs a markdown checklist result.
</Purpose>

<Instructions>

## Reference Document

Must read before review:

  references/guide.md (relative to this skill directory)

Contains: Performance budget, Critical rendering path, Image optimization, Font optimization, Caching strategy, Runtime performance, LCP/INP/CLS optimization patterns, Framework quick fixes.

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

### Critical Rendering Path

| Code | Item | Detection Pattern |
|------|------|------------------|
| WP-01 | render-blocking script 없음 | `<script src=` without `defer`/`async`/`type="module"` |
| WP-02 | LCP 이미지 fetchpriority + preload | `fetchpriority="high"` and `<link rel="preload" as="image"` |
| WP-03 | Critical CSS 처리 | render-blocking `<link rel="stylesheet"` without `media` attribute |

### Image Optimization

| Code | Item | Detection Pattern |
|------|------|------------------|
| WP-04 | img width/height 또는 aspect-ratio (CLS 방지) | `<img` without both `width`+`height` or `aspect-ratio` CSS |
| WP-05 | loading="lazy" (below-fold) | `<img` without `loading="lazy"` for non-LCP images |
| WP-06 | 현대 이미지 포맷 (WebP/AVIF) | `<picture>` element, `.webp`, `.avif` extensions |

### JavaScript

| Code | Item | Detection Pattern |
|------|------|------------------|
| WP-07 | 코드 스플리팅 | dynamic `import(` expressions present |
| WP-08 | 트리 쉐이킹 패턴 | `import _ from 'lodash'` or similar whole-library imports |
| WP-09 | 레이아웃 스래싱 없음 | mixed read/write of layout properties in loops |

### Font

| Code | Item | Detection Pattern |
|------|------|------------------|
| WP-10 | font-display 최적화 (block 금지) | `@font-face` without `font-display: swap\|optional\|fallback`, or using `font-display: block` |
| WP-11 | 중요 폰트 preload | `<link rel="preload" as="font"` for critical fonts |

### LCP — Largest Contentful Paint (target ≤ 2.5s)

| Code | Item | Detection Pattern |
|------|------|------------------|
| WP-12 | LCP 요소 초기 HTML에 존재 | hero/LCP image rendered via `useEffect(() => { fetch(` — JS-dependent |

### INP — Interaction to Next Paint (target ≤ 200ms)

| Code | Item | Detection Pattern |
|------|------|------------------|
| WP-13 | 이벤트 핸들러 즉각 시각 피드백 | click handlers without immediate visual state change |
| WP-14 | 무거운 연산 지연 처리 | synchronous heavy loops; absence of `requestIdleCallback` or Web Worker |
| WP-15 | React memo 활용 | expensive components without `React.memo()` or `useMemo` |

### CLS — Cumulative Layout Shift (target ≤ 0.1)

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

1. Confirm every item (WP-01 through WP-18) has been evaluated — none skipped.
2. Every ❌ must include: filename, line number or code pattern, concrete issue description.
3. Every ⚠️ must include a specific improvement recommendation.
4. If any item could not be evaluated, mark ➖ and state reason.
5. If zero ❌ items found, state explicitly: "All evaluated items pass."

</Instructions>

<Output_Format>
## Web Performance 검토 결과 — {YYYY-MM-DD}

검토 파일: {파일 목록}

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
