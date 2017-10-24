import { Component } from 'react';
import { connect } from 'react-redux';
import getNestedState from '../../utils/get-nested-state';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import { NAME, ID } from './constants';
import { FutureEvents, PastEvents } from  './components/EventList';

class Events extends Component {
  componentWillMount(){
    this.state = { showPast: false };
  }
  showPast = () => {
    this.setState({ showPast: true });
  }
  render(){
    let { params, upcomingLoaded } = this.props;
    return(
      <section className="container--medium event-lists">
        <FutureEvents params={params} />
        {(!this.state.showPast && upcomingLoaded) &&
          <div className="event-lists__show-past-button-wrapper">
            <a className="button transparent lg event-lists__show-past-button" onClick={this.showPast}>
              Show Past Events
            </a>
          </div>
        }{this.state.showPast &&
          <PastEvents params={params} />
        }
      </section>
    );
  }
}

const mapStateToProps = (state) => ({
  upcomingLoaded: getNestedState(state, 'eventList.upcoming.hasResults')
});

Events = connect(mapStateToProps)(Events);

const APP = ({}) => (
  <Router>
    <Switch>
      <Route path="/events" component={Events} />
      <Route path="/:programSlug/events" render={({match: { params }})=>(
        <Events params={params} />
      )}/>
      <Route path="/:programSlug/:subprogramSlug/events" render={({match: { params }})=>(
        <Events params={params} />
      )}/>
    </Switch>
  </Router>
);

export default { NAME, ID, APP };
