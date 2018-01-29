import { BrowserRouter as Router, Route } from 'react-router-dom';
import { Component } from 'react';
import { Fetch, } from '../components/API';
import { NAME, ID } from './constants';
import Publications from './components/Publications';

class Routes extends Component {
  render(){
    let { response : { results }} = this.props;
    return (
      <div className="container">
        <Router>
          <div className="homepage__publications">
            <Route path="/:contentType/" render={(props)=> (<Publications content_types={results.content_types} programs={results.programs} {...props} />)} />
          </div>
        </Router>
      </div>
    );
  }
}

class APP extends Component {

  render() {
    let { contentTypes, programs } = this.props;
    return (
      <Fetch component={Routes}
        name={`${NAME}.meta`}
        endpoint={`meta`}
        fetchOnMount={true} />
    );
  }
}

export default {
  NAME, ID, APP
};
