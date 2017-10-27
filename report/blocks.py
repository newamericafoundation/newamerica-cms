from wagtail.wagtailcore import blocks


class EndnoteBlock(blocks.StructBlock):
    number = blocks.TextBlock()
    note = blocks.RichTextBlock()
