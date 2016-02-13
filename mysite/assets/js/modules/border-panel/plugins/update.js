import $ from 'jquery'

import {
  INTERVAL,
  CONTENT_ITEM_CLASS_NAME,
  NAV_CLASS_NAME,
  NAV_ITEM_CLASS_NAME,
  LEFT_ARROW_CLASS_NAME,
  RIGHT_ARROW_CLASS_NAME
} from './../constants.js'

export default function update($this, state) {
    var width = $this.width()
    $this.find(`.${CONTENT_ITEM_CLASS_NAME}`).each((i, el) => {
      var $el = $(el)
      var xTransform = (i - state.activeItemIndex) * width
      $el.addTransformStyle(`translate(${xTransform}px, 0)`)
      $el.setModifierClass('active', (i === state.activeItemIndex), CONTENT_ITEM_CLASS_NAME)
    })
    $this.find(`.${NAV_ITEM_CLASS_NAME}`).each((i, el) => {
      $(el).setModifierClass('active', (i === state.activeItemIndex), NAV_ITEM_CLASS_NAME)
    })
  }
