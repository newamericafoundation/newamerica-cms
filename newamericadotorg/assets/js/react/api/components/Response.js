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

  hasLoaded = false;

  render(){
    let { children, className, transition, showLoading, component, fetchOnMount, renderIfNoResults} = this.props;
    let { isFetching, results, hasResults } = this.props.response;

    if(!hasResults && !this.hasLoaded){
      if(showLoading) return (<div className="loading-icon-container"><LoadingIcon /></div>);
      return null;
    }
    if(hasResults && results.length===0 && !renderIfNoResults && !this.hasLoaded) return null;
    this.hasLoaded = true;

    let classes = 'compose__fetch-response' + (transition ? ' fetch-transition ' : '') + (className ? ' ' + className : '') + (isFetching ? ' is-fetching': '');

    if(!showLoading){
      return (<this.props.component {...this.props}/>);
    }

    return (
      <span className={`${classes}`}>
        <this.props.component {...this.props} />
        {children}
        {isFetching && <div className="loading-icon-container"><LoadingIcon /></div>}
      </span>
    );
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Response);
