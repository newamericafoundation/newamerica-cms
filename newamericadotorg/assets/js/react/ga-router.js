import createBrowserHistory from 'history/createBrowserHistory';

import { Component } from 'react';
import { Router } from 'react-router-dom';

export default class GARouter extends Component {
  pushDataLayer = (location) => {
    dataLayer.push({
      'event':'VirtualPageview',
      'virtualPagePath': location.pathname,
      'virtualPageTitle': document.title,
      'virtualPageHostname': window.location.host || window.location.hostname,
      'virtualReferrer': document.referrer
    });
  }

  triggerVirtualPageView = (location) => {
    setTimeout(()=>{
      try {
        this.pushDataLayer(location)
      } catch(err){
        // if dataLayer isn't loaded yet
        if(err.name=='ReferenceError'){
          setTimeout(()=>{
            this.pushDataLayer(location);
          }, 500);
        }
      }
    }, 1)
  }
  constructor(props){
    super(props);

    const history = createBrowserHistory();
    let currentPath = location.pathname;
    history.listen((location, action) => {
      if(location.pathname != currentPath) this.triggerVirtualPageView(location);
      currentPath = location.pathname;
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
