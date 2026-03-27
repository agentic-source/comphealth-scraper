# Manuscript Conversion Guide

How to turn your assembled Markdown manuscript into publish-ready DOCX, PDF,
and EPUB/Kindle files.

---

## Markdown to DOCX (via Pandoc)

### 1. Install Pandoc

| Platform | Command / Instructions |
|----------|----------------------|
| macOS    | `brew install pandoc` |
| Windows  | Download the installer from [pandoc.org](https://pandoc.org) |
| Linux    | `sudo apt install pandoc` |

Verify the installation:

```bash
pandoc --version
```

### 2. Run the Conversion

```bash
pandoc assembled-manuscript.md -o manuscript.docx --toc
```

- `--toc` generates a table of contents from your headings.
- The output file `manuscript.docx` can be opened in Microsoft Word, Google
  Docs, or LibreOffice Writer.

### 3. Apply Styles in Word

Pandoc maps Markdown headings to Word heading styles, but the default
formatting is plain. After opening the DOCX:

1. **Heading styles** -- Select each chapter title and confirm it uses the
   *Heading 1* style. Sub-sections should be *Heading 2*, *Heading 3*, etc.
2. **Fonts** -- Choose a readable body font (e.g., Georgia 11pt or
   Garamond 12pt) and a complementary heading font. Apply via
   *Home > Styles > Modify*.
3. **Page breaks** -- Insert a page break before every chapter heading
   (*Insert > Page Break* or `Ctrl+Enter`). This keeps each chapter starting
   on a fresh page.

### 4. Clean Up the DOCX

- **Consistent fonts and spacing** -- Use *Find & Replace* (Format options) to
  standardise font sizes and line spacing across the entire document.
- **Remove Markdown artifacts** -- Search for stray backticks, raw HTML tags,
  or bracket-style links that Pandoc did not convert cleanly.
- **Check images** -- Make sure all images appear at the correct size and
  position; resize or re-anchor as needed.

---

## DOCX to PDF

### Option A -- Print to PDF (Recommended)

This is the simplest and most reliable approach:

1. Open `manuscript.docx` in **Microsoft Word** or **Google Docs**.
2. Go to **File > Print**.
3. Choose **Save as PDF** (or *Microsoft Print to PDF* on Windows).
4. Save the file.

Option A is recommended because it preserves exactly what you see on screen,
including fonts, spacing, and images.

### Option B -- Pandoc with a PDF Engine

If you prefer a command-line workflow:

```bash
pandoc assembled-manuscript.md -o manuscript.pdf --pdf-engine=wkhtmltopdf
```

You will need a PDF engine installed (e.g., `wkhtmltopdf`, `xelatex`, or
`weasyprint`). Install `wkhtmltopdf` with:

| Platform | Command |
|----------|---------|
| macOS    | `brew install wkhtmltopdf` |
| Windows  | Download from [wkhtmltopdf.org](https://wkhtmltopdf.org) |
| Linux    | `sudo apt install wkhtmltopdf` |

> **Tip:** For most authors, Option A (print to PDF) produces cleaner results
> with less fuss.

---

## EPUB Conversion for Kindle

### Option A -- Upload DOCX Directly to KDP (Recommended)

Amazon KDP accepts DOCX files and converts them to Kindle format
automatically. No extra conversion step is needed:

1. Log in to [kdp.amazon.com](https://kdp.amazon.com).
2. Create a new Kindle eBook.
3. In the **Manuscript** section, upload your `manuscript.docx`.
4. KDP's built-in converter handles the EPUB/Kindle format for you.

This is the simplest path and avoids potential formatting differences from
third-party conversion tools.

### Option B -- Convert with Calibre

If you want a local EPUB file (for testing, other storefronts, or archival):

1. **Download Calibre** (free, open-source) from
   [https://calibre-ebook.com](https://calibre-ebook.com).
2. Open Calibre and click **Add books** to import your `manuscript.docx`.
3. Select the book, then click **Convert books**.
4. Set the **Output format** dropdown to **EPUB**.
5. Click **OK** to start the conversion.
6. Right-click the book and choose **Open containing folder** to find the
   generated `.epub` file.

You can then upload the EPUB to KDP or any other distribution platform.

---

## KDP-Specific Formatting Tips

Follow these guidelines to pass KDP's quality checks and deliver a good
reading experience on Kindle devices:

- **Use Heading 1 for chapter titles.** KDP uses H1 headings to generate
  Kindle chapter markers and the navigable table of contents.

- **Hyperlinked table of contents is required.** KDP quality standards mandate
  a TOC with working hyperlinks. In Word, use *References > Table of Contents*
  to generate one automatically.

- **Use page breaks between chapters.** Insert proper page breaks
  (*Insert > Page Break*) rather than stacking blank lines. Blank lines render
  inconsistently across Kindle devices.

- **Avoid headers and footers.** Kindle ignores them entirely; they can cause
  unexpected rendering artifacts.

- **Images: keep under 5 MB each.** Use JPG for photographs and PNG for
  graphics with text or sharp edges. Ensure images are at least 300 DPI for
  print-quality rendering but stay within the 5 MB per-image limit.

- **Test with the KDP online previewer.** Before publishing, use the previewer
  on the KDP dashboard to check how your book looks on different Kindle
  devices, tablets, and the Kindle app. Fix any formatting issues before going
  live.
