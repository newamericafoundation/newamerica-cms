import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import reactRenderer from '../../react-renderer';
import Response from './Response';
import LoadingIcon from '../../components/LoadingIcon';
import { mapDispatchToProps, mapStateToProps } from './props';

class Fetch extends Component {
  hasLoaded = false;
  componentWillMount(){
    let {
      setEndpoint, resetQuery, receiveResults, endpoint,
      initialQuery, clear, fetchData, fetchOnMount, setBase, baseUrl
    } = this.props;

    setEndpoint(endpoint);
    if(baseUrl) setBase(baseUrl);
    resetQuery(initialQuery);

    if(clear){
      receiveResults([]);
      return;
    }

    if(fetchOnMount) fetchData();
  }

  componentDidUpdate(prevProps){
    let { fetchData, eager, resetQuery,initialQuery, fetchOnMount, endpoint, setEndpoint } = this.props;
    if(!eager || !fetchOnMount) return;
    if(JSON.stringify(prevProps.initialQuery) != JSON.stringify(initialQuery)|| prevProps.endpoint != endpoint ){
      setEndpoint(endpoint);
      resetQuery(initialQuery);
      fetchData();
    }
  }
  render() {
    let { className, showLoading, component, transition, fetchOnMount, renderIfNoResults, children, loadingState } = this.props;
    let { isFetching, results, hasResults} = this.props.response;

    if(component===null) return null;
    if(!hasResults && fetchOnMount){
      if(loadingState) return ( loadingState );
      if(showLoading) return (<div className="loading-icon-container"><LoadingIcon /></div>);
      return null;
    }

    if(hasResults && results.length===0 && !renderIfNoResults && !this.hasLoaded) return null;
    this.hasLoaded = true;

    let classes = 'na-react__fetch-component' + (transition ? ' fetch-transition ' : '') + (className ? ' ' + className : '') + (isFetching ? ' is-fetching': '');

    if(!showLoading){
      return (<this.props.component {...this.props} />);
    }

    return (
      <span className={`${classes}`}>
        <this.props.component {...this.props}/>
        {isFetching && <div className="loading-icon-container"><LoadingIcon /></div>}
      </span>
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
    loadingState: PropTypes.element,
    eager: PropTypes.bool,
    baseUrl: PropTypes.string,
    clear: PropTypes.bool,
    initialQuery: PropTypes.object,
    fetchOnMount: PropTypes.bool,
    showLoading: PropTypes.bool,
    transition: PropTypes.bool,
    renderIfNoResults: PropTypes.bool
  }

  static defaultProps = {
    initialQuery: {},
    fetchOnMount: false,
    eager: false,
    component: 'span',
    showLoading: false,
    transition: false,
    renderIfNoResults: true
  }

  name = null;

  constructor(props){
    super(props);

    let { name } = props;
    let component = reactRenderer.components[name] || {};

    if(name.indexOf('.')==-1 || !component.multi)
      this.name = name;
    else if(component.multi)
      this.name = `${name}.${component.components.length}`;

  }

  render(){
    return (
      <Fetch {...this.props} name={this.name} />
    );
  }
}

export default FetchWrapper;
