---
name: quality
description: Comprehensive web quality review across 2 areas: accessibility (KWCAG2.2 + semantic HTML, 40 items) and SEO & web performance (Technical SEO + Page Experience, 29 items). Generates unified HTML + CSV reports. Use when asked to "web quality audit", "종합 품질 검토", "웹 품질 감사", "전체 품질 리뷰", "접근성 검토", "a11y 체크", "웹표준 확인", "SEO 검토", "성능 검토".
model: sonnet
context: fork
agent: web-quality
---

<Skill_Guide>
<Purpose>
After completing work, performs a comprehensive review of changed web code
across two quality areas — Accessibility (KWCAG2.2 + Semantic HTML) and
SEO & Web Performance (Technical SEO + Page Experience / Core Web Vitals) —
and generates a single unified HTML + CSV report. The accessibility area is
fully delegated to the accessibility skill; the SEO & performance area
delegates to the seo skill.
</Purpose>

<Instructions>

## Internal Execution Order

1. Run accessibility skill
2. Run seo skill

Entry point: always executed via the web-quality agent.

---

## Step 1. Determine Review Scope

```bash
git diff --name-only HEAD
```

- Filter files: `*.html`, `*.htm`, `*.tsx`, `*.jsx`, `*.ts`, `*.js`, `*.vue`, `*.svelte`, `*.css`, `*.scss`
- Changed files exist → use as review targets
- No changed files → AskUserQuestion: "검토할 파일이나 작업 내용을 알려주세요."
- User specifies scope explicitly → use that instead

**Pass the determined file list to sub-skills. Sub-skills must not re-determine scope.**

---

## Step 1.5. Environment Detection (Lighthouse + Playwright)

Detect whether Lighthouse CLI and Playwright MCP are available before delegating to sub-skills.
Pass the detection results as environment context so each sub-skill skips redundant checks.

### 1.5-1. Determine Dev Server URL

Find `playwright.config.ts` in the repository and extract the base URL:

```bash
# Find playwright.config.ts (may not be at repo root)
find . -name "playwright.config.ts" -not -path "*/node_modules/*" 2>/dev/null | head -1
```

If found, read it and extract `baseURL` and `webServer` settings.

Resolution order:
1. `baseURL` from `playwright.config.ts`
2. `webServer.url` from `playwright.config.ts`
3. Fallback: `http://localhost:3000`

Verify the server responds:

```bash
curl -s --connect-timeout 5 "{baseURL}" -o /dev/null -w "%{http_code}"
```

- HTTP 200 → `DEV_SERVER_RUNNING`
- No response → `DEV_SERVER_NOT_RUNNING`

### 1.5-2. Lighthouse CLI

```bash
npx lighthouse --version 2>/dev/null || echo "LH_NOT_INSTALLED"
```

### 1.5-3. Playwright MCP

Check whether Playwright MCP tools are available in the current session
by attempting a no-op call. If `mcp__playwright__browser_snapshot` or similar
tools exist in the tool list, Playwright MCP is available.

### 1.5-4. Pass Environment Context

Pass the following to both accessibility and seo sub-skills:

| Key | Value |
| --- | --- |
| `dev_server_url` | Determined URL or `null` |
| `dev_server_running` | `true` / `false` (curl response) |
| `lighthouse_available` | `true` / `false` (CLI installed + server responds) |
| `playwright_available` | `true` / `false` (MCP tools exist + server responds) |
| `unavailable_reason` | Specific reason when requirements not met |

When requirements are not met: tool-dependent items fall back to static analysis only, verdict marked accordingly.

---

## Step 2. Accessibility Review — Delegate to accessibility skill

Delegate KWCAG2.2 33-item accessibility review to the `accessibility` skill.

Reference: `<plugin-root>/skills/accessibility/SKILL.md`

Delegation instructions:
- Step 1 (scope) is already determined — pass the same file set
- Pass Step 1.5 environment context (lighthouse_available, playwright_available, dev_server_url)
- Steps 2–5: KWCAG2.2 33-item code review + Lighthouse accessibility verification + Playwright interaction verification
- Step 7 (individual report generation) is skipped — collect only result data (✅/❌/⚠️/➖/🔵 per item)

Collected results → **Section A: Accessibility**

---

## Step 3. SEO & Web Performance Review — Delegate to seo skill

Execute the 'seo' skill against the same file set determined in Step 1.
Pass the Step 1.5 environment context (lighthouse_available, dev_server_url).
Steps 3–4: Static Analysis + Lighthouse SEO/Performance verification.
Collect the result row for each SEO-code and WP-code item.
Collected results → **Section B: SEO & Web Performance**

---

## Step 4. Generate Unified Report

Collect results from both sections (A–B) and generate a single HTML + CSV file.

```bash
TIMESTAMP=$(date +%Y%m%d-%H%M)
REPORT_DIR="reports/web-quality/${TIMESTAMP}"
mkdir -p "${REPORT_DIR}"

# Save path
${REPORT_DIR}/report.html
${REPORT_DIR}/report.csv
```

Reuse the same directory for re-runs within the same minute (no suffix needed).

---

## Step 5. Verify Results

1. Confirm both sections (A–B) have been collected — none may be skipped.
2. Confirm both `reports/web-quality/YYYYMMDD-HHmm/report.html` and `reports/web-quality/YYYYMMDD-HHmm/report.csv` have been written.
3. Verify the HTML report contains both section headers (A–B).
4. Verify the CSV contains rows for both areas.
5. If any section was skipped or failed, report the reason and do not claim completion.

</Instructions>

<Output_Format>

Read `references/output-format.md` for full HTML + CSV report templates.

Key requirements:
- 2-area summary grid (접근성 / SEO & Web Performance) with color-coded cards
- Badge classes: `badge-pass` (✅), `badge-fail` (❌), `badge-partial` (⚠️), `badge-na` (➖), `badge-unknown` (🔵)
- Section headers color-coded: a11y=#6c8ebf, seo=#f0a830
- Fix guide section: only ❌ items, with code examples
- Verdict method values: `정적분석` / `Lighthouse` / `Playwright` / `판정불가`
- CSV header: `영역,코드,항목명,결과,판정방식,발견된 문제,수정 가이드`
- Language: Korean / Style: inline CSS only

</Output_Format>
</Skill_Guide>
