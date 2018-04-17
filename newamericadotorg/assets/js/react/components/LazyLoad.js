import { Component } from 'react';
import LazyLoad from 'vanilla-lazyload';
import PropTypes from 'prop-types';

export const lazyloadBackgroundImage = new LazyLoad({ elements_selector: '.lazyload--background' });
export const lazyload = new LazyLoad();
export const update = () => {
  lazyload.update();
  lazyloadBackgroundImage.update();
}

export class LazyLoadImages extends Component {
  static propTypes = {
    component: PropTypes.oneOfType([
      PropTypes.func,
      PropTypes.string
    ])
  }

  static defaultProps ={
    component: 'span'
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
      <this.props.component {...this.props} className={'compose__lazyload-images-wrapper ' + (className||'')}>
        {children}
      </this.props.component>
    );
  }
}

export class LazyImage extends Component {
  el = null;
  shouldComponentUpdate(nextProps){
    let { src } = this.props;
    if(src !== nextProps.src){
      this.el.removeAttribute('data-was-processed');
      this.el.removeAttribute('src');
      return true;
    }

    return false;
  }

  render(){
    let { src, className } = this.props;

    return(
      <img
        ref={(el) => { this.el = el; }}
        data-original={src}
        className={`lazyload ${className}`} />
    );
  }
}

export class LazyBackgroundImage extends LazyImage {
  render(){
    let { src, className } = this.props;

    return(
      <div
        ref={(el) => { this.el = el; }}
        data-original={src}
        className={`lazyload--background ${className}`} />
    );
  }
}

const singleton = {
  lazyload,
  lazyloadBackgroundImage,
  update
};

export default singleton;
