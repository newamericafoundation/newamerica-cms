import { Component } from 'react';

export default class ScrollToTop extends Component {
  componentWillMount() {
    window.scrollTo(0,0);
  }

  render() {
    return null;
  }
}
