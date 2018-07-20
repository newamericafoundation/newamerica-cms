# DocxParse

The 'x' in `.docx` stands for xml. `DocxParse` takes a word document's `document.xml`, and, using [python-docx](http://python-docx.readthedocs.io/en/latest/), loops through each element, and organizes them into the appropriate Wagtail block_type.

## Word Formatting

In order for `DocxParse` to know how to split the document to match the `Report` model, the Word document must be properly formatted with the appropriate [Paragraph Style](https://support.office.com/en-us/article/customize-or-create-new-styles-in-word-d38d6e47-f6fc-48eb-a607-1eb120dec563) (as opposed to styling manually by making text bold and changing the font size)

| Paragraph Style  | Text* | Effect |
| - | - | - |
| Heading 1 | *n/a* | Signifies start of a section (which is rendered as an individual page on the website). The heading text will become the page's name and slug |
| Heading 2 | *n/a* | Signifies start of a subsection. Subsections get a heading in a report and show up in the table of contents |
| Heading 2 | "Box Start" | By writing "Box Start" and giving it an H2 style, all text beneath that heading will be grouped into a box block_type and displayed on the website as a box. **"Box Start" styles must have a corresponding "Box End" style.** |
| Heading 2 | "Box End" | All text after this point will not be grouped in a box. **Box End must have a corresponding "Box Start" style.** |
| Text Box | *n/a* | Though not a paragraph style, a text box indicates that an image, figure, or data viz will be placed here. This breaks up a paragraph block in Wagtail so that you can insert an image block without having to split a paragraph block manually |


## Overview

`document.xml` looks something like this:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<w:document ...attributes>
  <w:body>
    <w:p w14:paraId="7A4C4C5A" w14:textId="77777777" w:rsidR="00311D62" w:rsidRDefault="000E5F82" w:rsidP="009955B9">
      <w:r w:rsidRPr="006D2979">
        <w:rPr>
          <w:b/>
          <w:sz w:val="24"/>
          <w:szCs w:val="24"/>
        </w:rPr>
        <w:t>Some text</w:t>
      </w:r>
      <w:r w:rsidR="00075D5C">
        <w:t xml:space="preserve">More text</w:t>
      </w:r>
    </w:p>
    ...
  </w:body>
</w:document>
```

At the top level, Docx is made up of `<w:p>` paragraph elements that are *not* analogous to an HTML `<p>`. Each paragraph is composed of `<w:r>` "run" elements that break up the paragraph based on the formatting changes made in Word.

Inside a run, the child elements of `<w:rPr>` determine the formatting (so in the example above "Some text" would be bolded because inside the run's `<w:rPr>` element is a `<w:b/>` element). `<strong>`, `<em>`, and all heading HTML elements can be determined by what's inside the `<w:rPr>` element.

Most of the time, what we want to be an HTML paragraph or a Wagtail block spans multiple `<w:p>` elements, so this solution flattens the structure so that runs are the top level element and not `<w:p>`, then regroups the runs based on which Wagtail block_type it should be added to.

Endnotes and hyperlinks are stored in a separate xml file that can be parsed and referenced by their id.

There are a handful of additional `document.xml` elements that code for `<ul>`, `<ol>`, `<a>`, `<img>`, `<table>` HTML elements:

| Docx Element | HTML Element | Description |
| - | - | - |
| `<w:ilvl />` | `<li/>` | if this element is a descendant of a paragraph element, all runs in that paragraph should be grouped into an list HTML element |
| `<w:hyperlink/>` | `<a/>`  | hyperlinks appear at the same level as a run and are ignored by `python-docx` when looping through paragraphs. Get the id attribute from this element, then lookup url from the links xml file. |
| `<w:drawing />` | `<img/>` | if this element is a descendant of a paragraph element, the entire paragraph is a text box  |
| `<w:tbl>` | `<table />`| this appears at the same level as a paragraph and is ignored by `python-docs` |
| `<w:footnoteReference>` | citations | footnotes are separated into their own run. Get the id attribute from this element which is always the same as the citation number |
| `<w:pPr>` | `<br/>` or `<p/>` | paragraph breaks are determined by the number of `<w:pPr>` tags inside a paragraph element. `<p/>` is used if there is more than one, `<br/>` if there is just one |
