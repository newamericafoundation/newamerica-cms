const NAME = 'feedback';
const ID = 'feedback';

import { SET_FEEDBACK, SET_FEEDBACK_TYPE, SET_FEEDBACK_MESSAGE, SET_FEEDBACK_LEVEL, SET_FEEDBACK_EMAIL, RESET_FEEDBACK  } from './constants';
import { Text, TextArea } from '../components/Inputs';
import { connect } from 'react-redux';
import { Component } from 'react';
import bowser from 'bowser';
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
    let { contact, level, message, type, browser, os, page, ip } = this.props;
    let props = { contact, level, message, type, browser, os, page, ip};
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
    let { contact, level, message, type } = this.props;
    let { isOpen, isSubmitting } = this.state;
    return (
      <div className={`global-feedback${isOpen? ' open' : ''}`}>
        <div className="open-close" onClick={this.toggle}>
          {isOpen && <PlusX x={true} />}
          {!isOpen && <label className="block button--text margin-0">Feedback</label>}
        </div>
        <form>
          <div className="global-feedback__level">
            <label className="block">Related to:</label>
            <label onClick={()=>{this.setLevel('sitewide')}} className={`${level=='sitewide' ? 'selected ' : ''}button--text`}>The whole site</label>
            <label onClick={()=>{this.setLevel('thispage')}} className={`${level=='thispage' ? 'selected ' : ''}button--text`}>This page</label>
          </div>
          <div className="global-feedback__type margin-top-25">
              <a title="like" className={`fa fa-thumbs-up${type=='like' ? ' selected' : ''}`} onClick={()=>{this.setType('like');}}/>
              <a title="dislike" className={`fa fa-thumbs-down${type=='dislike' ? ' selected' : ''}`} onClick={()=>{this.setType('dislike');}}/>
              <a title="bug" className={`fa fa-bug${type=='bug' ? ' selected' : ''}`} onClick={()=>{this.setType('bug');}}/>
          </div>
          <div className="global-feedback__email margin-top-25">
            <Text label="Email or Name" value={contact} onChange={(e)=>{this.setEmail(e.target.value)}} type="text" />
          </div>
          <div className="global-feedback__message margin-top-25">
            <TextArea label="Feedback" value={message} onChange={(e)=>{this.setMessage(e.target.value)}} type="text" />
          </div>
          <label className="button margin-top-25 margin-bottom-0" onClick={this.submit}>
            {!isSubmitting && <span>Send</span>}
            {isSubmitting && <span className="loading-dots--absolute">
              <span>.</span><span>.</span><span>.</span>
            </span>}
          </label>
        </form>
      </div>
    )
  }
}


const mapStateToProps = (state) => ({
  contact: state.feedback.email || cache.get('feedback_email') || '',
  level: state.feedback.level || 'sitewide',
  message: state.feedback.message || '',
  type: state.feedback.type || '',
  browser: `${bowser.name} ${bowser.version}`,
  os: `${bowser.osname} ${bowser.osversion}`,
  page: location.href,
  ip: state.site.ip
});

APP = connect(mapStateToProps)(APP);

export default { ID, NAME, APP, REDUCERS };
