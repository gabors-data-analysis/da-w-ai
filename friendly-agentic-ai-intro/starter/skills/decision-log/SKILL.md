---
name: decision-log
description: Keep a DECISIONS.md log of the analytical choices made during data work (which observations to keep, how a variable is defined, which method, which chart), so the researcher can review the reasoning before trusting results. Use whenever cleaning data, building a sample, defining variables, choosing a method or designing a table or figure, even if the user does not mention it. Also use when the user asks "what did you decide?" or "review the decisions".
---

# Decision log

Every result rests on judgment calls the reader never sees. The researcher needs to
check those calls *before* looking at results. This skill keeps them in one file,
`DECISIONS.md` in the project folder, written as the decisions are made.

## What to log

Log a decision when a reasonable analyst could have chosen differently AND the choice
could change the results or how we read them. Examples:

- dropping observations (missing values, outliers, small groups, a year or a country)
- defining a variable (what counts as "employed", income in levels or logs, which year's prices)
- merging tables (which key, what to do with rows that do not match)
- choosing a method (mean or median, which regression, which controls)
- designing an exhibit (what goes in the main chart, what is left out)

Do not log mechanical steps with no real alternative, or formatting.

## Format

Create `DECISIONS.md` on first use. Keep a summary table on top and a short entry for each
decision below it. Number entries D1, D2, ... and never renumber or delete them.

```markdown
# Decision log

| ID | Date | Decision | Basis | Status |
|----|------|----------|-------|--------|
| D1 | 2026-11-06 | Drop respondents younger than 18 | user | decided |

## D1 - Drop respondents younger than 18
- **Decision point:** The survey includes 16-17 year olds; the question is about adult voters.
- **Chosen:** Keep age 18 and above (drops 412 of 9,870 rows).
- **Alternatives:** keep all (rejected: they cannot vote); keep 16+ (only where voting age is 16).
- **Basis:** user instruction, 2026-11-06.
- **Affects:** all tables and figures. Easy to reverse.
```

The **Basis** field matters most. Be honest about it:

- `evidence` a check was run (name the file or the numbers)
- `convention` common practice in the field (name the source)
- `user` the researcher asked for it (give the date)
- `default` chosen for convenience, not tested. This label is the most useful one for the
  reviewer, because it shows where to look first.

**Status** is `decided`, `provisional` (to make progress, revisit later) or `needs-review`.

## How to work

1. Write the entry when the decision is made, not at the end.
2. If a decision drops a lot of data, changes the main finding, or is hard to undo,
   mark it `needs-review` and tell the user in plain words before going on.
3. If a decision is reversed, add a new entry and mark the old one `superseded by Dn`.
4. When the user asks to review the log, list first the `default` and `provisional`
   decisions that many results depend on.
