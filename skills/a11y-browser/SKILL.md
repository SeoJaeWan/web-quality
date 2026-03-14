---
name: a11y-browser
description: Browser-based accessibility verification using agent-browser. Tests keyboard navigation, focus visibility, ARIA state changes, duplicate IDs, and color contrast on a live page. Manages dev server lifecycle automatically. Called by the a11y orchestrator or usable standalone. Use when asked for browser-based accessibility testing, keyboard navigation checks, or ARIA verification.
model: sonnet
context: fork
agent: general-purpose
---

<Skill_Guide>
<Purpose>
Verifies accessibility items that **cannot be determined from source code alone** using
agent-browser CLI. Focuses on runtime behaviors: computed color contrast, ARIA state
changes on interaction, focus trap behavior, and visual rendering checks.

Items detectable from code (keyboard access patterns, outline removal, duplicate IDs)
are handled by a11y-static's scan script — this skill does not duplicate that work.

Automatically starts the dev server if it's not already running.
</Purpose>

<Instructions>

## Why agent-browser

Each Playwright MCP tool call returns the full accessibility tree (~2-5K tokens per snapshot),
and keyboard testing requires ~10 round-trips. agent-browser chains all commands in a single
Bash call and uses compact snapshots, drastically reducing token usage (~93% savings).

---

## Step 1. Ensure Dev Server

The browser needs a running dev server to test against.

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

4. **Still unreachable** → return all items as `🔵 판정불가 (dev server 시작 실패)` and stop.

---

## Step 2. Check agent-browser

```bash
npx agent-browser --version 2>/dev/null || echo "AB_NOT_AVAILABLE"
```

Unavailable → return all items as `🔵 판정불가 (agent-browser 사용 불가)` and stop.

---

## Step 3. Determine Target URL

Infer route from the target files:
- `app/dashboard/page.tsx` → `/dashboard`
- `src/pages/About.tsx` → `/about`
- Cannot infer → use base URL (homepage)

---

## Step 4. Page Readiness Check

Open the page and take a **full-tree snapshot** (no `-i` flag) to verify the page
actually rendered as expected. This prevents all downstream tests from running against
the wrong page (e.g., a login redirect, error page, or loading spinner).

```bash
npx agent-browser open {URL} \
  && npx agent-browser snapshot -c
```

Determine page state from the snapshot:

| State | How to detect | Action |
| --- | --- | --- |
| **Expected page** | Target components visible in tree | Proceed to Step 5 |
| **Auth redirect** | Login form, `/login` URL, "sign in" text | Verify shared elements (e.g., Navbar) that are present. Remaining → `🔵 판정불가 (인증 필요 페이지)` |
| **Loading/hydration** | Spinner, skeleton, empty body | Wait 3s: `npx agent-browser eval "await new Promise(r => setTimeout(r, 3000))"` then re-snapshot. Still loading → `🔵 판정불가 (페이지 로딩 실패)` |
| **Error page** | 404, 500, error boundary | `🔵 판정불가 (에러 페이지: {status})` |
| **Empty/blocked** | No content, CSP violation | `🔵 판정불가 (페이지 접근 불가)` |

Only verify elements that are actually present in the rendered tree.

---

## Step 5. Verification Tests

Browser verification covers only items that **cannot be determined from source code alone**.
Items like A-10 (keyboard access), A-11 (focus style), A-32 (duplicate ID) are handled
by a11y-static's scan script — no need to re-check them here.

### 5-1. A-08: Color Contrast (Computed)

Check contrast on elements with explicit text, replacing Lighthouse's role:

```bash
npx agent-browser eval "(() => { const els = document.querySelectorAll('p,span,a,button,label,h1,h2,h3,h4,h5,h6,li,td,th'); const results = []; for (const el of els) { if (!el.textContent.trim()) continue; const s = getComputedStyle(el); const c = s.color; const bg = s.backgroundColor; if (c && bg && bg !== 'rgba(0, 0, 0, 0)') results.push({text:el.textContent.trim().slice(0,30),color:c,bg:bg,fontSize:s.fontSize}); if (results.length >= 10) break; } return JSON.stringify(results); })()"
```

Calculate contrast ratio from the RGB values. WCAG AA requires 4.5:1 for normal text, 3:1 for large text (>=18pt or >=14pt bold).

### 5-2. A-33: ARIA State Changes

Check ARIA attribute changes before/after interaction:

```bash
npx agent-browser snapshot -i -c \
  && npx agent-browser click "@eN" \
  && npx agent-browser snapshot -i -c
```

Replace `@eN` with the element ref from the first snapshot (e.g., hamburger, toggle).

- `aria-expanded`, `aria-selected`, `aria-checked`, `aria-pressed` changes → `✅`
- No state change → `⚠️`
- No interactive elements → `➖`

### 5-3. A-12, A-26, A-28, A-31 (Conditional)

Only test these if relevant elements exist on the page:

- **A-12 Focus order**: Modal/popup trigger → click → check focus moves inside
- **A-26 Change on request**: `<select>` → change option → check no auto-navigation
- **A-28 Error suggestion**: Form → submit empty → check error message + focus
- **A-31 Consistent navigation**: Navigate to another page → check nav structure persists

### 5-4. Runtime-Only Items

These items cannot be determined from source code alone — static analysis marks them
as `➖ N/A (브라우저 검증 대상)` and delegates them here. Only test when relevant
elements are detected in the page snapshot:

- **A-02 자막 제공**: `<video>` elements → check if `<track>` exists in DOM, verify
  captions are visible during playback
  ```bash
  npx agent-browser eval "JSON.stringify([...document.querySelectorAll('video')].map(v => ({src:v.src,tracks:[...v.querySelectorAll('track')].map(t=>({kind:t.kind,src:t.src}))})))"
  ```

- **A-04 선형 구조**: Check if visual rendering order matches DOM order
  ```bash
  npx agent-browser eval "JSON.stringify([...document.querySelectorAll('button,a,input,[tabindex]')].slice(0,10).map(e => {const r=e.getBoundingClientRect(); return {tag:e.tagName,text:e.textContent?.slice(0,20),top:Math.round(r.top),left:Math.round(r.left)}}))"
  ```
  Compare `top`/`left` positions against DOM order — significant mismatches indicate
  CSS reordering that may confuse screen readers.

- **A-06 색에 무관한 인식**: Check if color is the sole means of conveying information
  ```bash
  npx agent-browser eval "JSON.stringify([...document.querySelectorAll('.error,.required,.active,.selected,.invalid')].slice(0,5).map(e => {const s=getComputedStyle(e); return {text:e.textContent?.slice(0,30),color:s.color,bg:s.backgroundColor,hasIcon:!!e.querySelector('svg,img,.icon'),hasBorder:s.borderWidth!=='0px'}}))"
  ```
  Elements relying only on color (no icon, border, or text indicator) → `⚠️`

- **A-09 콘텐츠 구분**: Check adjacent content blocks have visual separation
  ```bash
  npx agent-browser eval "JSON.stringify([...document.querySelectorAll('section,article,aside,nav')].slice(0,5).map(e => {const s=getComputedStyle(e); return {tag:e.tagName,border:s.border,padding:s.padding,margin:s.margin,bg:s.backgroundColor}}))"
  ```

- **A-15 정지 기능**: Detect auto-cycling content and check for pause controls
  ```bash
  npx agent-browser eval "JSON.stringify({carousels: document.querySelectorAll('[class*=carousel],[class*=slider],[class*=swiper]').length, pauseButtons: document.querySelectorAll('[aria-label*=pause],[aria-label*=stop],[class*=pause]').length, animations: document.querySelectorAll('[style*=animation]').length})"
  ```

- **A-16 깜박임**: Check for rapid animations
  ```bash
  npx agent-browser eval "JSON.stringify([...document.querySelectorAll('*')].filter(e => {const s=getComputedStyle(e); return s.animationName!=='none'}).slice(0,5).map(e => {const s=getComputedStyle(e); return {tag:e.tagName,animation:s.animationName,duration:s.animationDuration}}))"
  ```

- **A-27 도움 정보**: Navigate to 2+ pages and check help link consistency
  ```bash
  npx agent-browser snapshot -i -c
  ```
  Note help/support link positions, then navigate to another page and re-snapshot.
  Compare link positions for consistency.

For items where no relevant elements exist on the page, mark as `➖ N/A`.

---

## Step 6. Cross-Validation

When browser results differ from static analysis → **browser result takes precedence**.
Verdict method: `브라우저 검증`

---

## Output Format

**Only output items with issues** (❌, ⚠️, or 🔵 판정불가). Passing items (✅) and
N/A items (➖) are omitted — focus on actionable findings only.

Return a JSON object with summary and findings:

```json
{
  "summary": {
    "url_tested": "http://localhost:3000/dashboard",
    "items_verified": 12,
    "violations": 2,
    "advisories": 1,
    "inconclusive": 0
  },
  "findings": [
    {
      "id": "A-10",
      "name": "키보드 사용 보장",
      "result": "❌",
      "verdict_method": "브라우저 검증",
      "issue": "StatsCard — div onClick not reachable via Tab",
      "fix_guide": "Replace <div onClick> with <button> or add tabIndex={0}, role=\"button\", onKeyDown"
    }
  ]
}
```

- `findings` contains only ❌, ⚠️, and 🔵 items
- 🔵 판정불가 must include specific reason (e.g., "인증 필요 페이지")
- If no issues found, return empty `findings: []` with the summary

</Instructions>
</Skill_Guide>
