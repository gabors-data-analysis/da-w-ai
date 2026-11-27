---
name: blindspot
description: A fresh look at results (a table, a figure, a set of estimates) before they are interpreted. Finds problems hiding in plain sight and opportunities that are being overlooked. Use when output exists and the writing is about to start.
---

# Blindspot

When we have a main finding, we stop seeing the rest of the output: the odd spike, the
sample that shrinks between two columns, the subgroup nobody looked at. This skill
looks at the output as a stranger would. It does not check the code. That is the job
of the `referee` skill.

## Steps

1. **List before you interpret.** Write down every visible feature of the output: each
   estimate and its sign, each spike or break, each sample size, each pattern across
   columns. The main finding is one item on the list.
2. **Go through four questions**, in this order.
   - **What is there that the story doesn't explain?** For each feature, ask what could
     produce it. Start with the dull explanations: rounding, a sample restriction,
     measurement, small numbers. Name the feature that is hardest to explain.
   - **What should be there and isn't?** A check a sceptical reader would ask for.
     A subgroup or a period that was never shown. Observations dropped without comment.
     A sample size that changes without a reason.
   - **Is there a more interesting result than the one reported?** Differences across
     groups, signs of a mechanism, a pattern in the descriptive statistics.
   - **Is a strength being undersold?** A simple test that would answer the main
     objection. A figure that would make the case better than a table.
3. **Mark each finding** DONE (explained) or FLAG (no clean explanation yet). For each
   FLAG, name the cheapest check that could settle it.
4. **Write the report** to `docs/reviews/blindspot_<date>.md`: the four questions with
   their findings, then one ruling.
   - CLEAR: go on to interpretation.
   - CONDITIONAL: go on, and state the open questions in the text.
   - HOLD: do not interpret until the flagged problems are resolved.
5. **Close the flags.** When the author has acted, add one line under each FLAG: settled
   by which check, or still open. Mentioning a problem in the paper does not settle it.
   A flag that is still open goes to the `referee` as a question.

Change no files other than the report.

## Develop it further

- Add the checks your field always asks for (attrition, interviewer effects, coder
  agreement, pre-trends).
- Add a fifth question that fits your kind of evidence.

Based on `/blindspot` by Scott Cunningham (MixtapeTools), which was inspired by Jason
Fletcher's habit of "owning all the numbers". Shortened and adapted.
