import { Fetch, Response } from '../components/API';
import { EventListItem } from '../components/Content';
import Carousel from '../components/Carousel';
import { Component } from 'react';
import PropTypes from 'prop-types';

const EventCarousel = ({ response }) => (
  <div className="program-event-carousel">
    <Carousel items={response.results} itemComponent={EventListItem}/>
  </div>
);

export class Events extends Component {

  render() {
    return(
      <Fetch
        name="programEventList"
        endpoint="event"
        component={EventCarousel}
        fetchOnMount={true}
        showLoading={true}
        transition={true}
        initialQuery={{
          page_size: 18,
          program_id: this.props.programId
        }}
      />
    );
  }
}
