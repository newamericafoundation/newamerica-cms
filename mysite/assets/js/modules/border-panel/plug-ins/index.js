import $ from 'jquery'

import {
  INTERVAL,
  CONTENT_ITEM_CLASS_NAME,
  NAV_CLASS_NAME,
  NAV_ITEM_CLASS_NAME,
  LEFT_ARROW_CLASS_NAME,
  RIGHT_ARROW_CLASS_NAME
} from './../constants.js'

import addBorderPanelNavListeners from './add_nav_event_listeners.js'
import updateBorderPanel from './update.js'

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

$.fn.extend({

  addBorderPanelInteractivity: function() {

    var $this = $(this)

    var state = getInitialState()

    start()

    function start() {
      setup()
      addBorderPanelNavListeners($this, state)
      setCarouselInterval()
    }

    function setup() {
      state.activeItemIndex = 0
      state.itemCount = $this.find(`.${CONTENT_ITEM_CLASS_NAME}`).length
      addNav()
      updateBorderPanel($this, state)
    }

    function getInitialState() {
      return {
        activeItemIndex: 0,
        itemCount: $this.find(`.${CONTENT_ITEM_CLASS_NAME}`).length,
        shouldChangeOnInterval: true
      }
    }

    function addNav() {
      var navHtml = navTemplate({ buttonCount: state.itemCount })
      $this.prepend(navHtml)
    }

    function setCarouselInterval() {
      if (state.itemCount === 1) { return }
      setInterval(() => {
        if (!state.shouldChangeOnInterval) {
          state.shouldChangeOnInterval = true
          return
        }
        shiftActiveItemIndex(state, +1)
        updateBorderPanel($this, state)
      }, INTERVAL)
    }

  }

})
