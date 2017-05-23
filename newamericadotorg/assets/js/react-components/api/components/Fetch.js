import { Component, PropTypes } from 'react';
import { connect } from 'react-redux';
import { BASEURL } from '../constants';
import {
  fetch, setEndpoint, setParam, setParams,
  setBase, receiveResults
} from '../actions';

class Fetch extends Component {
  component = null;

  static propTypes = {
    name: PropTypes.string.isRequired,
    endpoint: PropTypes.string.isRequired,
    component: Proptype.object,
    eager: PropTypes.bool,
    baseUrl: PropTypes.string,
    clear: PropTypes.bool,
    initialQuery: PropTypes.object,
    fetchOnMount: PropTypes.bool
  }

  static defaultProps = {
    initialQuery: {},
    baseUrl: BASEURL
  }

  componentWillMount(){
    let {
      setParams, receiveResults, endpoint,
      initialQuery, clear, fetch, fetchOnMount,
      component
    } = this.props;

    this.component = component || (<span></span>);

    setParams(endpoint, initialQuery);

    if(clear){
      receiveResults([]);
      return;
    }

    if(fetchOnMount) fetch();
  }

  render() {
    let { className, children } = this.props;
    return (
      <this.component className={'compose__component ' + className}>
        {children}
      </this.component>
    );
  }
}

const mapStateToProps = state => ({});

const mapDispatchToProps = dispatch => ({
  setParams: function(endpoint,query){
    dispatch(setParams(this.name, {endpoint, query}));
  },

  fetch: function(){
    dispatch(fetch(this.name));
  },

  setEndpoint: function(endpoint){
    dispatch(setEndpoint(this.name, endpoint));
  },

  setParam: function(key, value){
    dispatch(setParam(this.name, {key, value}));
    if(this.eager) this.fetch();
  },

  receiveResults: function(val){
    dispatch(receiveResults(this.name, val));
  },

  setBase: function(baseUrl){
    dispatch(setBase(this.name, baseUrl));
  }
});

export default connect(
  mapStateToProps, mapDispatchToProps
)(Fetch);
