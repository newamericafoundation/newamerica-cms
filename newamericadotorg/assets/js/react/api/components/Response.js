import { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import LoadingIcon from '../../components/LoadingIcon';
import { mapStateToProps, mapDispatchToProps } from './props';

class Response extends Component {
  static propTypes = {
    name: PropTypes.string.isRequired,
    component: PropTypes.oneOfType([
      PropTypes.func,
      PropTypes.string
    ]),
    showLoading: PropTypes.bool,
    transition: PropTypes.bool
  }

  static defaultProps = {
    component: 'div',
    showLoading: false,
    transition: false
  }

  render(){
    let { children, className, transition, showLoading, component } = this.props;
    let { isFetching } = this.props.response;
    return (
      <this.props.component {...this.props}
        className={'compose__response-component ' + (transition ? ' fetch-transition ' : '') +  (className||'') + (isFetching? ' is-fetching': '')}>
        {children || (component.props ? component.props.children : '')}
        {(isFetching&&showLoading) && <div className="loading-icon-container"><LoadingIcon /></div>}
      </this.props.component>
    );
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Response);
