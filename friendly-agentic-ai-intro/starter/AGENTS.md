# Instructions for the AI agent in this project

The agent reads this file at the start of every session. Edit it freely.
When the agent makes the same mistake twice, add a line here.

## About me

- I am a social scientist (EDIT: field, e.g. sociology, political science, economics).
- I have used AI as a chatbot, mostly for text. I have not written code before.
- Explain what you do in plain language. The first time you use a technical term,
  give a one-line definition.
- Use Python for code, unless I ask for R or Stata.

## How to work with me

- For any task with more than a few steps, first show me a short plan and wait for my OK.
- Do the smallest thing that answers my request. Ask before adding extras.
- Work in small steps. Stop at natural break points and tell me what you did and what is left.
- If my request is unclear, ask one question rather than guessing.
- When you finish, say what you did not do or could not check.
- Keep `status.md` up to date: what is done, what is open, what comes next.
  Update it at the end of each task. When I say "continue", read it first.

## Safety with my files

- Never delete files. If something should go, move it to `_old/` and tell me.
- Never change anything in `data/raw/`. Raw data stays as it arrived.
- Never overwrite a Word, Excel or PDF file I gave you. Save your changes as a new
  file with `_v2` (or the next number) at the end of the name.
- Install Python packages only inside this project's environment (`.venv`).
  Ask before installing anything for the whole computer.
- Do not upload my files or data to any website or online service.

## Data and numbers

- Never make up numbers, references, quotes or sources. If you cannot verify something, say so.
- When you report a number, say where it comes from (which file, which script, which web page).
- Check your own results: count rows before and after each step, and compare a few
  values by hand with the source.
- Log analytical choices in `DECISIONS.md` (see the `decision-log` skill).

## Folders and files

- `data/raw/` original data, never edited
- `data/clean/` cleaned data, produced by code
- `code/` scripts, numbered in the order they run: `01_get_data.py`, `02_clean.py`, ...
- `output/` figures (PNG) and tables
- `docs/` notes, memos and drafts. Write new text in Markdown (`.md`);
  convert to Word only when I ask.
- Every result must be reproducible: running the scripts in order rebuilds all outputs.

## Writing

- Plain, direct prose. Short sentences. No hype words (delve, crucial, landscape,
  comprehensive, shed light on).
- Say what the data shows, then the caveats. Talk about associations, not effects,
  unless the design allows a causal reading.

## PDFs

- To read a PDF, first extract its text to a `.txt` file, then work from the text
  (see the `read-pdf` skill).
