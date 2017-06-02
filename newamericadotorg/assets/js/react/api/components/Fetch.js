import { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { BASEURL } from '../constants';
import Response from './Response';
import LoadingIcon from '../../components/LoadingIcon';
import { mapDispatchToProps, mapStateToProps } from './props';

class Fetch extends Component {
  static propTypes = {
    name: PropTypes.string.isRequired,
    endpoint: PropTypes.string.isRequired,
    component: PropTypes.oneOfType([
      PropTypes.func,
      PropTypes.string
    ]),
    eager: PropTypes.bool,
    baseUrl: PropTypes.string,
    clear: PropTypes.bool,
    initialQuery: PropTypes.object,
    fetchOnMount: PropTypes.bool,
    showLoading: PropTypes.bool,
    transition: PropTypes.bool
  }

  static defaultProps = {
    initialQuery: {},
    baseUrl: BASEURL,
    fetchOnMount: false,
    eager: false,
    component: 'div',
    showLoading: false,
    transition: false
  }

  componentWillMount(){
    let {
      setParams, receiveResults, endpoint,
      initialQuery, clear, fetchData, fetchOnMount
    } = this.props;

    setParams({ endpoint, query: initialQuery }, false);

    if(clear){
      receiveResults([]);
      return;
    }

    if(fetchOnMount) fetchData();
  }

  mapNameToResponse = () => {
    let { children, name } = this.props;
    let _children;
    if(typeof children == 'object'){
      if(children.type === Response){
        return (<Response name={name} component={children.props.component} />);
      }
    }

    return children;
  }

  render() {
    let { className, showLoading, component, transition } = this.props;
    let { isFetching } = this.props.response;
    let children = this.mapNameToResponse();
    return (
      <this.props.component {...this.props}
        className={'compose__fetch-component' + (transition ? ' fetch-transition ' : '') + (className||'') + (isFetching? ' is-fetching': '')}>
        {children || (component.props ? component.props.children : '')}
        {(isFetching&&showLoading) && <div className="loading-icon-container"><LoadingIcon /></div>}
      </this.props.component>
    );
  }
}

export default connect(
  mapStateToProps, mapDispatchToProps
)(Fetch);
