import './index.scss';

const NAME = 'feedback';
const ID = 'feedback';

import { SET_FEEDBACK, SET_FEEDBACK_TYPE, SET_FEEDBACK_MESSAGE, SET_FEEDBACK_LEVEL, SET_FEEDBACK_EMAIL, RESET_FEEDBACK  } from './constants';
import { Text, TextArea } from '../components/Inputs';
import { connect } from 'react-redux';
import React, { Component } from 'react';
import cache from '../cache';
import { PlusX } from '../components/Icons';
import * as REDUCERS from './reducers';

class APP extends Component {
  state = {
    isOpen: false,
    isSubmitting: false
  }
  setType = (type) => {
    this.props.dispatch({
      type: SET_FEEDBACK_TYPE,
      feedback_type: type,
      component: NAME
    });
  }

  setMessage = (message) => {
    this.props.dispatch({
      type: SET_FEEDBACK_MESSAGE,
      message,
      component: NAME
    });
  }

  setLevel = (level) => {
    this.props.dispatch({
      type: SET_FEEDBACK_LEVEL,
      level,
      component: NAME
    });
  }

  setEmail = (email) => {
    this.props.dispatch({
      type: SET_FEEDBACK_EMAIL,
      email,
      component: NAME
    });
  }

  submit = () => {
    if(this.state.isSubmitting) return false;
    let { username, level, message, type, browser, os, page } = this.props;
    let props = { username, level, message, type, browser, os, page};
    let url = new URL('https://script.google.com/macros/s/AKfycbzayhkZNORzDqeMyRQgEXsc1_OAU6i4yU8DuxShl_900U71iI4/exec');
    for(let k in props)
      url.searchParams.append(k, props[k]);

    this.setState({ isSubmitting: true });
    fetch(url, {
        method: 'GET',
        credentials: 'same-origin',
        mode: 'cors',
        redirect: 'follow'
      }).then(response => {
        return response.json();
      }).then( response => {
        this.setState({ isOpen: false, isSubmitting: false });
        this.props.dispatch({
          type: RESET_FEEDBACK,
          component: NAME
        });

      });
  }

  toggle = () => {
    this.setState({ isOpen: !this.state.isOpen });
  }

  render(){
    let { level, message, type } = this.props;
    let { isOpen, isSubmitting } = this.state;
    return (
      <div className={`global-feedback${isOpen? ' open' : ''}`}>
        <div className="open-close" onClick={this.toggle}>
          {isOpen && <PlusX x={true} />}
          {!isOpen && <h5 className="margin-0">Feedback</h5>}
        </div>
        <form>
          <div className="global-feedback__level">
            <h4 className="margin-5">Related to</h4>
            <a onClick={()=>{this.setLevel('sitewide')}} className={`${level=='sitewide' ? 'selected ' : ''}button--text`}>The whole site</a>
            <a onClick={()=>{this.setLevel('thispage')}} className={`${level=='thispage' ? 'selected ' : ''}button--text`}>This page</a>
          </div>
          <div className="global-feedback__type">
              <h4 className="margin-5">Type</h4>
              <a className={`${type=='bug' ? 'selected ' : ''}button--text`} onClick={()=>{this.setType('bug');}}>Bug</a>
              <a className={`${type=='request' ? 'selected ' : ''}button--text`} onClick={()=>{this.setType('request');}}>Request</a>
          </div>
          <div className="global-feedback__message margin-top-10">
            <TextArea label="Feedback" value={message} onChange={(e)=>{this.setMessage(e.target.value)}} type="text" />
          </div>
          <a className="button margin-top-25 margin-bottom-0" onClick={this.submit}>
            {!isSubmitting && <span>Send</span>}
            {isSubmitting && <span className="loading-dots--absolute">
              <span>.</span><span>.</span><span>.</span>
            </span>}
          </a>
        </form>
      </div>
    )
  }
}


const mapStateToProps = (state) => {
  if(state.feedback){
    return {
      ...state.feedback
    };
  }

  return {
    level: 'sitewide', username: '', message: '', type: '', page: location.href, os: ''
  };
};

APP = connect(mapStateToProps)(APP);

export default { ID, NAME, APP, REDUCERS };
