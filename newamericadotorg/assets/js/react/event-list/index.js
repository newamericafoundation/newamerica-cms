import { Component } from 'react';
import { NAME, ID } from './constants';
import { FutureEvents, PastEvents } from  './components/EventList';

class APP extends Component {
  componentWillMount(){
    this.state = { showPast: false };
  }
  showPast = () => {
    this.setState({ showPast: true });
  }
  render(){
    return(
      <section className="container--wide event-list">
        <FutureEvents />
        {!this.state.showPast &&
          <div className="event-list__show-past-button-wrapper">
            <a className="button transparent lg event-list__show-past-button" onClick={this.showPast}>
              Show Past Events
            </a>
          </div>
        }{this.state.showPast &&
          <PastEvents />
        }
      </section>
    );
  }
}

export default { NAME, ID, APP };
