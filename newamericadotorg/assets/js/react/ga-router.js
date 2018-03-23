import createBrowserHistory from 'history/createBrowserHistory';
import ReactGA from 'react-ga';
import { Component } from 'react';
import { Router } from 'react-router-dom';


export default class GARouter extends Component {
  constructor(props){
    super(props);
    ReactGA.initialize('UA-368921-34');
    const history = createBrowserHistory();
    history.listen((location, action) => {
      ReactGA.set({ page: location.pathname });
      ReactGA.pageview(location.pathname);
    });
    this.state = {
      history
    }
  }
  render(){
    return (
      <Router history={this.state.history}>
        {this.props.children}
      </Router>
    );
  }
}
