---
name: qa-dynamic-pdf-generator
description: Set a modern, dynamic design direction for converting technical QA Markdown documents into PDFs. Use when exporting test plans, specs, or bug reports that need strong visual hierarchy, readable typography, and product-specific aesthetic judgment rather than generic default styling.
metadata:
  origin: user
---

# QA Dynamic PDF Generator

Use this skill when the work is not just converting text to a file, but making technical QA documentation feel purposeful, polished, and highly readable. 

## When to Use

- The user asks to convert QA Markdown files (test plans, test cases, technical specs, bug reports) into PDF format.
- The user asks to make a technical document more polished, distinctive, or less generic.
- The implementation needs visual hierarchy, typography, color accents, and interaction-like states (e.g., PASS/FAIL badges) applied to a static document.
- The default Markdown-to-PDF output looks flat, academic, templated, or visually fatiguing.

## Design Direction

Before converting the document, apply a specific visual direction:

1. **Typography:** Prioritize readability for long-form technical reading. Use a modern, clean sans-serif font (e.g., Inter, Roboto, or Segoe UI) with a line-height of 1.6. Use a crisp monospace font (e.g., JetBrains Mono, Fira Code) for code and technical terms, paired with a subtle background tint and rounded corners.
2. **Color Palette (Dynamic Professionalism):** Avoid a monochromatic gray/black UI. Use a deep primary accent (e.g., Indigo `#4338CA` or Ocean Teal `#0F766E`) for primary headers and borders. Use dark slate (`#1E293B`) instead of pure black for body text to reduce eye strain.
3. **Memorable detail:** Style blockquotes and notes as "Info Cards" (callouts) with a soft background, a thick colored left border, and generous padding, moving away from standard italicized academic quotes.
4. **Constraints:** The document must remain printable and readable. Contrast must be accessible. Page breaks must not orphan headers or split small tables awkwardly.

## Implementation Guidance

### Content States and QA Badges

Before rendering the PDF, identify structural QA data in the Markdown and enhance it with specific visual states:

| State / Indicator | Implementation Check |
| --- | --- |
| `[PASS]` / Success | Green background (`#DCFCE7`) with dark green bold text, styled as an inline rounded badge. |
| `[FAIL]` / Error | Red background (`#FEE2E2`) with dark red bold text, styled as an inline rounded badge. |
| `[BLOCKED]` | Yellow/Amber background with dark bold text, styled as an inline rounded badge. |
| `[IN PROGRESS]` | Soft blue background with dark blue bold text, styled as an inline rounded badge. |

### Build from the contract

- Use an HTML/CSS intermediary step (via WeasyPrint, Puppeteer, or Pandoc) or a robust Typst template to enforce the design system before generating the final PDF.
- Design tables explicitly: remove harsh vertical borders, add subtle bottom borders to rows, and apply a soft background color to the table header (`<th>`) that matches the primary accent.
- Ensure all text fits within the page margins cleanly; wrap long code strings or URLs to prevent layout overflow.
- Define CSS `@page` rules or Typst page setups to handle page margins, page numbers, and running headers consistently.

## Anti-Patterns

- Do not default to common generated patterns: standard Times New Roman, plain Arial, or unmodified browser-default typography.
- Do not use rigid, black-line spreadsheet-style gridlines for tables.
- Do not use pure `#000000` text on a pure `#FFFFFF` background for dense technical text; it causes visual fatigue.
- Do not leave standard Markdown blockquotes (`>`) unstyled; they must look like deliberate callout boxes.
- Do not allow page breaks (`page-break-inside`) to split code blocks, single test cases, or small tables across two pages.

## Review Checklist

- The document immediately communicates a modern, professional standard rather than a generic text dump.
- The visual hierarchy supports scanning (H1s and H2s are distinct, QA badges immediately draw the eye to failures or passes).
- Typography fits the page margins and does not overflow.
- Color choices have strong contrast and do not collapse into a one-note grayscale palette.
- Tables are "breathable" without vertical borders.
- Page breaks occur logically; headers are not left orphaned at the bottom of a page.

### Rendered finish gate

Inspect the rendered PDF (or the HTML preview) before final delivery. Check that the custom fonts loaded correctly, the badges have proper padding, and the margins are uniform. Fix formatting failures (like overflowing tables or broken layouts), then repeat the export. Keep the intermediate CSS or template files in the workspace so they can be reused for future QA documents.