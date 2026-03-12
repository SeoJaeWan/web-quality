---
name: seo
description: SEO + Web Performance review covering Technical SEO (11 items) and Page Experience/Core Web Vitals (18 items). Invoked via web-quality orchestrator. Not directly triggerable.
model: sonnet
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

When invoked via the quality orchestrator, use the file list passed from it as-is.
Proceed to Step 2.

Standalone execution only:

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

### Page Experience — LCP (target ≤ 2.5s)

| Code  | Item                      | Detection Pattern                                                     |
| ----- | ------------------------- | --------------------------------------------------------------------- |
| WP-12 | LCP 요소 초기 HTML에 존재 | hero/LCP image rendered via `useEffect(() => { fetch(` — JS-dependent |

### Page Experience — INP (target ≤ 200ms)

| Code  | Item                           | Detection Pattern                                                       |
| ----- | ------------------------------ | ----------------------------------------------------------------------- |
| WP-13 | 이벤트 핸들러 즉각 시각 피드백 | click handlers without immediate visual state change                    |
| WP-14 | 무거운 연산 지연 처리          | synchronous heavy loops; absence of `requestIdleCallback` or Web Worker |
| WP-15 | React memo 활용                | expensive components without `React.memo()` or `useMemo`                |

### Page Experience — CLS (target ≤ 0.1)

| Code  | Item                           | Detection Pattern                                             |
| ----- | ------------------------------ | ------------------------------------------------------------- |
| WP-16 | 뷰포트 위 동적 삽입 금지       | `prepend(`, `insertBefore(` above viewport                    |
| WP-17 | 애니메이션 transform/opacity만 | CSS `transition: height\|width\|top\|left\|margin\|padding`   |
| WP-18 | 동적 콘텐츠 공간 예약          | `<iframe>`, `<video>`, ad slots without reserved `min-height` |

---

## Step 4. Lighthouse SEO + Performance Verification

Run Lighthouse CLI on the SEO and Performance categories to augment static analysis with quantitative data.

### 4-1. Check Environment

When invoked via the quality orchestrator, use the passed `lighthouse_available`, `dev_server_url`, and `runtime_probe_reason` values.

Standalone execution:

```bash
node scripts/resolve-dev-server.mjs
npx lighthouse --version 2>/dev/null || echo "LH_NOT_INSTALLED"
```

- Parse the resolver JSON and use its final `reachable`, `dev_server_url`, and `reason` values.
- Lighthouse not installed or resolver says server unreachable → Lighthouse-target items: keep static analysis result, verdict = `정적분석`
- Environment ready → proceed to Step 4-2

### 4-2. Run Lighthouse

```bash
npx lighthouse {dev_server_url}{route} \
  --output json \
  --output-path /tmp/lh-seo-report.json \
  --chrome-flags="--headless=new" \
  --preset=desktop \
  --only-categories=seo,performance,best-practices
```

Infer route from changed files:
- `src/pages/Dashboard.tsx` → `/dashboard`
- `src/app/about/page.tsx` → `/about`
- Cannot infer → use baseURL only (homepage)

### 4-3. Lighthouse → SEO Item Mapping (8 items)

| Code | Lighthouse audit ID | Item Name |
| --- | --- | --- |
| SEO-01 | `is-crawlable` | noindex 없음 |
| SEO-02 | `document-title` | title 태그 존재하고 고유 |
| SEO-04 | `is-on-https` | HTTPS 사용 |
| SEO-05 | `meta-description` | meta description 존재 |
| SEO-06 | `canonical` | canonical URL 설정 |
| SEO-09 | `doctype` | DOCTYPE html 선언 |
| SEO-10 | `charset` | charset UTF-8 최상단 |
| SEO-11 | `viewport` | viewport meta 태그 |

### 4-4. Lighthouse → Web Performance Item Mapping (9 items)

| Code | Lighthouse audit ID | Item Name |
| --- | --- | --- |
| WP-01 | `render-blocking-resources` | render-blocking script 없음 |
| WP-02 | `prioritize-lcp-image` | LCP 이미지 fetchpriority + preload |
| WP-03 | `render-blocking-resources` | Critical CSS 처리 |
| WP-04 | `unsized-images` | img width/height 또는 aspect-ratio |
| WP-05 | `offscreen-images` | loading="lazy" |
| WP-06 | `modern-image-formats` | WebP/AVIF 포맷 |
| WP-10 | `font-display` | font-display 최적화 |
| WP-12 | `largest-contentful-paint-element` | LCP 요소 초기 HTML 존재 |
| WP-17 | `non-composited-animations` | 애니메이션 transform/opacity |

### 4-5. Interpret Lighthouse Results

Extract `audits[audit_id]` from JSON:

```
score: 1 → ✅ Pass
score: 0 or between 0–1 → check numericValue for verdict
score: null → ➖ N/A
```

For ❌ results, extract the specific failing element's URL, selector, and snippet from `details.items`.

### 4-6. Collect Quantitative Metrics

Extract Core Web Vitals metrics from Lighthouse JSON and include in the report:

| Metric | audit ID | Threshold |
| --- | --- | --- |
| LCP (ms) | `largest-contentful-paint` | ≤ 2500ms |
| CLS | `cumulative-layout-shift` | ≤ 0.1 |
| TBT (ms) | `total-blocking-time` | ≤ 200ms |
| Performance Score | `categories.performance.score` | 0–100 |
| SEO Score | `categories.seo.score` | 0–100 |

Display a metrics summary card at the top of the report.

### 4-7. Cross-Validation (Lighthouse vs Static Analysis)

**When Lighthouse and static analysis results differ → Lighthouse takes precedence.**

- Lighthouse ❌ but static ✅ → **❌** (verdict: `Lighthouse`)
- Lighthouse ✅ but static ❌ → **✅** (verdict: `Lighthouse`)
- Both agree → use that result (verdict: `Lighthouse`)
- Lighthouse not run → keep static analysis result (verdict: `정적분석`)

---

## Step 5. Report Results

Present findings as a markdown checklist table:

| Code | Area | Item | Result | Verdict Method | Issue Found |
| ---- | ---- | ---- | ------ | -------------- | ----------- |

Result values: ✅ Pass / ❌ Fail / ⚠️ Advisory / ➖ N/A / 🔵 판정불가
Verdict method values: `정적분석` / `Lighthouse` / `판정불가`

---

## Step 6. Verify Results

1. Confirm every item (SEO-01 through SEO-11, WP-01 through WP-18) has been evaluated — none skipped.
2. Every ❌ must include: filename, line number or code pattern, concrete issue description.
3. Every ⚠️ must include a specific improvement recommendation.
4. If any item could not be evaluated, mark ➖ and state reason.
5. If zero ❌ items found, state explicitly: "All evaluated items pass."

</Instructions>

<Output_Format>

## SEO & Web Performance 검토 결과 — {YYYY-MM-DD}

검토 파일: {파일 목록}

### Lighthouse 메트릭 요약 (Lighthouse 실행 시에만)

| 메트릭 | 측정값 | 기준값 | 상태 |
| --- | --- | --- | --- |
| Performance Score | {0–100} | — | — |
| SEO Score | {0–100} | — | — |
| LCP | {N}ms | ≤ 2500ms | ✅/❌ |
| CLS | {N} | ≤ 0.1 | ✅/❌ |
| TBT | {N}ms | ≤ 200ms | ✅/❌ |

### Technical SEO (11항목)

| 코드   | 우선순위 | 항목                     | 결과        | 판정방식 | 발견된 문제 |
| ------ | -------- | ------------------------ | ----------- | -------- | ----------- |
| SEO-01 | Critical | noindex 없음             | ✅/❌/⚠️/➖ |          |             |
| SEO-02 | Critical | title 태그 존재하고 고유 | ✅/❌/⚠️/➖ |          |             |
| SEO-03 | Critical | h1 하나                  | ✅/❌/⚠️/➖ |          |             |
| SEO-04 | Critical | HTTPS 사용               | ✅/❌/⚠️/➖ |          |             |
| SEO-05 | High     | meta description         | ✅/❌/⚠️/➖ |          |             |
| SEO-06 | High     | canonical URL            | ✅/❌/⚠️/➖ |          |             |
| SEO-07 | High     | 구조화 데이터 (JSON-LD)  | ✅/❌/⚠️/➖ |          |             |
| SEO-08 | Medium   | 서술적 URL 구조          | ✅/❌/⚠️/➖ |          |             |
| SEO-09 | High     | DOCTYPE html 선언        | ✅/❌/⚠️/➖ |          |             |
| SEO-10 | High     | charset UTF-8 최상단     | ✅/❌/⚠️/➖ |          |             |
| SEO-11 | High     | viewport meta 태그       | ✅/❌/⚠️/➖ |          |             |

### Page Experience / Web Performance (18항목)

| 코드  | 영역   | 항목                               | 결과        | 판정방식 | 발견된 문제 |
| ----- | ------ | ---------------------------------- | ----------- | -------- | ----------- |
| WP-01 | CRP    | render-blocking script 없음        | ✅/❌/⚠️/➖ |          |             |
| WP-02 | CRP    | LCP fetchpriority + preload        | ✅/❌/⚠️/➖ |          |             |
| WP-03 | CRP    | Critical CSS 처리                  | ✅/❌/⚠️/➖ |          |             |
| WP-04 | 이미지 | img width/height 또는 aspect-ratio | ✅/❌/⚠️/➖ |          |             |
| WP-05 | 이미지 | loading="lazy"                     | ✅/❌/⚠️/➖ |          |             |
| WP-06 | 이미지 | WebP/AVIF 포맷                     | ✅/❌/⚠️/➖ |          |             |
| WP-07 | JS     | 코드 스플리팅                      | ✅/❌/⚠️/➖ |          |             |
| WP-08 | JS     | 트리 쉐이킹 패턴                   | ✅/❌/⚠️/➖ |          |             |
| WP-09 | JS     | 레이아웃 스래싱 없음               | ✅/❌/⚠️/➖ |          |             |
| WP-10 | 폰트   | font-display 최적화                | ✅/❌/⚠️/➖ |          |             |
| WP-11 | 폰트   | 중요 폰트 preload                  | ✅/❌/⚠️/➖ |          |             |
| WP-12 | LCP    | LCP 요소 초기 HTML 존재            | ✅/❌/⚠️/➖ |          |             |
| WP-13 | INP    | 이벤트 핸들러 즉각 피드백          | ✅/❌/⚠️/➖ |          |             |
| WP-14 | INP    | 무거운 연산 지연 처리              | ✅/❌/⚠️/➖ |          |             |
| WP-15 | INP    | React memo 활용                    | ✅/❌/⚠️/➖ |          |             |
| WP-16 | CLS    | 뷰포트 위 동적 삽입 금지           | ✅/❌/⚠️/➖ |          |             |
| WP-17 | CLS    | 애니메이션 transform/opacity       | ✅/❌/⚠️/➖ |          |             |
| WP-18 | CLS    | 동적 콘텐츠 공간 예약              | ✅/❌/⚠️/➖ |          |             |

### 수정 가이드

{❌ 항목별 구체적 수정 방법}
</Output_Format>
</Skill_Guide>
