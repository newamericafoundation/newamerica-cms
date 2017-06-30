import { Component } from 'react';

class ScrollToTop extends Component {
  componentDidUpdate(prevProps) {
    if (this.props.location !== prevProps.location) {
      setTimeout(function(){
        window.scrollTo(0, 0)
      }, 0);
    }
  }

  render() {
    return null;
  }
}

export default ScrollToTop;
