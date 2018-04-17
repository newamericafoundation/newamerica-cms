import { Component } from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import { NAME, ID } from './constants';
import { Fetch, Response } from '../components/API';
import Events from './components/Events';

class Routes extends Component {
  render(){
    return (
      <Router>
        <div className="container">
          <Route path="/events/" render={(props)=>(<Events {...props} program={this.props.response.results} />)}/> {/*hack for compatability with Program/Event component*/}
        </div>
      </Router>
    );
  }
}


class APP extends Component {

  render() {
    let { contentTypes, programs } = this.props;
    return (
      <Response component={Routes} name='meta' />
    );
  }
}

export default { NAME, ID, APP };
