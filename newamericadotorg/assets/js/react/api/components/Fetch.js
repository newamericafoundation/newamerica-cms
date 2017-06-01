import { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { BASEURL } from '../constants';
import {
  fetchData, fetchAndAppend, setEndpoint, setQueryParam, setParams,
  setQuery, setBase, receiveResults, setFetchingStatus
} from '../actions';


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
    fetchOnMount: PropTypes.bool
  }

  static defaultProps = {
    initialQuery: {},
    baseUrl: BASEURL,
    fetchOnMount: false,
    eager: false,
    component: 'span'
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

  applyNameToResponseChild = () => {
    let { children, name } = this.props;
    let _children;
    if(typeof children == 'object'){
      if(children.type){
        if(children.type.displayName=="Connect(Response)")
          _children = (
            <children.type {...children.props} name={name} >
              {children.props.children}
            </children.type>
          );
      }
    }
    return _children || children;
  }

  render() {
    let { className } = this.props;
    let children = this.applyNameToResponseChild();

    return (
      <this.props.component {...this.props} className={'compose__fetch-component ' + (className||'')}>
        {children}
      </this.props.component>
    );
  }
}

export const mapStateToProps = (state, props) => ({
  response: state[props.name] || { isFetching: false, hasNext: false, hasPrevious: false, results: [] }
});

export const mapDispatchToProps = (dispatch, props) => ({
  setParams: ({ endpoint, query, baseUrl }, eager) => {
    dispatch(setParams(props.name, { endpoint, query, baseUrl }));
    if(eager===false) return;
    if(props.eager || eager) dispatch(fetchData(props.name));
  },

  setEndpoint: (endpoint, eager) => {
    dispatch(setEndpoint(props.name, endpoint));
    if(eager===false) return;
    if(props.eager || eager) dispatch(fetchData(props.name));
  },

  setQueryParam: (key, value, eager) => {
    dispatch(setQueryParam(props.name, {key, value}));
    if(eager===false) return;
    if(props.eager || eager) dispatch(fetchData(props.name));
  },

  setQuery: (query, eager) => {
    dispatch(setQuery(props.name, query));
    if(eager===false) return;
    if(props.eager || eager) dispatch(fetchData(props.name));
  },

  setBase: (baseUrl, eager) => {
    dispatch(setBase(props.name, baseUrl));
    if(eager===false) return;
    if(props.eager || eager) dispatch(fetchData(props.name));
  },

  setFetchingStatus: (status) => {
    dispatch(setFetchingStatus(props.name, status));
  },

  fetchData: (callback) => {
    dispatch(fetchData(props.name, callback));
  },

  fetchAndAppend: (callback) => {
    dispatch(fetchAndAppend(props.name, callback));
  },

  receiveResults: (val) => {
    dispatch(receiveResults(props.name, val));
  }

});

export default connect(
  mapStateToProps, mapDispatchToProps
)(Fetch);
