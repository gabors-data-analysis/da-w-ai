---
name: referee
description: An independent audit of a finished empirical project. Reruns the code from scratch, checks that the outputs match, that the paper's numbers come from the outputs, and that the method supports the claims, then files a referee report. Use in a fresh session, when a project or a draft is complete.
---

# Referee

The session that built a project cannot audit it: it remembers its own reasoning and
tends to defend it. So this skill runs in a **fresh session**, as a reviewer who has
never seen the work. If you are the session that did the work, say so and stop.

**Never change the author's files.** Read them, run them, and write your own notes and
scripts under `docs/reviews/`.

## Steps

1. **Read first.** `README.md`, `AGENTS.md`, `DECISIONS.md`, then the scripts in `code/`
   in the order they run. Note what each script reads and writes.
2. **Rerun from scratch.** Copy the outputs to a temporary folder, run all scripts in
   order, and compare the new outputs with the saved ones. Report every difference.
   If a script cannot run (missing data, missing package), say exactly why.
3. **Follow the sample.** How many observations enter, and how many are left after each
   step? Is every drop explained in `DECISIONS.md`?
4. **Check the paper against the outputs.** Take the numbers in the abstract, the
   introduction and the conclusion. Find each in a table or figure, and in the output
   file behind it.
5. **Check the design.** Does the method support the claims? Look for causal words
   ("effect", "impact", "leads to") where the design shows an association. List the
   checks a sceptical reader would ask for and that are missing.
6. **Check that others can reproduce it.** Does the README say where the raw data came
   from and how to run the code? Is anything made by hand?
7. **File the report** at `docs/reviews/referee_<date>.md`: a summary; major concerns
   (must be addressed); minor concerns; questions for the author; a verdict (accept,
   minor revision, major revision); and the three things to do first.

## Develop it further

- Ask for the main result to be estimated again in a second language (R if the code is
  Python). Two independent versions rarely make the same mistake.
- Add the checks your field's referees always ask for.
- Add a second mode for slide decks or for qualitative work.

Based on `/referee2` by Scott Cunningham (MixtapeTools), shortened and adapted.
