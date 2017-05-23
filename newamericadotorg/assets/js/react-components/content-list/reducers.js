import { CONTENT_LOADING, CONTENT_LOADED, CONTENT_UNLOADED } from './constants';

export const contentLoaded = (state='undefined', action) => {
  switch(action.type) {
    case CONTENT_LOADING:
      return false;
    case CONTENT_LOADED:
      return true;
    case CONTENT_UNLOADED:
      return 'undefined';
    default:
      return state;
  }
}
