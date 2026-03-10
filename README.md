# web-quality-reviewer

AI agent + skill set for Claude Code — comprehensive web quality audit covering 2 areas in a single run.

Claude Code용 AI 에이전트 + 스킬 세트 — 2개 영역 웹 품질 감사를 한 번의 실행으로 수행합니다.

![Claude Code](https://img.shields.io/badge/Claude_Code-required-blue)
![KWCAG 2.2](https://img.shields.io/badge/KWCAG-2.2-green)
![Coverage](https://img.shields.io/badge/coverage-2_areas_69_items-orange)

---

## 개요

`web-quality-reviewer`는 Claude Code용 AI 에이전트 및 스킬 세트로, 한 번의 실행으로 웹 품질 종합 감사를 수행합니다. 접근성과 SEO & Web Performance 2개 영역을 커버하며, 한국어로 작성된 통합 HTML 리포트와 CSV 파일을 생성합니다.

프로젝트에 `playwright.config.ts`가 존재하면, 에이전트가 자동으로 Playwright 브라우저 검사를 실행하여 명도 대비, 키보드 내비게이션, 동적 ARIA 상태 변화 등 정적 코드 분석만으로는 신뢰할 수 없는 항목들을 자동 검증합니다.

---

## 검토 영역 (2개)

| 영역                          | 항목 수     | 기준 / 범위                                                              |
| ----------------------------- | ----------- | ------------------------------------------------------------------------ |
| **A. 접근성**                 | 33 + 7 = 40 | KWCAG 2.2 (한국 웹 콘텐츠 접근성 지침 2.2, 33항목) + 시맨틱 HTML (7항목) |
| **B. SEO & Web Performance**  | 11 + 18 = 29 | Technical SEO (SEO-01~11) + Page Experience / Core Web Vitals (WP-01~18) |

**접근성 상세:**

- KWCAG 2.2: 인식의 용이성 (9항목), 운용의 용이성 (15항목), 이해의 용이성 (7항목), 견고성 (2항목)
- 항목 8 (명도 대비), 10 (키보드 접근성), 33 (동적 ARIA): Playwright 설치 시 자동 검증

**SEO & Web Performance 상세:**

- Technical SEO: noindex, title, h1, HTTPS, meta description, canonical, JSON-LD, URL 구조, DOCTYPE, charset, viewport
- Page Experience: CRP (3항목), 이미지 (3항목), JS (3항목), 폰트 (2항목), LCP (1항목), INP (3항목), CLS (3항목)

---

## 출력 결과

검토 실행 후 프로젝트에 2개의 파일이 생성됩니다:

```
your-project/
└── reports/
    └── web-quality/
        └── YYYYMMDD-HHmm/
            ├── report.html   ← 색상 구분된 2개 섹션 시각적 리포트
            └── report.csv    ← 스프레드시트용 데이터 (영역 컬럼 포함)
```

동일 분 내 재실행 시 폴더를 재사용합니다.

---

## 요구사항

- **Claude Code** — [claude.ai/code](https://claude.ai/code)
- **Claude API 키** — 에이전트 실행에 필요
- **선택사항: Playwright** — `playwright.config.ts`를 설치 및 구성하면 항목 8 (명도 대비), 10 (키보드 접근성), 33 (동적 ARIA) 자동 검사 활성화

---

## 설치 방법

`agents/`와 `skills/` 폴더를 프로젝트의 `.claude/` 디렉토리에 복사합니다:

```bash
cp -r agents/ your-project/.claude/agents/
cp -r skills/ your-project/.claude/skills/
```

설치 후 프로젝트 구조:

```
your-project/
└── .claude/
    ├── agents/
    │   └── web-quality-reviewer.md
    └── skills/
        ├── web-quality-audit/
        │   ├── SKILL.md
        │   └── references/
        │       └── output-format.md
        ├── accessibility/
        │   ├── SKILL.md
        │   └── references/
        │       ├── kwcag22.md
        │       └── output-format.md
        └── seo/
            ├── SKILL.md
            └── references/
                └── guide.md
```

---

## 사용법

프로젝트에서 Claude Code를 열고 아래의 트리거 문구 중 하나를 입력합니다:

| 트리거              | 범위               |
| ------------------- | ------------------ |
| `웹 품질 검토해줘`  | 2개 영역 전체 감사 |
| `web quality audit` | 2개 영역 전체 감사 |
| `접근성 검토해줘`   | 접근성만           |
| `a11y 체크해줘`     | 접근성만           |
| `SEO 검토해줘`      | SEO만              |
| `성능 검토해줘`     | 성능만             |

에이전트는 `git diff --name-only HEAD`로 변경된 파일을 자동 감지하여 검토 범위로 사용합니다. 변경된 파일이 없으면 검토 대상을 지정해 달라고 요청합니다.

---

## 결과 예시

`reports/` 폴더에는 실제 프로젝트 실행으로 생성된 리포트 파일이 포함되어 있습니다.

HTML 리포트 구성:

- 상단에 2개 영역별 종합 점수 카드
- 영역별 합격/불합격/권고/해당없음 배지가 포함된 상세 결과 테이블
- 실패 항목별 구체적인 수정 방법이 담긴 수정 가이드 섹션

---

## 파일 구조

```
web-quality-reviewer/
├── README.md
├── agents/
│   └── web-quality-reviewer.md          ← 에이전트 정의 (트리거, 도구, 모델)
├── skills/
│   ├── web-quality-audit/
│   │   ├── SKILL.md                     ← 오케스트레이션 스킬 (2개 서브 스킬에 위임)
│   │   └── references/
│   │       └── output-format.md         ← 통합 HTML + CSV 리포트 템플릿
│   ├── accessibility/
│   │   ├── SKILL.md                     ← KWCAG2.2 33항목 + 시맨틱 HTML 검토
│   │   └── references/
│   │       ├── kwcag22.md               ← KWCAG2.2 전체 기준 테이블
│   │       └── output-format.md         ← 접근성 단독 리포트 템플릿
│   └── seo/
│       ├── SKILL.md                     ← Technical SEO (11항목) + Page Experience (18항목)
│       └── references/
│           └── guide.md                 ← SEO + Web Performance 통합 레퍼런스
└── reports/                             ← 생성된 리포트 저장 위치
```
