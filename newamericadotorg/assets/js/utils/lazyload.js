import { Component } from 'react';
import LazyLoad from '../../../../node_modules/vanilla-lazyload/src/lazyload.core';

export const lazyload = new LazyLoad();

export class LazyLoadImages extends Component {
  component = null;
  componentWillMount(){
    let { component } = this.props;
    this.component = component || 'span';
  }

  componentDidMount() {
    lazyload.update();
  }
  componentDidUpdate(){
    lazyload.update();
  }
  render() {
    let { className, children } = this.props;
    return (
      <this.component className={'compose__lazyload-images-wrapper ' + className}>
        {children}
      </this.component>
    );
  }
}

export default lazyload;
