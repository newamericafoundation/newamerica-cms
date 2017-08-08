import { Fetch, Response } from '../components/API';
import { EventListItem } from '../components/Content';
import Carousel from '../components/Carousel';
import { Component } from 'react';
import PropTypes from 'prop-types';

const EventCarousel = ({ response }) => (
  <section className="container--full-width program-block">
  	<div className="program-block__heading">
  		<h1 className="centered narrow-margin">Events</h1>
  		<p className="program-heading__subheading subheading--h1 centered">
  			Political Reform program publications help to generate new ideas, voices, and technologies.
  		</p>
  	</div>
  	<section className="program-events container">
      <div className="program-event-carousel">
        <Carousel items={response.results} itemComponent={EventListItem} n={5}/>
      </div>
    </section>
  	<div className="program-block__button-wrapper button-wrapper centered">
  		<a className="button transparent" href="{{page.url}}publications/">View All Events</a>
  	</div>
  </section>

);

export class Events extends Component {

  render() {
    return(
      <Fetch
        name="program.events"
        endpoint="event"
        component={EventCarousel}
        fetchOnMount={true}
        showLoading={true}
        renderIfNoResults={false}
        transition={true}
        initialQuery={{
          page_size: 18,
          program_id: this.props.programId
        }}
      />
    );
  }
}
