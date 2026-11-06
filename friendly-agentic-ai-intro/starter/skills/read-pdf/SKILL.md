---
name: read-pdf
description: Read a PDF (paper, report, book chapter, questionnaire, codebook) reliably by first extracting its text into a .txt file and then working from that text. Use whenever the user asks to read, summarize, quote, compare or extract information or tables from a PDF.
---

# Read a PDF: text first

Reading a PDF directly is unreliable: long files get cut, columns get mixed up, and the
agent may answer from a partial view without saying so. So we always extract the text
first, save it, and work from the saved text.

## Steps

1. **Extract the text.** Use the Python package `pymupdf` in this project's environment
   (install it with the project's package manager if missing). Save the text next to the
   PDF with the same name and a `.txt` ending, for example `paper.pdf` -> `paper.txt`.
   Mark each page with a line like `=== page 7 ===` so page numbers can be cited.
2. **Check the extraction.** Report the number of pages and the number of characters.
   If a page has almost no text (under ~200 characters), it is probably a scanned image.
   For those pages, render them to PNG (150 dpi is enough) and read the images.
   Tell the user which pages were read as images.
3. **Work from the `.txt` file**, not the PDF. For long documents (more than ~40 pages),
   read it section by section rather than all at once.
4. **Cite page numbers** for every claim, number or quote taken from the document.
   Quote exactly; never paraphrase inside quotation marks.
5. **Tables:** when the user needs a table, copy it into a CSV in `data/raw/` and then
   check three numbers from the CSV against the page image.

## What to tell the user at the end

- what was extracted (pages, characters, any pages read as images)
- where the `.txt` file is
- anything that could not be read well (garbled tables, formulas, footnotes)
