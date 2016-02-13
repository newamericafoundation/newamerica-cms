import $ from 'jquery'

import {
  INTERVAL,
  CONTENT_ITEM_CLASS_NAME,
  NAV_CLASS_NAME,
  NAV_ITEM_CLASS_NAME,
  LEFT_ARROW_CLASS_NAME,
  RIGHT_ARROW_CLASS_NAME
} from './../constants.js'

import addNav from './add_nav.js'
import update from './update.js'

import navTemplate from './../nav.jade'


function shiftActiveItemIndex(state, step = +1) {
  state.activeItemIndex += step
  if (state.activeItemIndex >= state.itemCount) {
    state.activeItemIndex = 0
  } else if (state.activeItemIndex <= -1) {
    state.activeItemIndex = state.itemCount - 1
  }
  return state
}

export default function addBorderPanelInteractivity($this) {

  var state

  start()

  function start() {
    state = getInitialState($this)
    addNav($this, state)
    update($this, state)
    setCarouselInterval($this, state)
  }

  function getInitialState($this) {
    return {
      activeItemIndex: 0,
      itemCount: $this.find(`.${CONTENT_ITEM_CLASS_NAME}`).length,
      shouldChangeOnInterval: true
    }
  }

  function setCarouselInterval($this, state) {
    if (state.itemCount === 1) {
      return
    }
    setInterval(() => {
      if (!state.shouldChangeOnInterval) {
        state.shouldChangeOnInterval = true
        return
      }
      shiftActiveItemIndex(state, +1)
      update($this, state)
    }, INTERVAL)
  }

}
