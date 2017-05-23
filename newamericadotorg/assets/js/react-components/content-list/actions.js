import { CONTENT_LOADED, CONTENT_LOADING, CONTENT_UNLOADED, NAME } from './constants';


export const loadContent = () => {
  return {
    type: CONTENT_LOADING,
    component: NAME
  }
}

export const unloadContent = () => {
  return {
    type: CONTENT_UNLOADED,
    component: NAME
  }
}

export const contentLoaded = () => {
  return {
    type: CONTENT_LOADED,
    component: NAME
  }
}
