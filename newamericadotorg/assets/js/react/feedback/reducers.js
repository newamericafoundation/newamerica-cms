import { SET_FEEDBACK, SET_FEEDBACK_TYPE, SET_FEEDBACK_MESSAGE, SET_FEEDBACK_LEVEL, SET_FEEDBACK_EMAIL, RESET_FEEDBACK } from './constants';
import cache from '../cache';

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

export const message = (state=null, action) => {
  switch(action.type){
    case SET_FEEDBACK_MESSAGE:
      return action.message;
    case RESET_FEEDBACK:
      return null;
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

export const email = (state=cache.get('feedback_email') || '', action) => {
  switch(action.type){
    case SET_FEEDBACK_EMAIL:
      cache.set('feedback_email', action.email, new Date().getTime() + 1800000)
      return action.email;
    default:
      return state;
  }
}
