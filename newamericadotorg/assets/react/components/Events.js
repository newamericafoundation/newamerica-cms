import { PublicationsList, PublicationsWrapper } from './Publications';
import { LoadingDots } from './Icons';
import { Link, NavLink } from 'react-router-dom';
import {
  SubprogramFilter,
  ProgramFilter,
  TopicFilter,
  DateFilter,
  FilterGroup
} from './Filters';
import { EventItem } from './ContentCards';
import React, { Component } from 'react';

class Filters extends Component {
  render() {
    let { program, response, history, location, topics } = this.props;
    return (
      <FilterGroup history={history} location={location} response={response}>
        <DateFilter
          label="Date"
          expanded={response.params.query.after !== undefined}
        />
        {program.programs && (
          <ProgramFilter
            programs={program.programs}
            expanded={response.params.query.program_id !== undefined}
            label="Program"
          />
        )}
        {program.subprograms && (
          <SubprogramFilter
            subprograms={program.subprograms}
            expanded={response.params.query.subprogram_id !== undefined}
            label="Project"
          />
        )}
        {topics && (
          <TopicFilter
            label="Topic"
            topics={topics}
            topicId={response.params.query.topic_id}
            expanded={response.params.query.topic_id !== undefined}
          />
        )}
      </FilterGroup>
    );
  }
}

class Past extends Component {
  render() {
    return (
      <PublicationsWrapper
        filters={<Filters {...this.props} />}
        publications={<PublicationsList {...this.props} />}
      />
    );
  }
}

export class EventsList extends Component {
  activeStyle = {
    fontWeight: 'bold'
  };

  render() {
    let { location, period, response } = this.props;
    return (
      <div className="program__events margin-top-35">
        <div className="program__events__period-toggles">
          <h6 className="inline with-separator">
            <NavLink
              style={period == 'future' ? this.activeStyle : {}}
              to={{ pathname: location.pathname, search: `?period=future` }}
            >
              Upcoming
            </NavLink>
          </h6>
          <h6 className="inline">
            <NavLink
              style={period == 'past' ? this.activeStyle : {}}
              to={{ pathname: location.pathname, search: `?period=past` }}
            >
              Past
            </NavLink>
          </h6>
        </div>
        {period == 'future' && <PublicationsList card_type='future_events' {...this.props} />}
        {period == 'past' && <Past {...this.props} />}
      </div>
    );
  }
}
