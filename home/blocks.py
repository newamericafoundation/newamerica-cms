from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from newamericadotorg.blocks import IntegerBlock, ButtonBlock, IframeBlock, CustomImageBlock, DatavizBlock
from in_depth.blocks import CollapsibleBlock


class ExternalLeadStoryBlock(blocks.StructBlock):
    link = blocks.URLBlock()
    image = ImageChooserBlock()
    image_alt = blocks.CharBlock(required=False)
    heading = blocks.CharBlock()
    description = blocks.CharBlock(required=False)
    tag = blocks.CharBlock(required=False)

    class Meta:
        icon = "link"
