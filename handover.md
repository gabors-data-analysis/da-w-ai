# Handover — Course reorganization to 6×200-min weeks

## Goal

Reorganize "Doing Data Analysis with AI" so the teaching unit is a **200-minute week**, matching the capstone format that worked well. This is an **8-unit course** (no skipping).

Three taught parts + capstone:
- **A — LLMs & Setup** (1 unit) — the only front-facing/lecture-heavy part
- **B — Core data analysis with AI** (2 units)
- **C — Research with AI** (2 units)
- **D — Capstone** (3 sessions, unchanged)

## Session shapes

Taught units use flexible chunking, not a fixed shape:
- Lecture-heavy units (A, C-econometrics): **50·50·50·50**
- Applied units (B1, B2, C-text): **50·100·50**
- Capstone: **30·120·50** (unchanged)

Every taught unit keeps the capstone delivery rhythm: task block + **Sunday 23:55** hand-in.

## NEW global requirement — before-class checklist

**Every unit** (including capstone sessions) gets a **"Before you come to class" checklist (30-60 min)** at the top. Mix of:
- Tech setup (accounts, installs, API keys, repo cloned)
- Short readings (link Knowledge Base pages)
- Key-term review (link glossary)

Per-unit checklist contents are specified in each unit below.

## NEW global requirement — every hands-on block has a deliverable

Every task/hands-on block in every unit must end in a concrete deliverable handed in by **Sunday 23:55** (repo, report, dataset, memo, or working environment). Specified per unit below.

## NEW global requirement — UI redesign

The unit pages need a redesigned UI (not just content moves). Rework the page layout/templates so the new structure reads cleanly — before-class checklist block, chunked session timeline, task cards, and a delivery block — consistent across all 8 units. Touch `custom.scss` and the `.qmd` page scaffolding.

---

## Final structure (8 units)

| # | Part | Unit | Shape | Built from |
|---|---|---|---|---|
| 1 | A | LLMs, models & harnesses + setup | 50·50·50·50 | week01, week03/04 setup, `which-ai`, `install-cli`, `vscode-setup` |
| 2 | B | From raw data to report | 50·100·50 | week03 + week06 |
| 3 | B | Data wrangling & debugging (review AI's work) | 50·100·50 | week02 + week05 |
| 4 | C | Econometrics with AI | 50·50·50·50 | week09 + week10 (+ DiD) |
| 5 | C | Text as data | 50·100·50 | week07 + week08 + `week05-to-add` |
| 6 | D | Capstone S1 — Data collection | 30·120·50 | unchanged |
| 7 | D | Capstone S2 — Text → expectations | 30·120·50 | unchanged |
| 8 | D | Capstone S3 — DiD + presentation | 30·120·50 | unchanged |

**Every hands-on/task block produces a deliverable** handed in by Sunday 23:55 (see per-unit specs).

---

## Unit specs

### Unit 1 — A · LLMs, models & harnesses + setup
Shape **50·50·50·50**. Only lecture-heavy unit.
- **Before class (30-60):** complete setup (accounts, installs) + read `which-ai`. That's enough.
- **Chunk 1 (50):** LLM basics, context windows, prompting (condensed week01); closed frontier vs **open-weights** models (Llama, Qwen, Mistral, DeepSeek) — capability/cost/privacy.
- **Chunk 2 (50):** what a harness is; the two course harnesses — **Claude Code** (terminal + desktop), **VS Code + GitHub Copilot** (any model); where **open-code tools** fit + open-weights/local models.
- **Chunk 3 (50):** hands-on — install/auth Claude Code terminal, then desktop app.
- **Chunk 4 (50):** hands-on — VS Code + Copilot, switch backing model; stretch: open-code tool / local open-weights model on a tiny task.
- **Delivery:** working environment + note on chosen setup and why.
- **NEW content:** open-weights/local-models reference page; open-code-tools page. Trim `which-ai`/`install-cli`/`vscode-setup` to just the two harnesses.

### Unit 2 — B · From raw data to report
Shape **50·100·50**.
- **Before class (30-60):** confirm Claude Code + VS Code working; download provided dataset; read prompting-for-data tips; review terms: tidy data, join, aggregate.
- **Intro (50):** get→explore→clean→create-vars→join→aggregate→report pipeline; prompting tips; what a good first report looks like.
- **Task (100, indiv/team):** run full pipeline on provided dataset → short report.
- **Discussion (50):** what AI got wrong, where to steer, reproducibility.
- **Deliverable:** the short report (notebook or HTML) + the pipeline script.
- **Source:** week03 + week06.

### Unit 3 — B · Data wrangling & debugging (review AI's work)
Shape **50·100·50**. **Keep skills + `agents.md` here.**
- **Before class (30-60):** clone provided repo; skim `designing-projects` + `reproducible-research`; review terms: `agents.md`, skills, the three kinds of tests.
- **Intro (50):** reviewing/debugging AI-written code; `agents.md` project files; skills; three kinds of tests; documentation (`README`/`DATA.md`); reproducibility.
- **Task (100):** messy data + AI-generated code → find/fix bugs, add `agents.md`, write tests, document.
- **Discussion (50):** silent failures, what tests caught, effect of `agents.md`/skills.
- **Deliverable:** fixed repo with `agents.md`, passing tests, and `README`/`DATA.md`.
- **Source:** week02 + week05 + `designing-projects`, `reproducible-research`.

### Unit 4 — C · Econometrics with AI
Shape **50·50·50·50**. **Recap moved to prep. DiD added. Overlap with capstone OK.**
- **Before class (30-60):** read the causality recap (the old in-class recap content moves here); review terms: confounder, backdoor path, control, instrument, exclusion restriction, DiD, parallel trends.
- **Chunk 1 (50):** AI-as-research-companion mindset; quick framing (no full recap — it's prep now).
- **Chunk 2 (50):** designing controls (Z) — week09.
- **Chunk 3 (50):** instrumental variables — 2-step approach, why not to tell the AI you're hunting IVs — week10.
- **Chunk 4 (50):** difference-in-differences with AI (parallel trends, event-study) — **NEW; overlaps capstone S3 intentionally**; + work-together: find controls/IV/DiD design for a given RQ.
- **Deliverable:** a one-page identification memo for the given RQ — proposed controls/IV/DiD design with assumptions stated.
- **Source:** week09 + week10 + new DiD material.

### Unit 5 — C · Text as data
Shape **50·100·50**.
- **Before class (30-60):** set up LLM API key (read `get-ai-api-key`); read `nlp-basics`; review terms: token, lexicon, classification, sentiment.
- **Intro (50):** text→tabular data; humans vs AI; lexicon vs ML vs LLM-via-API; sentiment.
- **Task (100):** build text→data pipeline (football-interview sentiment running case), classify via API.
- **Discussion (50):** validation, prompt reproducibility, disagreement across approaches.
- **Deliverable:** the text→data pipeline + resulting scored dataset + the reusable prompt.
- **Source:** week07 + week08 + sentiment material in `week05-to-add/`.

### Units 6-8 — D · Capstone (unchanged content)
- Still add a **before-class checklist** to each session (`capstone/index.qmd` is the overview; checklists go on `project01-03`):
  - **S1:** team formed, country picked, repo created, data-source scouting done; review terms: primary key, schema.
  - **S2:** API keys working, corpus source identified; review: rate limits, scraping etiquette.
  - **S3:** dataset frozen, expectation scores ready; review: DiD, parallel trends, event-study.

---

## Loose ends
- `week05-to-add/` → folds into Unit 5; then delete the folder.
- `week11/` (empty) → delete.
- `week00/` (already retired/redirect) → confirm can be removed or left as redirect.
- Naming: decide at build time — rename `weekNN/` → `unitNN/` (and `partA-…`?) OR keep folder names, change titles only. Lower-risk option: keep folders, change titles + sidebar.
- `_quarto.yml` sidebar/navbar: regroup into Part A / B / C / Capstone.

---

## TODO (ordered)

1. [ ] **Decide folder naming** (rename vs keep-and-retitle) — affects every later step. Recommend keep-and-retitle to avoid breaking links.
2. [ ] **Redesign the unit-page UI** — build the shared layout/template (before-class checklist block, chunked timeline, task cards, delivery block) in `custom.scss` + a `.qmd` scaffold; apply to all 8 units.
3. [ ] **Write 2 new Knowledge Base pages:** open-weights/local models; open-code tools.
4. [ ] **Unit 1** — consolidate week01 + setup pages into the 50·50·50·50 unit; before-class = setup + `which-ai`; trim harness coverage to Claude Code + Copilot.
5. [ ] **Unit 2** — merge week03 + week06 into "raw data to report"; add before-class checklist + deliverable.
6. [ ] **Unit 3** — merge week02 + week05 into "wrangling & debugging"; keep skills + `agents.md`; add before-class checklist + deliverable.
7. [ ] **Unit 4** — combine week09 + week10; move recap to prep; **write new DiD chunk**; add before-class checklist + identification-memo deliverable.
8. [ ] **Unit 5** — merge week07 + week08 + fold in `week05-to-add` sentiment; add before-class checklist + deliverable.
9. [ ] **Capstone** — add before-class checklists to `project01-03` (content otherwise unchanged).
10. [ ] **Clean up** — delete `week05-to-add/`, `week11/`; resolve `week00/`.
11. [ ] **Update `_quarto.yml`** — regroup sidebar into Part A/B/C/Capstone; update navbar.
12. [ ] **Update `CLAUDE.md`** — reflect new unit structure (it currently describes week00-week12).
13. [ ] **`quarto render`** — verify build, fix broken internal links.

## Open decisions for Gábor
- Folder rename vs keep-and-retitle (TODO #1).
- UI direction — any look/layout preferences for the redesign (TODO #2), or build a proposal first?
