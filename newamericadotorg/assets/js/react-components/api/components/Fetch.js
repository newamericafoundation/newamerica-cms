import { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { BASEURL } from '../constants';
import {
  fetchData, setEndpoint, setParam, setParams,
  setBase, receiveResults
} from '../actions';

import lazyload from '../../../utils/lazyload';

class Fetch extends Component {
  component = null;

  static propTypes = {
    name: PropTypes.string.isRequired,
    endpoint: PropTypes.string.isRequired,
    component: PropTypes.func,
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
      initialQuery, clear, fetchData, fetchOnMount,
      component
    } = this.props;

    this.component = component || 'span';

    setParams(endpoint, initialQuery);

    if(clear){
      receiveResults([]);
      return;
    }

    if(fetchOnMount) fetchData();
  }

  render() {
    let { className, children } = this.props;
    return (
      <this.component className={'compose__fetch-component ' + className}>
        {children}
      </this.component>
    );
  }
}

const mapStateToProps = state => ({});

const mapDispatchToProps = (dispatch, props) => ({
  setParams: (endpoint,query) => {
    dispatch(setParams(props.name, {endpoint, query}));
  },

  fetchData: () => {
    dispatch(fetchData(props.name));
  },

  setEndpoint: (endpoint) => {
    dispatch(setEndpoint(props.name, endpoint));
  },

  setParam: (key, value) => {
    dispatch(setParam(props.name, {key, value}));
    if(props.eager) this.fetch();
  },

  receiveResults: (val) => {
    dispatch(receiveResults(props.name, val));
  },

  setBase: (baseUrl) => {
    dispatch(setBase(this.name, baseUrl));
  }
});

export default connect(
  mapStateToProps, mapDispatchToProps
)(Fetch);
