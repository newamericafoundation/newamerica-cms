from wagtail import blocks

class CtaBlock(blocks.StructBlock):
  title = blocks.CharBlock(required=False, max_length=50)
  description = blocks.TextBlock(required=False, max_length=200)
  link_text = blocks.CharBlock(required=False, max_length=200)
  link_url = blocks.CharBlock(required=False, max_length=200)