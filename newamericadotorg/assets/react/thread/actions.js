import { NAME, LOAD_ARTICLE_IMAGE, RESET_ARTICLE_IMAGES, SET_EDITION_STATUS, SET_MENU_STATE } from './constants';

export const loadArticleImage = (image) => ({
  type: LOAD_ARTICLE_IMAGE,
  image,
  component: 'thread.edition'
});

export const clearArticleImages = () => ({
  type: RESET_ARTICLE_IMAGES,
  component: 'thread.edition'
});

export const setIsReady = (status) => ({
  type: SET_EDITION_STATUS,
  component: 'thread.edition',
  isReady: status
});

export const reloadScrollEvents = () => ({
  type: 'RELOAD_SCROLL_EVENTS',
  component: 'site'
});

export const setMenuState = (state) => ({
  type: SET_MENU_STATE,
  component: 'thread.edition',
  state
});
