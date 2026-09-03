# PDF Publication Style

All project PDFs use a LaTeX-inspired serif hierarchy based on the supplied reference `.tex` files. Those files do not load a custom font package, so conventional LaTeX resolves their body and headings to Computer Modern-style serif faces.

This project uses **Latin Modern Roman** for regular text, bold text, italic text, tables, diagrams, headers, and footers. Latin Modern is a maintained extension of Computer Modern and provides the closest reproducible match for the existing ReportLab publication workflow. The PDF exporter embeds the selected fonts so readers do not need them installed. The files come from the official [CTAN Latin Modern package](https://www.ctan.org/pkg/lm).

| Publication role | Font face | Reference behavior |
|---|---|---|
| Body, tables, captions | Latin Modern Roman 10 Regular | LaTeX roman body text |
| Titles and headings | Latin Modern Roman 10 Bold Extended | `\bfseries` headings |
| Emphasis | Latin Modern Roman 10 Italic | `\itshape` / `\emph` |
| Bold emphasis | Latin Modern Roman 10 Bold Extended Oblique | Combined bold and italic |

The existing navy/teal visual system remains in place. Font size, leading, hierarchy, table rules, restrained color, page headers, and page numbering follow the presentation logic visible in the reference documents.

Source fonts are stored under `assets/fonts/latin-modern/`. They are distributed under the GUST Font License included in that directory. The optional exporter fails if the font files are absent rather than silently falling back to another typeface.

Future PDF reports, analyses, memoranda, design summaries, and appendices in this repository must use these registered font faces or a LaTeX pipeline that renders an equivalent Computer Modern/Latin Modern hierarchy. A different typeface requires an explicit owner-directed style revision.
