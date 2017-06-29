import { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import composer from '../../index';
import { BASEURL } from '../constants';
import Response from './Response';
import LoadingIcon from '../../components/LoadingIcon';
import { mapDispatchToProps, mapStateToProps } from './props';

class Fetch extends Component {
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

  componentDidUpdate(prevProps){
    let { fetchData, setParams, endpoint, initialQuery, fetchOnMount } = this.props;
    if( !Object.is(prevProps.endpoint, endpoint) ){
      setParams({ endpoint, query: initialQuery }, false);
      if(fetchOnMount) fetchData();
    }
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
    let { isFetching, results } = this.props.response;

    if(!results) return null;
    if(results instanceof Array && !results.length) return null;
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

Fetch = connect(
  mapStateToProps, mapDispatchToProps
)(Fetch);

class FetchWrapper extends Component{
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

  name = null;

  constructor(props){
    super(props);

    let { name } = props;
    let composerComponent = composer.components[name];

    this.name = name;

    if(composerComponent){
      if(composerComponent.multi){
        this.name = `${name}.${composerComponent.components.length}`;
      }
    }
  }

  render(){
    return (
      <Fetch {...this.props} name={this.name} />
    );
  }
}

export default FetchWrapper;
