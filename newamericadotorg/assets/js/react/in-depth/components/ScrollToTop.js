import { Component } from 'react';

export default class ScrollToTop extends Component {
  componentWillMount() {
    let content = document.querySelector('.in-depth__content');
    if(content) content.scrollTop = 0;
  }

  render() {
    return null;
  }
}
