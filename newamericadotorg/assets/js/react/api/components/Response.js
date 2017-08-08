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
    transition: PropTypes.bool,
    renderIfNoResults: PropTypes.bool
  }

  static defaultProps = {
    component: 'div',
    showLoading: false,
    transition: false,
    renderIfNoResults: true
  }

  render(){
    let { children, className, transition, showLoading, component, fetchOnMount, renderIfNoResults } = this.props;
    let { isFetching, results, hasResults } = this.props.response;
    if(!hasResults && fetchOnMount) return null;
    if(hasResults && results.length===0 && !renderIfNoResults) return null;
    return (
      <this.props.component {...this.props}
        className={'compose__response-component ' + (transition ? ' fetch-transition ' : '') +  (className||'') + (isFetching? ' is-fetching': '')}>
      </this.props.component>
    );
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Response);
