---
name: a11y-browser
description: Browser-based accessibility verification using agent-browser. Tests keyboard navigation, focus visibility, ARIA state changes, duplicate IDs, and color contrast on a live page. Manages dev server lifecycle automatically. Called by the a11y orchestrator or usable standalone. Use when asked for browser-based accessibility testing, keyboard navigation checks, or ARIA verification.
model: sonnet
context: fork
agent: general-purpose
---

<Skill_Guide>
<Purpose>
Verifies interaction-based accessibility items in a real browser using agent-browser CLI.
Covers dynamic behaviors that static analysis cannot detect: keyboard navigation, focus movement,
ARIA state changes, duplicate IDs in rendered DOM, and computed color contrast.

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

### 5-1. A-10 + A-11: Keyboard & Focus Visible

After readiness check, use `-i -c` flags for compact interactive-only snapshots:

```bash
npx agent-browser snapshot -i -c \
  && npx agent-browser press Tab && npx agent-browser snapshot -i -c \
  && npx agent-browser press Tab && npx agent-browser snapshot -i -c \
  && npx agent-browser press Tab && npx agent-browser snapshot -i -c \
  && npx agent-browser press Tab && npx agent-browser snapshot -i -c \
  && npx agent-browser press Tab && npx agent-browser snapshot -i -c \
  && npx agent-browser eval "(() => { const f = document.activeElement; const s = getComputedStyle(f); return JSON.stringify({tag:f.tagName,outline:s.outline,boxShadow:s.boxShadow,border:s.border}); })()"
```

- A-10: All interactive elements reachable via Tab → `✅` / No focus movement → `❌` / Partial → `⚠️`
- A-11: outline/boxShadow/border shows visual change → `✅` / No indicator → `❌`

### 5-2. A-08: Color Contrast (Computed)

Check contrast on elements with explicit text, replacing Lighthouse's role:

```bash
npx agent-browser eval "(() => { const els = document.querySelectorAll('p,span,a,button,label,h1,h2,h3,h4,h5,h6,li,td,th'); const results = []; for (const el of els) { if (!el.textContent.trim()) continue; const s = getComputedStyle(el); const c = s.color; const bg = s.backgroundColor; if (c && bg && bg !== 'rgba(0, 0, 0, 0)') results.push({text:el.textContent.trim().slice(0,30),color:c,bg:bg,fontSize:s.fontSize}); if (results.length >= 10) break; } return JSON.stringify(results); })()"
```

Calculate contrast ratio from the RGB values. WCAG AA requires 4.5:1 for normal text, 3:1 for large text (>=18pt or >=14pt bold).

### 5-3. A-32: Duplicate ID

Confirm suspected duplicate IDs in the actual DOM:

```bash
npx agent-browser eval "document.querySelectorAll('[id]').length + ' total, duplicates: ' + JSON.stringify([...new Set([...document.querySelectorAll('[id]')].map(e=>e.id).filter((id,i,a)=>a.indexOf(id)!==i))])"
```

### 5-4. A-33: ARIA State Changes

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

### 5-5. A-12, A-26, A-28, A-31 (Conditional)

Only test these if relevant elements exist on the page:

- **A-12 Focus order**: Modal/popup trigger → click → check focus moves inside
- **A-26 Change on request**: `<select>` → change option → check no auto-navigation
- **A-28 Error suggestion**: Form → submit empty → check error message + focus
- **A-31 Consistent navigation**: Navigate to another page → check nav structure persists

---

## Step 6. Cross-Validation

When browser results differ from static analysis → **browser result takes precedence**.
Verdict method: `Playwright` (keep this label for report consistency)

---

## Output Format

Return results as a JSON array. Each verified item:

```json
{
  "id": "A-10",
  "name": "키보드 사용 보장",
  "result": "❌",
  "verdict_method": "Playwright",
  "issue": "StatsCard.tsx — div onClick not reachable via Tab, no focus received after 5 Tab presses",
  "fix_guide": "Replace <div onClick> with <button> or add tabIndex={0}, role=\"button\", onKeyDown"
}
```

Classification:
- `✅` Pass / `❌` Fail / `⚠️` Advisory / `➖` N/A
- `🔵 판정불가` with specific reason when verification was not possible

</Instructions>
</Skill_Guide>
