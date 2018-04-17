import { LOAD_ARTICLE_IMAGE, RESET_ARTICLE_IMAGES, SET_EDITION_STATUS, SET_MENU_STATE } from './constants';

export const articleImages = (state=[], action) => {
  switch(action.type){
    case LOAD_ARTICLE_IMAGE:
      return [...state, action.image];
    case RESET_ARTICLE_IMAGES:
      return [];
    default:
      return state;
  }
}

export const isReady = (state=false, action) => {
  switch(action.type){
    case SET_EDITION_STATUS:
      return action.isReady;
    default:
      return state;
  }
}

export const menuIsOpen = (state=false, action) => {

  switch(action.type){
    case SET_MENU_STATE:
      return action.state;
    default:
      return state;
  }
}
