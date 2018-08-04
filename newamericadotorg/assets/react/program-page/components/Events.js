import './Events.scss';

import { NAME } from '../constants';
import React, { Component } from 'react';
import { Fetch } from '../../components/API';
import { EventsList } from '../../components/Events';

export default class Events extends Component {
  initialQuery = () => {
    let { programType, program } = this.props;
    let params = new URLSearchParams(location.search.replace('?', ''));
    let period = params.get('period') || 'future';
    let programId = programType == 'program' ? 'program_id' : 'subprogram_id';

    let initQuery = {
      [programId]: program.id,
      time_period: period,
      page_size: 12,
      page: 1,
      image_rendition: period=='future' ? 'fill-700x510' : 'fill-300x230'
    };

    if(params.get('projectId'))
      initQuery.subprogram_id = params.get('projectId');
    if(params.get('topicId'))
      initQuery.topic_id = params.get('topicId');
    if(params.get('after'))
      initQuery.after = params.get('after');
    if(params.get('before'))
      initQuery.before = params.get('before');

    return initQuery
  }
  render(){
    let { program, location, history, programType } = this.props;
    let params = new URLSearchParams(location.search.replace('?', ''));
    let period = params.get('period') || 'future';

    return (
      <Fetch name={`${NAME}.events`}
        component={EventsList}
        endpoint="event"
        fetchOnMount={true}
        eager={true}
        period={period}
        location={location}
        history={history}
        program={program}
        initialQuery={this.initialQuery()}/>
    );
  }
}
