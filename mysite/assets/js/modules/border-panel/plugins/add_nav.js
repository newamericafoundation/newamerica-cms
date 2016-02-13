import $ from 'jquery'

import navTemplate from './../nav.jade'

import {
  INTERVAL,
  CONTENT_ITEM_CLASS_NAME,
  NAV_CLASS_NAME,
  NAV_ITEM_CLASS_NAME,
  LEFT_ARROW_CLASS_NAME,
  RIGHT_ARROW_CLASS_NAME
} from './../constants.js'

import updateBorderPanel from './update.js'

function shiftActiveItemIndex(state, step = +1) {
  state.activeItemIndex += step
  if (state.activeItemIndex >= state.itemCount) {
    state.activeItemIndex = 0
  } else if (state.activeItemIndex <= -1) {
    state.activeItemIndex = state.itemCount - 1
  }
  return state
}

function addNavMarkup($this, state) {
  var navHtml = navTemplate({ buttonCount: state.itemCount })
  $this.prepend(navHtml)
}

function addNavEventListeners($this, state) {
  $this.find(`.${NAV_CLASS_NAME}`).click((e) => {
    var $target = $(e.target)
    state.shouldChangeOnInterval = false
    if (!$target.hasClass(NAV_ITEM_CLASS_NAME)) {
      return
    }
    var index = $target.index()
    if (state.activeItemIndex !== index) {
      state.activeItemIndex = index
      updateBorderPanel($this, state)
    }
  })

  $this.find(`.${LEFT_ARROW_CLASS_NAME}`).click((e) => {
    shiftActiveItemIndex(state, -1)
    state.shouldChangeOnInterval = false
    updateBorderPanel($this, state)
  })

  $this.find(`.${RIGHT_ARROW_CLASS_NAME}`).click((e) => {
    shiftActiveItemIndex(state, +1)
    state.shouldChangeOnInterval = false
    updateBorderPanel($this, state)
  })
}

export default function addNav($this, state) {
  addNavMarkup($this, state)
  addNavEventListeners($this, state)
}
