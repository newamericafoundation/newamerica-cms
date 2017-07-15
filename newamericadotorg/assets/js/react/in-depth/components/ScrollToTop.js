import { Component } from 'react';

export default class ScrollToTop extends Component {
  componentWillMount() {
    setTimeout(()=>{
      window.scrollTo(0,0);
    }, 0);
  }

  render() {
    return null;
  }
}
