import { PublicationsList, PublicationsWrapper, LoadingDots } from './Publications';
import { Link, NavLink } from 'react-router-dom';
import { Filter, SubprogramFilter, ProgramFilter, TopicFilter, FilterGroup } from './Filters';
import { EventItem } from './ContentCards'
import { format as formatDate } from 'date-fns';
import { Component } from 'react';

class Upcoming extends Component {

  render(){
    let { events } = this.props;
    if(events.length==0){
      return (

        <div className="margin-top-60 centered">
          <label>No upcoming events. </label> <NavLink className="button--text" to={{ search:"?period=past" }}>See past events</NavLink>.
        </div>
      )
    }
    return (
      <div className="program__events__upcoming margin-top-35 row gutter-10">
        {events.map((e,i)=>(
          <div className="col-md-4 col-12">
            <EventItem event={e} />
          </div>
        ))}
      </div>
    );
  }
}

class AbstractFilter extends Filter {
  render(){
    let { subprograms, response: { params: { query } } } = this.props;
    return (
      <div className={`program__publications-filters__filter type ${this.state.expanded ? 'expanded' : ''}`}>
        {this.label()}
        <form>
        </form>
      </div>
    );
  }
}

class Filters extends Component {
  render(){
    let { program, response, history, location } = this.props;
    return (
      <FilterGroup
          history={history}
          location={location}
          response={response}>
        <AbstractFilter label="Date" />
        {program.programs && <ProgramFilter programs={program.programs} label="Program" />}
        {program.subprograms && <SubprogramFilter subprograms={program.subprograms} label="Project" />}
        {program.topics && <TopicFilter label="Topic" />}
      </FilterGroup>
    );
  }
}

class Past extends Component {
  render(){
    return (
      <PublicationsWrapper
          filters={<Filters {...this.props}/>}
          publications={<PublicationsList {...this.props} />}/>
    );
  }
}

export class EventsList extends Component {
  activeStyle = {
    fontWeight: 'bold',
    fontStyle: 'italic'
  }

  render(){
    let { location, period, response } = this.props;
    return (
      <div className="program__events margin-top-35">
        <div className="program__events__period-toggles">
          <label className="inline with-separator">
            <NavLink style={period=='future' ? this.activeStyle : {}} to={{ pathname: location.pathname, search:`?period=future`}}>Upcoming</NavLink>
          </label>
          <label className="inline">
            <NavLink style={period=='past' ? this.activeStyle : {}} to={{ pathname: location.pathname, search:`?period=past`}}>Past</NavLink>
          </label>
        </div>
        {(response.isFetching && period=='future') && <div className="margin-top-35 centered"><LoadingDots /></div>}
        {(!response.isFetching && period=='future') && <Upcoming events={response.results}/>}
        {(period=='past') && <Past {...this.props} />}
      </div>
    );
  }
}
