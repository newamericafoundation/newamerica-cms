import { NAME, LOAD_ARTICLE_IMAGE, RESET_ARTICLE_IMAGES, SET_EDITION_STATUS } from './constants';

export const loadArticleImage = (image) => ({
  type: LOAD_ARTICLE_IMAGE,
  image,
  component: 'weekly.edition'
});

export const clearArticleImages = () => ({
  type: RESET_ARTICLE_IMAGES,
  component: 'weekly.edition'
});

export const setIsReady = (status) => ({
  type: SET_EDITION_STATUS,
  component: 'weekly.edition',
  isReady: status
});

export const reloadScrollEvents = () => ({
  type: 'RELOAD_SCROLL_EVENTS',
  component: 'site'
});
