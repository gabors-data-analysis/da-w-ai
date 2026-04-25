# Book draft — *Data Analysis with AI*

This directory holds a **draft Quarto book** built from the same source material as the website (`week*/`, `da-knowledge/`, `assignments/`, `capstone/`, `project0*/`). The website continues to be the primary public artefact; this is a parallel artefact for self-learners and for an eventual print edition.

## What's here

```
book/
├── _quarto.yml          # book project: TOC, parts, formats (HTML + PDF)
├── index.qmd            # Preface (book vision)
├── how-to-use.qmd       # How to read it; book/labs split; reflection rule
├── linear-plan.qmd      # Editorial rationale + week→chapter mapping
├── chapters/            # Chapter wrappers (one .qmd per chapter)
│   ├── 01-ai-for-coding.qmd      → includes ../../week00/index.qmd
│   ├── 02-llm-review.qmd         → includes ../../week01/index.qmd  (exemplar)
│   ├── 14-agentic-cli.qmd        → includes ../../week04/index.qmd  (exemplar)
│   ├── 31-capstone-brief.qmd     → includes ../../capstone/index.qmd (exemplar)
│   ├── … 30+ stubs that include the matching source page
│   └── A1-rights-thanks.qmd
└── labs/                # Stripped-down lab versions of the original assignments
    ├── index.qmd
    └── lab-01.qmd … lab-10.qmd  → each includes ../../assignments/assignment_NN.qmd
```

The book is structured in eight parts plus a Reference section and an appendix. See `_quarto.yml` for the full TOC and `linear-plan.qmd` for the editorial rationale.

## Build

```bash
cd book
quarto preview        # live preview, HTML
quarto render         # full HTML render → _book/
```

Web-only by design — see "Editorial decisions" below. The book project is independent of the website project at the repo root. They can be rendered separately.

## Known issues in this draft

1. **Include duplicates frontmatter and H1.** Each chapter wrapper has its own frontmatter and H1; the included source file (`week01/index.qmd` etc.) also has a frontmatter block and a hero section. In the HTML render this appears as a second title block below the chapter heading. There are three ways to clean this up; pick one before going past draft:
   - **(a) Convert sources to partials** — rename `week01/index.qmd` → `week01/_body.qmd` (Quarto skips frontmatter on partials starting with `_`) and have both the website and the book pull from the partial. Cleanest, but requires touching every source file.
   - **(b) Strip frontmatter at include time** with a small Lua filter in `_quarto.yml`.
   - **(c) Copy content** into the chapter wrappers and drop the includes. Most editorial control, most maintenance burden.
2. **Hero sections.** The `::: {.hero-section}` blocks render fine on the book pages too, since the book is web-only. They look slightly heavy at the start of every chapter; defer or trim later.
3. **Internal links** in the source files point to website paths (e.g. `da-knowledge/which-ai.html`). In the book they should point to chapter anchors. Fix-up will be a one-pass `sed` once the structure is final.
4. **Lab 9 is intentionally absent** — there is no `assignment_09.qmd` in the source.
5. **R code in some included sources.** Some weekly material has R snippets alongside Python. The book is Python-only; the next pass will trim R from the included content (or the source files themselves).

## Editorial decisions (locked for Spring 2026)

The first draft listed these as open questions. They are now locked:

- **Python only.** No R, no side-by-side. Principles transfer.
- **Claude Code as the CLI agent.** Cursor / Codex / Aider get one-paragraph mentions; the workflow is written against Claude Code.
- **Web-first.** Print edition is the print editor's problem from a frozen snapshot. We do not cripple the web version pre-emptively.
- **Yearly spring edition.** Currently *Spring 2026, 26 April 2026*. Model snapshot in [`versions.qmd`](versions.qmd). Errata between editions go in the GitHub issue tracker.
- **Econometrics: brief + redirect.** Where the book brushes against DiD/IV/etc., we cover the workflow and point readers at [*Data Analysis for Business, Economics, and Policy* (Békés & Kézdi, 2021)](https://gabors-data-analysis.com/getting-started) for the method.
- **Many short chapters** over few long ones. Prefer splitting over merging as content fleshes out.

## Relationship to the website

The website at the repo root (`_quarto.yml` there) keeps its week-by-week sidebar and is the right form for an instructor running the live course. The book here is a parallel arrangement of the same material as a single linear path. Editing source pages updates both.
