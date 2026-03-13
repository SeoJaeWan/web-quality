---
name: seo-lighthouse
description: Lighthouse CLI-based SEO and Web Performance verification. Runs Lighthouse on a live page to measure Core Web Vitals (LCP, CLS, TBT), Performance/SEO scores, and verify 17 audit items with real measurements. Manages dev server lifecycle automatically. Called by the seo orchestrator or usable standalone. Use when asked for Lighthouse-based SEO testing, Core Web Vitals measurement, or performance verification.
model: sonnet
context: fork
agent: general-purpose
---

<Skill_Guide>
<Purpose>
Verifies SEO and Web Performance items using Lighthouse CLI on a live page.
Provides real measurements that static analysis cannot: Core Web Vitals metrics (LCP, CLS, TBT),
aggregate Performance/SEO scores, and runtime verification of 17 items.

Static analysis can detect code patterns like "missing fetchpriority", but only Lighthouse
can tell you the actual LCP is 4200ms. This runtime data is what makes this skill valuable
as a complement to static analysis.

Automatically starts the dev server if it's not already running.
</Purpose>

<Instructions>

## Step 1. Ensure Dev Server

Lighthouse needs a running dev server to test against.

1. **Find the project** — look for `package.json` files containing a `"dev"` script
   (e.g., `next dev`, `vite`, `webpack serve`). Prefer the one closest to the target files.

2. **Check if already running** — read the port from the dev script or default to 3000:
   ```bash
   curl -s -o /dev/null -w "%{http_code}" http://localhost:3000
   ```

3. **Start if needed**:
   ```bash
   cd {project-dir} && nohup npm run dev > /tmp/dev-server.log 2>&1 &
   echo $!
   ```
   Poll until responsive (up to 30s):
   ```bash
   for i in $(seq 1 30); do
     curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 | grep -q "200\|302\|307" && break
     sleep 1
   done
   ```

4. **Still unreachable** -> return all items as `🔵 판정불가 (dev server 시작 실패)` and stop.

---

## Step 2. Check Lighthouse CLI

```bash
npx lighthouse --version 2>/dev/null || echo "LH_NOT_AVAILABLE"
```

Unavailable -> return all items as `🔵 판정불가 (Lighthouse 사용 불가)` and stop.

---

## Step 3. Determine Target URL

Infer route from the target files:
- `app/dashboard/page.tsx` -> `/dashboard`
- `src/pages/About.tsx` -> `/about`
- Cannot infer -> use base URL (homepage)

---

## Step 4. Run Lighthouse

```bash
npx lighthouse {dev_server_url}{route} \
  --output json \
  --output-path /tmp/lh-seo-report.json \
  --chrome-flags="--headless=new" \
  --preset=desktop \
  --only-categories=seo,performance,best-practices
```

If Lighthouse fails (Chrome not found, timeout, etc.) -> return all items as
`🔵 판정불가 (Lighthouse 실행 실패: {reason})` and stop.

---

## Step 5. SEO Item Mapping (8 items)

Extract audit results from the JSON and map to SEO item codes:

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

---

## Step 6. Web Performance Item Mapping (9 items)

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

---

## Step 7. Interpret Results

Extract `audits[audit_id]` from JSON:

```
score: 1       -> ✅ Pass
score: 0 or 0-1 -> check numericValue for verdict, likely ❌
score: null    -> ➖ N/A
```

For ❌ results, extract the specific failing element's selector and snippet from `details.items`.

---

## Step 8. Collect Core Web Vitals Metrics

This is the unique value Lighthouse provides over static analysis — actual measured numbers.

| Metric | audit ID | Threshold |
| --- | --- | --- |
| LCP (ms) | `largest-contentful-paint` | <= 2500ms |
| CLS | `cumulative-layout-shift` | <= 0.1 |
| TBT (ms) | `total-blocking-time` | <= 200ms |
| Performance Score | `categories.performance.score` | 0-100 |
| SEO Score | `categories.seo.score` | 0-100 |

---

## Step 9. Cross-Validation

When Lighthouse results differ from static analysis -> **Lighthouse result takes precedence**.
Verdict method: `Lighthouse`

---

## Output Format

Return results as a JSON array with two sections:

### Item Results

```json
{
  "id": "SEO-01",
  "name": "noindex 없음",
  "result": "✅",
  "verdict_method": "Lighthouse",
  "issue": "",
  "fix_guide": ""
}
```

### Metrics (separate object)

```json
{
  "metrics": {
    "performance_score": 85,
    "seo_score": 92,
    "lcp_ms": 1850,
    "cls": 0.05,
    "tbt_ms": 120
  }
}
```

Classification:
- `✅` Pass / `❌` Fail / `⚠️` Advisory / `➖` N/A
- `🔵 판정불가` with specific reason when verification was not possible

</Instructions>
</Skill_Guide>
