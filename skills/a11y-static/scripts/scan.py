#!/usr/bin/env python3
"""KWCAG2.2 static accessibility scanner.

Scans web source files (HTML, JSX, TSX, Vue, Svelte) for accessibility issues
using regex-based pattern matching. Outputs structured JSON to stdout.

Usage:
    python scan.py file1.tsx file2.html ...
    python scan.py --dir src/

Handles both HTML and JSX syntax (className, {}, self-closing tags).
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read_file(path: str) -> str:
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def find_line(content: str, pos: int) -> int:
    """Return 1-based line number for a character position."""
    return content[:pos].count("\n") + 1


def collect_files(paths: list[str]) -> list[str]:
    """Expand directories and filter to web files."""
    WEB_EXTS = {".html", ".htm", ".tsx", ".jsx", ".ts", ".js", ".vue", ".svelte", ".css", ".scss"}
    result = []
    for p in paths:
        pp = Path(p)
        if pp.is_dir():
            for f in pp.rglob("*"):
                if f.suffix.lower() in WEB_EXTS and "node_modules" not in f.parts:
                    result.append(str(f))
        elif pp.suffix.lower() in WEB_EXTS:
            result.append(str(p))
    return sorted(set(result))


# ---------------------------------------------------------------------------
# Scanners — each returns a list of finding dicts
# ---------------------------------------------------------------------------

def scan_a01_alt_text(content: str, fname: str) -> list[dict]:
    """A-01: img without alt, input type=image without alt."""
    findings = []
    # <img without alt (HTML and JSX)
    for m in re.finditer(r'<img\b([^>]*?)(/\s*>|>)', content, re.IGNORECASE | re.DOTALL):
        attrs = m.group(1)
        if not re.search(r'\balt\s*=', attrs, re.IGNORECASE):
            findings.append({
                "item": "A-01", "severity": "error",
                "file": fname, "line": find_line(content, m.start()),
                "message": "<img> missing alt attribute",
                "code": m.group(0)[:80]
            })
    # <input type="image" without alt
    for m in re.finditer(r'<input\b([^>]*?)(/\s*>|>)', content, re.IGNORECASE | re.DOTALL):
        attrs = m.group(1)
        if re.search(r'type\s*=\s*["\']image["\']', attrs, re.IGNORECASE):
            if not re.search(r'\balt\s*=', attrs, re.IGNORECASE):
                findings.append({
                    "item": "A-01", "severity": "error",
                    "file": fname, "line": find_line(content, m.start()),
                    "message": "<input type=\"image\"> missing alt attribute",
                    "code": m.group(0)[:80]
                })
    # img with empty alt on potentially meaningful context (candidate for LLM review)
    for m in re.finditer(r'<img\b([^>]*?)(/\s*>|>)', content, re.IGNORECASE | re.DOTALL):
        attrs = m.group(1)
        if re.search(r'alt\s*=\s*["\']["\']', attrs) or re.search(r'alt\s*=\s*\{["\']["\']\}', attrs):
            # Check if it looks like a meaningful image (has descriptive src)
            src_match = re.search(r'src\s*=\s*["\{].*?(chart|graph|logo|icon|banner|hero|photo|product)', attrs, re.IGNORECASE)
            if src_match:
                findings.append({
                    "item": "A-01", "severity": "candidate",
                    "file": fname, "line": find_line(content, m.start()),
                    "message": "Potentially meaningful image has empty alt=\"\" — verify if decorative",
                    "code": m.group(0)[:80]
                })
    return findings


def scan_a07_autoplay(content: str, fname: str) -> list[dict]:
    """A-07: autoplay attribute on audio/video."""
    findings = []
    for m in re.finditer(r'<(audio|video)\b([^>]*?)>', content, re.IGNORECASE | re.DOTALL):
        attrs = m.group(2)
        if re.search(r'\bautoplay\b', attrs, re.IGNORECASE) or re.search(r'\bautoPlay\b', attrs):
            has_muted = bool(re.search(r'\bmuted\b', attrs, re.IGNORECASE))
            findings.append({
                "item": "A-07", "severity": "error" if not has_muted else "candidate",
                "file": fname, "line": find_line(content, m.start()),
                "message": f"<{m.group(1)}> has autoplay" + (" (muted)" if has_muted else " without muted"),
                "code": m.group(0)[:80]
            })
    return findings


def scan_a10_keyboard(content: str, fname: str) -> list[dict]:
    """A-10: Non-interactive elements with click handlers but no keyboard support."""
    findings = []
    # div/span/li with onClick but no onKeyDown/onKeyPress/onKeyUp and no role="button"
    pattern = r'<(div|span|li|td|tr)\b([^>]*?on[Cc]lick[^>]*?)>'
    for m in re.finditer(pattern, content, re.DOTALL):
        attrs = m.group(2)
        has_keyboard = bool(re.search(r'on[Kk]ey(Down|Press|Up)', attrs))
        has_role = bool(re.search(r'role\s*=\s*["\']button["\']', attrs, re.IGNORECASE))
        has_tabindex = bool(re.search(r'tabIndex\s*=\s*["\{]', attrs, re.IGNORECASE))
        if not has_keyboard and not has_role:
            findings.append({
                "item": "A-10", "severity": "candidate",
                "file": fname, "line": find_line(content, m.start()),
                "message": f"<{m.group(1)}> has onClick without keyboard handler or role=\"button\"" +
                           (" (has tabIndex)" if has_tabindex else ""),
                "code": m.group(0)[:100]
            })
    return findings


def scan_a11_focus_visible(content: str, fname: str) -> list[dict]:
    """A-11: outline: none/0 without replacement focus style."""
    findings = []
    # CSS outline removal patterns
    for m in re.finditer(r'outline\s*:\s*(none|0)\b', content, re.IGNORECASE):
        # Check surrounding context for replacement styles
        ctx_start = max(0, m.start() - 200)
        ctx_end = min(len(content), m.end() + 200)
        context = content[ctx_start:ctx_end]
        has_replacement = bool(re.search(r'(box-shadow|border|outline-offset|ring)', context, re.IGNORECASE))
        if not has_replacement:
            findings.append({
                "item": "A-11", "severity": "error",
                "file": fname, "line": find_line(content, m.start()),
                "message": "outline: none/0 without replacement focus style",
                "code": content[max(0, m.start()-30):m.end()+30].strip()
            })
        else:
            findings.append({
                "item": "A-11", "severity": "candidate",
                "file": fname, "line": find_line(content, m.start()),
                "message": "outline removed but replacement style found nearby — verify adequacy",
                "code": content[max(0, m.start()-30):m.end()+30].strip()
            })
    return findings


def scan_a17_skip_nav(content: str, fname: str) -> list[dict]:
    """A-17: Missing skip navigation link."""
    findings = []
    # Only check files that look like page/layout components
    is_page = bool(re.search(r'(page|layout|index|app)\.(tsx|jsx|html|vue|svelte)', fname, re.IGNORECASE))
    if not is_page:
        return findings
    has_skip = bool(re.search(r'href\s*=\s*["\']#(main|content|main-content)', content, re.IGNORECASE))
    has_skip = has_skip or bool(re.search(r'skip.*(nav|link|content)', content, re.IGNORECASE))
    if not has_skip:
        findings.append({
            "item": "A-17", "severity": "candidate",
            "file": fname, "line": 1,
            "message": "Page/layout file without skip navigation link (href=\"#main\")",
            "code": ""
        })
    return findings


def scan_a18_heading(content: str, fname: str) -> list[dict]:
    """A-18: Heading hierarchy and title issues."""
    findings = []
    # Check heading hierarchy (h1-h6)
    headings = [(int(m.group(1)), find_line(content, m.start()))
                for m in re.finditer(r'<h([1-6])\b', content, re.IGNORECASE)]
    if headings:
        prev_level = 0
        for level, line in headings:
            if prev_level > 0 and level > prev_level + 1:
                findings.append({
                    "item": "A-18", "severity": "candidate",
                    "file": fname, "line": line,
                    "message": f"Heading hierarchy skip: h{prev_level} → h{level}",
                    "code": ""
                })
            prev_level = level
    # iframe without title
    for m in re.finditer(r'<iframe\b([^>]*?)>', content, re.IGNORECASE | re.DOTALL):
        attrs = m.group(1)
        if not re.search(r'\btitle\s*=', attrs, re.IGNORECASE):
            findings.append({
                "item": "A-18", "severity": "error",
                "file": fname, "line": find_line(content, m.start()),
                "message": "<iframe> missing title attribute",
                "code": m.group(0)[:80]
            })
    return findings


def scan_a19_link_text(content: str, fname: str) -> list[dict]:
    """A-19: Poor link text."""
    findings = []
    VAGUE_TEXTS = ["더보기", "클릭", "여기", "바로가기", "click here", "here", "more", "read more", "link"]
    for m in re.finditer(r'<a\b([^>]*?)>(.*?)</a>', content, re.IGNORECASE | re.DOTALL):
        attrs = m.group(1)
        text = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        has_aria = bool(re.search(r'aria-label\s*=', attrs, re.IGNORECASE))
        if not text and not has_aria:
            findings.append({
                "item": "A-19", "severity": "error",
                "file": fname, "line": find_line(content, m.start()),
                "message": "Empty link text without aria-label",
                "code": m.group(0)[:80]
            })
        elif text.lower().strip() in [t.lower() for t in VAGUE_TEXTS] and not has_aria:
            findings.append({
                "item": "A-19", "severity": "candidate",
                "file": fname, "line": find_line(content, m.start()),
                "message": f"Vague link text: \"{text}\" — consider adding context",
                "code": m.group(0)[:80]
            })
    return findings


def scan_a25_lang(content: str, fname: str) -> list[dict]:
    """A-25: html element missing lang attribute."""
    findings = []
    html_match = re.search(r'<html\b([^>]*?)>', content, re.IGNORECASE | re.DOTALL)
    if html_match:
        attrs = html_match.group(1)
        if not re.search(r'\blang\s*=', attrs, re.IGNORECASE):
            findings.append({
                "item": "A-25", "severity": "error",
                "file": fname, "line": find_line(content, html_match.start()),
                "message": "<html> missing lang attribute",
                "code": html_match.group(0)[:60]
            })
    return findings


def scan_a26_change_on_request(content: str, fname: str) -> list[dict]:
    """A-26: select onChange causing navigation."""
    findings = []
    for m in re.finditer(r'<select\b([^>]*?)>', content, re.IGNORECASE | re.DOTALL):
        attrs = m.group(1)
        if re.search(r'on[Cc]hange', attrs):
            findings.append({
                "item": "A-26", "severity": "candidate",
                "file": fname, "line": find_line(content, m.start()),
                "message": "<select> has onChange — verify it doesn't auto-navigate",
                "code": m.group(0)[:80]
            })
    return findings


def scan_a29_label(content: str, fname: str) -> list[dict]:
    """A-29: Input elements without associated labels."""
    findings = []
    SKIP_TYPES = {"hidden", "submit", "button", "reset", "image"}
    for m in re.finditer(r'<input\b([^>]*?)(/\s*>|>)', content, re.IGNORECASE | re.DOTALL):
        attrs = m.group(1)
        # Get input type
        type_match = re.search(r'type\s*=\s*["\'](\w+)["\']', attrs, re.IGNORECASE)
        input_type = type_match.group(1).lower() if type_match else "text"
        if input_type in SKIP_TYPES:
            continue
        has_label_ref = bool(re.search(r'\bid\s*=', attrs, re.IGNORECASE))
        has_aria = bool(re.search(r'aria-label(ledby)?\s*=', attrs, re.IGNORECASE))
        has_title = bool(re.search(r'\btitle\s*=', attrs, re.IGNORECASE))
        # Check if wrapped in <label>
        ctx_start = max(0, m.start() - 100)
        pre_ctx = content[ctx_start:m.start()]
        wrapped = bool(re.search(r'<label\b', pre_ctx, re.IGNORECASE))
        if not has_aria and not has_title and not wrapped:
            if has_label_ref:
                # Has id — check if a <label for="..."> exists
                id_match = re.search(r'id\s*=\s*["\']([^"\']+)["\']', attrs)
                if id_match:
                    label_for = re.search(r'<label\b[^>]*\bfor\s*=\s*["\']' + re.escape(id_match.group(1)) + r'["\']', content, re.IGNORECASE)
                    if label_for:
                        continue
            findings.append({
                "item": "A-29", "severity": "error",
                "file": fname, "line": find_line(content, m.start()),
                "message": f"<input type=\"{input_type}\"> without label, aria-label, or title",
                "code": m.group(0)[:80]
            })
    # textarea/select without label
    for tag in ["textarea", "select"]:
        for m in re.finditer(rf'<{tag}\b([^>]*?)>', content, re.IGNORECASE | re.DOTALL):
            attrs = m.group(1)
            has_aria = bool(re.search(r'aria-label(ledby)?\s*=', attrs, re.IGNORECASE))
            has_title = bool(re.search(r'\btitle\s*=', attrs, re.IGNORECASE))
            ctx_start = max(0, m.start() - 100)
            wrapped = bool(re.search(r'<label\b', content[ctx_start:m.start()], re.IGNORECASE))
            if not has_aria and not has_title and not wrapped:
                findings.append({
                    "item": "A-29", "severity": "error",
                    "file": fname, "line": find_line(content, m.start()),
                    "message": f"<{tag}> without label, aria-label, or title",
                    "code": m.group(0)[:80]
                })
    return findings


def scan_a32_parsing(content: str, fname: str) -> list[dict]:
    """A-32: Duplicate IDs."""
    findings = []
    ids: dict[str, list[int]] = {}
    for m in re.finditer(r'\bid\s*=\s*["\']([^"\']+)["\']', content):
        id_val = m.group(1)
        ids.setdefault(id_val, []).append(find_line(content, m.start()))
    for id_val, lines in ids.items():
        if len(lines) > 1:
            findings.append({
                "item": "A-32", "severity": "error",
                "file": fname, "line": lines[0],
                "message": f"Duplicate id=\"{id_val}\" found {len(lines)} times (lines: {', '.join(map(str, lines))})",
                "code": ""
            })
    return findings


def scan_a33_aria(content: str, fname: str) -> list[dict]:
    """A-33: Custom components missing ARIA attributes."""
    findings = []
    role_requirements = {
        "button": ["aria-pressed", "aria-expanded", "aria-label"],
        "tab": ["aria-selected", "aria-controls"],
        "tabpanel": ["aria-labelledby"],
        "dialog": ["aria-modal", "aria-labelledby"],
        "switch": ["aria-checked"],
        "checkbox": ["aria-checked"],
        "combobox": ["aria-expanded"],
        "menu": ["aria-labelledby"],
        "menuitem": ["aria-label"],
    }
    for m in re.finditer(r'role\s*=\s*["\'](\w+)["\']', content, re.IGNORECASE):
        role = m.group(1).lower()
        if role in role_requirements:
            ctx_start = max(0, m.start() - 200)
            ctx_end = min(len(content), m.end() + 200)
            context = content[ctx_start:ctx_end]
            required = role_requirements[role]
            has_any = any(re.search(attr.replace("-", r"[-]?"), context, re.IGNORECASE) for attr in required)
            if not has_any:
                findings.append({
                    "item": "A-33", "severity": "candidate",
                    "file": fname, "line": find_line(content, m.start()),
                    "message": f"role=\"{role}\" without expected ARIA attributes ({', '.join(required[:2])}...)",
                    "code": content[m.start():min(m.start()+80, len(content))]
                })
    return findings


def scan_a03_table(content: str, fname: str) -> list[dict]:
    """A-03: Table structure issues."""
    findings = []
    for m in re.finditer(r'<table\b([^>]*?)>(.*?)</table>', content, re.IGNORECASE | re.DOTALL):
        table_content = m.group(2)
        has_caption = bool(re.search(r'<caption\b', table_content, re.IGNORECASE))
        has_th = bool(re.search(r'<th\b', table_content, re.IGNORECASE))
        if not has_th:
            findings.append({
                "item": "A-03", "severity": "candidate",
                "file": fname, "line": find_line(content, m.start()),
                "message": "<table> without <th> — verify if data table or layout table",
                "code": ""
            })
        if not has_caption and has_th:
            findings.append({
                "item": "A-03", "severity": "candidate",
                "file": fname, "line": find_line(content, m.start()),
                "message": "Data table without <caption>",
                "code": ""
            })
    return findings


def scan_a13_char_shortcut(content: str, fname: str) -> list[dict]:
    """A-13: Single character keyboard shortcuts."""
    findings = []
    # Look for keydown/keypress handlers checking single characters
    for m in re.finditer(r'on[Kk]ey(Down|Press|Up)\s*=\s*\{', content):
        ctx_end = min(len(content), m.end() + 300)
        handler_ctx = content[m.end():ctx_end]
        # Check for single key comparisons without modifier keys
        if re.search(r'key\s*===?\s*["\'][a-zA-Z0-9]["\']', handler_ctx):
            if not re.search(r'(ctrl|alt|shift|meta)Key', handler_ctx, re.IGNORECASE):
                findings.append({
                    "item": "A-13", "severity": "candidate",
                    "file": fname, "line": find_line(content, m.start()),
                    "message": "Single character keyboard shortcut without modifier key",
                    "code": content[m.start():min(m.start()+80, len(content))]
                })
    return findings


def scan_a22_pointer_cancel(content: str, fname: str) -> list[dict]:
    """A-22: onMouseDown/onPointerDown with immediate execution."""
    findings = []
    for m in re.finditer(r'on(MouseDown|PointerDown)\s*=\s*\{', content):
        findings.append({
            "item": "A-22", "severity": "candidate",
            "file": fname, "line": find_line(content, m.start()),
            "message": f"on{m.group(1)} handler — verify action isn't executed on down-event",
            "code": content[m.start():min(m.start()+60, len(content))]
        })
    return findings


def scan_a23_label_name(content: str, fname: str) -> list[dict]:
    """A-23: Icon buttons without accessible name."""
    findings = []
    # button with only icon/svg content and no aria-label
    for m in re.finditer(r'<button\b([^>]*?)>(.*?)</button>', content, re.IGNORECASE | re.DOTALL):
        attrs = m.group(1)
        inner = m.group(2).strip()
        has_aria = bool(re.search(r'aria-label(ledby)?\s*=', attrs, re.IGNORECASE))
        has_title = bool(re.search(r'\btitle\s*=', attrs, re.IGNORECASE))
        # Check if inner content is only icons/svg (no readable text)
        text_only = re.sub(r'<[^>]+>', '', inner).strip()
        is_icon_only = not text_only or all(ord(c) > 0x2000 for c in text_only.replace(' ', ''))
        if is_icon_only and not has_aria and not has_title and inner:
            findings.append({
                "item": "A-23", "severity": "candidate",
                "file": fname, "line": find_line(content, m.start()),
                "message": "Button appears icon-only without aria-label",
                "code": m.group(0)[:80]
            })
    return findings


def scan_a28_error_suggestion(content: str, fname: str) -> list[dict]:
    """A-28: Form validation without proper error handling."""
    findings = []
    # Forms with required fields but no aria-invalid/aria-describedby pattern
    has_required = bool(re.search(r'\brequired\b', content, re.IGNORECASE))
    has_error_handling = bool(re.search(r'aria-invalid|aria-describedby|aria-errormessage', content, re.IGNORECASE))
    if has_required and not has_error_handling:
        findings.append({
            "item": "A-28", "severity": "candidate",
            "file": fname, "line": 1,
            "message": "Form has required fields but no aria-invalid/aria-describedby error pattern",
            "code": ""
        })
    return findings


# ---------------------------------------------------------------------------
# Semantic HTML scanners
# ---------------------------------------------------------------------------

def scan_semantic(content: str, fname: str) -> list[dict]:
    """Semantic HTML checks."""
    findings = []

    # S-01: Presentational tags
    for m in re.finditer(r'<(b|i)(\s|>)', content):
        tag = m.group(1)
        replacement = "strong" if tag == "b" else "em"
        findings.append({
            "item": "S-01", "severity": "candidate",
            "file": fname, "line": find_line(content, m.start()),
            "message": f"<{tag}> tag — consider <{replacement}> for semantic meaning",
            "code": ""
        })

    # S-02: Paragraph via line breaks
    for m in re.finditer(r'<br\s*/?\s*>\s*<br\s*/?\s*>', content, re.IGNORECASE):
        findings.append({
            "item": "S-02", "severity": "candidate",
            "file": fname, "line": find_line(content, m.start()),
            "message": "Consecutive <br> tags — consider using <p> for paragraphs",
            "code": ""
        })

    # S-03: Missing landmarks (only in page/layout files)
    is_page = bool(re.search(r'(page|layout|index|app)\.(tsx|jsx|html)', fname, re.IGNORECASE))
    if is_page:
        has_main = bool(re.search(r'<main\b', content, re.IGNORECASE))
        has_header = bool(re.search(r'<header\b', content, re.IGNORECASE))
        has_nav = bool(re.search(r'<nav\b', content, re.IGNORECASE))
        if not has_main:
            findings.append({
                "item": "S-03", "severity": "candidate",
                "file": fname, "line": 1,
                "message": "Page file without <main> landmark",
                "code": ""
            })

    # S-04: Clickable div/span (covered by A-10, skip if already caught)

    return findings


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

ALL_SCANNERS = [
    scan_a01_alt_text,
    scan_a03_table,
    scan_a07_autoplay,
    scan_a10_keyboard,
    scan_a11_focus_visible,
    scan_a13_char_shortcut,
    scan_a17_skip_nav,
    scan_a18_heading,
    scan_a19_link_text,
    scan_a22_pointer_cancel,
    scan_a23_label_name,
    scan_a25_lang,
    scan_a26_change_on_request,
    scan_a28_error_suggestion,
    scan_a29_label,
    scan_a32_parsing,
    scan_a33_aria,
    scan_semantic,
]


def scan_file(filepath: str) -> list[dict]:
    content = read_file(filepath)
    if not content:
        return []
    fname = os.path.basename(filepath)
    findings = []
    for scanner in ALL_SCANNERS:
        findings.extend(scanner(content, fname))
    return findings


def main():
    parser = argparse.ArgumentParser(description="KWCAG2.2 static accessibility scanner")
    parser.add_argument("files", nargs="*", help="Files or directories to scan")
    parser.add_argument("--dir", "-d", type=str, help="Directory to scan recursively")
    args = parser.parse_args()

    paths = list(args.files or [])
    if args.dir:
        paths.append(args.dir)
    if not paths:
        print(json.dumps({"error": "No files specified"}), file=sys.stderr)
        sys.exit(1)

    files = collect_files(paths)
    if not files:
        print(json.dumps({"error": "No web files found", "paths": paths}), file=sys.stderr)
        sys.exit(1)

    all_findings = []
    for f in files:
        all_findings.extend(scan_file(f))

    # Group by item
    by_item: dict[str, list] = {}
    for f in all_findings:
        by_item.setdefault(f["item"], []).append(f)

    # Summary
    errors = [f for f in all_findings if f["severity"] == "error"]
    candidates = [f for f in all_findings if f["severity"] == "candidate"]

    output = {
        "files_scanned": files,
        "summary": {
            "total_findings": len(all_findings),
            "errors": len(errors),
            "candidates": len(candidates),
            "items_with_issues": sorted(by_item.keys())
        },
        "findings": all_findings
    }

    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
