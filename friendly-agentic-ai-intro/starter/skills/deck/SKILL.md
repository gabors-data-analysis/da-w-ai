---
name: deck
description: Turn a paper, a memo or a set of results into a slide deck that an audience can follow. One idea per slide, titles that state the point, figures before tables. Use when the user asks for slides, a talk or a presentation.
---

# Deck

A deck is not a short version of the paper. It is made for a room: one idea at a time,
shown and not read out.

## Before any slide

Ask the user three things, unless they already said:

1. Who is the audience, and how long is the talk?
2. What is the one sentence the audience should remember?
3. Which format: PowerPoint or PDF?

## Steps

1. **Outline first.** Write `slides/outline.md`: one line per slide, which is the
   slide's title. Show it to the user and wait for their OK.
2. **Build the slides** from the outline, with these rules.
   - **One idea per slide.**
   - **Titles state the point.** "Turnout rose by five points among first-time voters", not "Results".
   - **No walls of text.** A few short lines, or one figure, or one small table.
   - **A figure before a table.** If a table is needed, show only the rows that the
     argument uses.
   - **Open with the question** or a concrete example, not with an outline slide.
   - **The main result comes early**, within the first third.
   - **End on the one sentence** to remember, not on "Thank you".
3. **Take every number from the project's outputs**, never from memory. The deck and the
   paper must agree.
4. **Look at the result.** Turn each slide into an image and look at it: does any text
   run off the slide, overlap, or get too small to read? Fix it and look again.
5. **Report**: the number of slides, the file, and anything in the paper that the deck
   leaves out.

## Develop it further

- Add your university's template, or your own colours and fonts.
- Add rules for different audiences: a seminar, a lecture, a policy briefing.
- Add speaker notes for each slide.

Based on `/beautiful_deck` and the "Rhetoric of Decks" by Scott Cunningham
(MixtapeTools). Shortened and adapted.
