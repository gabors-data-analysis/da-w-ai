---
name: paper-check
description: A short consistency check of a draft before anyone else reads it. Finds places where the paper contradicts itself or its own tables and figures, such as numbers that differ between sections, numbers that are not in the exhibit they cite, missing references and leftover placeholders. Use on every version of a paper, memo or slide deck before it is sent or shared.
---

# Paper check

This check answers one question: does the document contradict itself, or the tables and
figures it points to? It does not judge the research. That is the job of the `referee`
skill.

Read the whole document once before you flag anything. Many findings are of the kind
"the abstract and Section 4 disagree", and you only see those with the whole text in view.

## The checks

1. **Repeated numbers.** List every headline number and each place it appears:
   abstract, introduction, results, conclusion, slides. The values must agree.
2. **Text against exhibits.** Every number quoted in the text appears in the table or
   figure it cites, at the precision printed there.
3. **References inside the document.** Every table and figure is mentioned in the text,
   and every mention points to an exhibit that exists. Every citation has an entry in
   the reference list.
4. **Signs, units and wording.** Higher or lower, percent or percentage points. Does the
   text say "effect" where the design shows an association?
5. **Leftovers.** `TODO`, `??`, `XXX`, empty brackets, a note to self.

## How to report

- Check each finding against the source before you write it down. A wrong flag costs
  more trust than the slip it claims to catch.
- If you cannot trace a number, write "not traced", not "wrong".
- Number the findings P1, P2, ... and give the place of each. Fix nothing. The author
  answers by number.
- Write the report to `docs/reviews/paper-check_<date>.md`, and end it with what you
  did not check.

## Develop it further

- Add a language check against a description of your own writing style.
- Add the rules of your journal: word limits, the abstract's structure, how to report
  estimates.
- Check only what changed since the last version.

Based on the `paper-check` and `consistency-check` skills of Gábor Békés. Shortened.
