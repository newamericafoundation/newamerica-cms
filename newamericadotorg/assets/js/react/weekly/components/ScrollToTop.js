import React, { Component } from 'react';
import { connect } from 'react-redux';
let timeout = 0;

let addScrollEvent = (dispatch) => {
  let content = document.querySelector('.weekly-content'),
    header = document.querySelector('.weekly-header');


  if(header){
    if(header.style.top != '0px' && header.style.top != '' && header.style.top != null){
      header.style.display = 'none';
    }
    setTimeout(function(){
      header.style.top = '0px';
      header.style.display = 'block';
    }, 250);
  }

  if(!content) return;
  let isArticle = content.classList.contains('weekly-article');
  content.addEventListener('scroll', (e) => {
    let top = content.scrollTop;
    clearTimeout(timeout);
    dispatch({
      type: 'SET_IS_SCROLLING',
      component: 'site',
      isScrolling: true
    });

    timeout = setTimeout(()=>{
      dispatch({
        type: 'SET_IS_SCROLLING',
        component: 'site',
        isScrolling: false
      });
    }, 17);
    requestAnimationFrame(function(){
      if(isArticle) header.style.top = -top*2 + 'px';
    });
  }, false);

}

class ScrollToTop extends Component {
  componentDidUpdate(prevProps) {

    //addScrollEvent(this.props.dispatch);
  }

  componentDidMount(){
    //addScrollEvent(this.props.dispatch);
  }

  render() {
    return null;
  }
}

export default connect()(ScrollToTop);
