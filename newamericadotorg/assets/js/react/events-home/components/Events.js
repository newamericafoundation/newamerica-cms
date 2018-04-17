import { Component } from 'react';
import { EventsList } from '../../components/Events';
import { Fetch } from '../../components/API';
import { NAME } from '../constants';

export default class Events extends Component {
  initialQuery = () => {
    let { program } = this.props;
    let params = new URLSearchParams(location.search.replace('?', ''));
    let period = params.get('period') || 'future';

    let initQuery = {
      time_period: period,
      page_size: 6,
      page: 1,
      image_rendition: period=='future' ? 'fill-700x510' : 'fill-300x230'
    };

    if(params.get('programId'))
      initQuery.program_id = params.get('programId');
    if(params.get('after'))
      initQuery.after = params.get('after');
    if(params.get('before'))
      initQuery.before = params.get('before');

    return initQuery
  }

  render(){
    let { location, history, program } = this.props;
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
