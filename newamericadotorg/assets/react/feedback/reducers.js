import { SET_FEEDBACK, SET_FEEDBACK_TYPE, SET_FEEDBACK_MESSAGE, SET_FEEDBACK_LEVEL, SET_FEEDBACK_EMAIL, RESET_FEEDBACK } from './constants';
import cache from '../cache';
import bowser from 'bowser';

const _browser = bowser.getParser(window.navigator.userAgent);
const browserInfo = _browser.parse().parsedResult;

export const type = (state=null, action) => {
  switch(action.type){
    case SET_FEEDBACK_TYPE:
      return action.feedback_type;
    case RESET_FEEDBACK:
      return null;
    default:
      return state;
  }
}

export const message = (state='', action) => {
  switch(action.type){
    case SET_FEEDBACK_MESSAGE:
      return action.message;
    case RESET_FEEDBACK:
      return '';
    default:
      return state;
  }
}

export const level = (state='sitewide', action) => {
  switch(action.type){
    case SET_FEEDBACK_LEVEL:
      return action.level;
    case RESET_FEEDBACK:
      return 'sitewide';
    default:
      return state;
  }
}

export const username = (state='') => {
  return window.user.username;
}

export const page = (state='') => {
  return location.href;
}

export const browser = (state='') => {
  return `${browserInfo.browser.name} ${browserInfo.browser.version}`;
}

export const os = (state) => {
  return `${browserInfo.os.name} ${browserInfo.os.version}`;
}
