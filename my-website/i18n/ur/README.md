# Urdu Translation for Physical AI Book

This directory contains the Urdu translation of the Physical AI & Humanoid Robotics book.

## Directory Structure

- `docusaurus-theme-classic/` - Contains UI translations for the website theme
  - `navbar.json` - Translations for navigation bar items
  - `footer.json` - Translations for footer items

- `docs/` - Contains translations for the documentation pages
  - `introduction.md` - Urdu translation of the introduction page

- `textbook/` - Contains translations for the textbook content
  - `front-matter/` - Translations for front matter sections
  - `chapter-01/` - Translations for Chapter 1
  - `chapter-02/` - Translations for Chapter 2
  - `chapter-03/` - Translations for Chapter 3
  - `chapter-04/` - Translations for Chapter 4
  - `chapter-05/` - Translations for Chapter 5
  - `back-matter/` - Translations for back matter sections

- `content/` - Contains translations for additional content pages
  - `chapter-01/` - Translations for Chapter 1 content

## How to Add More Translations

To add translations for additional chapters or pages:

1. Create the corresponding directory structure in the i18n/ur/ directory
2. Translate the content from the English version
3. Ensure the file names match the English version
4. Add appropriate frontmatter if required

## Language Settings

Urdu (ur) has been added as a supported locale in docusaurus.config.ts with:
- Label: "اردو"
- Direction: Right-to-left (rtl)