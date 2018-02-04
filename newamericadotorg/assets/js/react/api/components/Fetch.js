import { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import composer from '../../index';
import Response from './Response';
import LoadingIcon from '../../components/LoadingIcon';
import { mapDispatchToProps, mapStateToProps } from './props';

class Fetch extends Component {
  hasLoaded = false;
  componentWillMount(){
    let {
      setEndpoint, resetQuery, receiveResults, endpoint,
      initialQuery, clear, fetchData, fetchOnMount
    } = this.props;

    setEndpoint(endpoint);
    resetQuery(initialQuery);

    if(clear){
      receiveResults([]);
      return;
    }

    if(fetchOnMount) fetchData();
  }

  componentDidUpdate(prevProps){
    let { fetchData, setEndpoint, eager, resetQuery, endpoint, initialQuery, fetchOnMount } = this.props;
    if( !Object.is(prevProps.endpoint, endpoint) || !Object.is(prevProps.initialQuery, initialQuery) ){
      setEndpoint(endpoint);
      resetQuery(initialQuery);
      if(fetchOnMount && eager) fetchData();
    }
  }
  render() {
    let { className, showLoading, component, transition, fetchOnMount, renderIfNoResults, children } = this.props;
    let { isFetching, results, hasResults} = this.props.response;

    if(!hasResults && fetchOnMount){
      if(showLoading) return (<div className="loading-icon-container"><LoadingIcon /></div>);
      return null;
    }

    if(hasResults && results.length===0 && !renderIfNoResults && !this.hasLoaded) return null;
    this.hasLoaded = true;

    let classes = 'compose__fetch-component' + (transition ? ' fetch-transition ' : '') + (className ? ' ' + className : '') + (isFetching ? ' is-fetching': '');

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
    let composerComponent = composer.components[name] || {};

    if(name.indexOf('.')==-1 || !composerComponent.multi)
      this.name = name;
    else if(composerComponent.multi)
      this.name = `${name}.${composerComponent.components.length}`;

  }

  render(){
    return (
      <Fetch {...this.props} name={this.name} />
    );
  }
}

export default FetchWrapper;
