---
name: ref-check
description: Check every reference in a paper or a reading list. Confirms that each one is a real publication with a DOI or a stable link, and that authors, title, journal, year, volume and pages belong to the same publication. Use after a literature search, whenever references were added or changed, and before a draft is sent to anyone.
---

# Reference check

A model can write a reference that looks right and does not exist, or one that mixes
two real papers. This skill checks references one at a time. It never writes a
reference from scratch, and it never overwrites the author's list.

## Steps

1. **Find the list.** A reference section in a Markdown or Word file, or a `.bib` file.
   Count the entries and tell the user the number. Above 30, ask before you go on.
2. **Check one entry at a time.** Do not skim the whole list. For each entry:
   - find its DOI, or a stable link at the publisher or a repository;
   - open the publisher's page, or look the DOI up in a registry such as Crossref;
   - compare authors, title, journal or publisher, year, volume and pages.
3. **Classify each entry.**
   - `clean`: everything matches.
   - `corrected`: the publication exists, and one or more fields were wrong. Give the
     old and the new value, and the link you used.
   - `unverifiable`: you found no trace of it. Do not guess. In a draft that an AI
     helped to write, such an entry may be invented: say so plainly.
4. **Check the text against the list.** Every citation in the text has an entry, and
   every entry is cited at least once.
5. **Check what the text says about each reference.** A reference can be real and still
   be cited for something it does not say. Compare the sentence that cites it with the
   paper's abstract, and mark it `supported`, `not supported` or `claim not checked`.
6. **Write the report** to `docs/reviews/ref-check_<date>.md`: the counts, how you
   checked (publisher's page or registry), then one line for each entry that is
   corrected, unverifiable or not supported. Add a corrected copy of the reference list
   as a new file. The author decides what goes into the paper.

## Develop it further

- For a long list, give each entry to its own subagent, so the last entries get the
  same care as the first.
- Check only the entries that changed since the last run.
- Add the reference style of your journal as a last step.

Based on `/bibcheck` from Scott Cunningham's MixtapeTools, in Gábor Békés's version.
Shortened and adapted.
