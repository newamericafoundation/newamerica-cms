import { NAME } from '../constants';
import { Component } from 'react';
import { Fetch } from '../../components/API';
import { EventsList } from '../../components/Events';

export default class Events extends Component {
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
        initialQuery={{
          subprogram_id: params.get('projectId') || '',
          [programType == 'program' ? 'program_id' : 'subprogram_id']: program.id,
          time_period: period,
          page_size: 6,
          page: 1,
          image_rendition: period=='future' ? 'fill-700x510' : 'fill-300x240'
        }}/>
    );
  }
}
