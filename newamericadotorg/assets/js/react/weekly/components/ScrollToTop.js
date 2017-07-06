import { Component } from 'react';
import { connect } from 'react-redux';
let timeout = 0;

let addScrollEvent = (dispatch) => {
  let content = document.querySelector('.weekly-content'),
    header = document.querySelector('.weekly-header');

  setTimeout(function(){
    if(header) header.style.top = '0px';
  });

  if(!content) return;
  content.addEventListener('scroll', (e) => {
    let top = -content.scrollTop*2 + 'px';
    clearTimeout(timeout);
    dispatch({
      type: 'SET_IS_SCROLLING',
      component: 'site',
      isScrolling: true
    });
    requestAnimationFrame(function(){
      header.style.top = top;
      timeout = setTimeout(()=>{
        dispatch({
          type: 'SET_IS_SCROLLING',
          component: 'site',
          isScrolling: false
        });
      }, 17);
    });
  }, false);

}

class ScrollToTop extends Component {
  componentDidUpdate(prevProps) {

    addScrollEvent(this.props.dispatch);
  }

  componentDidMount(){
    addScrollEvent(this.props.dispatch);
  }

  render() {
    return null;
  }
}

export default connect()(ScrollToTop);
