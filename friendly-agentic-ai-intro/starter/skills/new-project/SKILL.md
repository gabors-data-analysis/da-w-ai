---
name: new-project
description: Set up a new research project folder with a standard structure, a README, a status note and an empty decision log. Use at the start of every new project, before any data, code or text is added.
---

# New project

A project that starts with a clear structure is easier to check later, by the researcher
and by the agent. This skill sets it up the same way every time.

## Steps

1. **Name.** If the user gave no project name, ask for one. If they are away, take it
   from the research question and say which name you chose. Use lowercase and hyphens,
   no spaces or accents.
2. **Folders.** Create these in the current project folder. Do not touch files that are
   already there.
   - `data/raw/` original data, never edited
   - `data/clean/` cleaned data, produced by code
   - `code/` scripts, numbered in the order they run
   - `output/figures/` and `output/tables/`
   - `docs/readings/` papers as PDFs; `docs/` notes and drafts
   - `docs/reviews/` reports written by the review skills
   - `paper/` and `slides/` the final outputs
3. **Rules.** If the folder has no `AGENTS.md`, say so and ask the user where their own
   `AGENTS.md` is, so you can copy it. Do not write rules for them. If they are away,
   go on without one and note it in `status.md`.
4. **README.md.** Project title, the research question in one paragraph, the folder tree
   with one line per folder, and four empty sections: *Status*, *Data sources* (where
   from, and the download date), *Software* (programs and package versions) and
   *How to reproduce* (the scripts, in the order they run).
5. **status.md.** Today's date, what was set up, and the next steps as a checklist.
6. **DECISIONS.md.** An empty log with its header (see the `decision-log` skill).
7. **Report.** Show the folder tree and tell the user what to fill in first: the
   question in the README.

## Develop it further

- Add the folders your field needs: `transcripts/`, `codebooks/`, `ethics/`.
- Add a section to the README template that your funder or journal asks for.

Based on `/newproject` by Scott Cunningham (MixtapeTools), shortened and adapted.
