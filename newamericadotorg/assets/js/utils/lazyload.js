import { Component } from 'react';
import LazyLoad from '../../../../node_modules/vanilla-lazyload/src/lazyload.core';

export const lazyloadBackgroundImage = new LazyLoad({ elements_selector: '.lazyload' });
export const lazyload = new LazyLoad();
export const update = () => {
  lazyload.update();
  lazyloadBackgroundImage.update();
}

export class LazyLoadImages extends Component {
  component = null;
  componentWillMount(){
    let { component } = this.props;
    this.component = component || 'span';
  }

  componentDidMount() {
    update();
  }
  componentDidUpdate(){
    update();
  }
  render() {
    let { className, children } = this.props;
    return (
      <this.component className={'compose__lazyload-images-wrapper ' + (className || '')}>
        {children}
      </this.component>
    );
  }
}

const singleton = {
  lazyload,
  lazyloadBackgroundImage,
  update
};

export default singleton;
