import { Route } from 'react-router-dom';
import GARouter from '../ga-router';
import React, { Component } from 'react';
import { Fetch, Response} from '../components/API';
import { NAME, ID } from './constants';
import Publications from './components/Publications';

class Routes extends Component {
  render(){
    let { response : { results }} = this.props;
    return (
      <div className="container">
        <GARouter>
          <div className="homepage__publications">
            <Route path="/:contentType/" render={(props)=> (<Publications content_types={results.content_types} programs={results.programs} {...props} />)} />
          </div>
        </GARouter>
      </div>
    );
  }
}

class APP extends Component {
  render() {
    return (
      <Response component={Routes} name='meta'/>
    );
  }
}

export default {
  NAME, ID, APP
};
