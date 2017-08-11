import { Component } from 'react';
import { connect } from 'react-redux';
import { Fetch, Response } from '../../components/API'
import InfiniteLoadMore from '../../components/InfiniteLoadMore';
import DatePicker from '../../components/DatePicker';
import Select from '../../components/Select';
import EventListItem from './EventListItem';

export const List = ({ items, cols, children }) => (
  <div className="content-portrait-grid event-list row gutter-15">
    {items.map((r,i)=>(
      <EventListItem item={r} cols={cols} />
    ))}
    {children}
  </div>
);

const FutureList = ({ response }) => (
  <List items={response.results} cols='col-4 col-md-3 col-lg-5ths'>
    {(response.results.length===0 && !response.isFetching) &&
      <label className="active lg block centered">No upcoming events. Check back soon!</label>
    }
  </List>
);

let PastList = ({ response, fetchAndAppend, setQueryParam, setQuery, className, programs, isSiteWide }) => (
  <InfiniteLoadMore
    className={'event-lists__past-events ' + className }
    response={response}
    promptToLoadMore={true}
    upperBoundOffset={-(document.documentElement.clientHeight*1.5)}
    onNextPage={()=>{
      if(!response.hasNext) return false;
      setQueryParam('page', response.page+1);
      return fetchAndAppend;
    }}>
      <div className="content-filters">
        {isSiteWide &&<Select
          options={programs}
          className="content-filters__filter program wide"
          name="Program"
          valueAccessor='id'
          labelAccessor='title'
          onChange={(option)=>{
            if(option) setQueryParam('program_id', option.id, true);
            else setQueryParam('program_id', '', true);
        }}/>}
        <DatePicker
          onDatesChange={({startDate, endDate})=>{
            setQuery({
              after: startDate || '',
              before: endDate || ''
            }, true);
          }}
        />
      </div>
    <List items={response.results} cols='col-4 col-md-3 col-lg-5ths'/>
  </InfiniteLoadMore>
);

const mapStateToProps = (state) => ({
  programs: state.programData.results
});

PastList = connect(mapStateToProps)(PastList);

export class FutureEvents extends Component {
  render(){
    let { params } = this.props;
    let query = {};
    if(params){
      if(params.projectSlug) query.project_slug = params.projectSlug;
      else if(params.programSlug) query.program_slug = params.programSlug;
    }
    return(
      <div className="event-list">
        <h1 className="event-list__heading centered">Upcoming Events</h1>
        <Fetch name="eventList.upcoming"
          className="event-lists__upcoming-events"
          endpoint="event"
          fetchOnMount={true}
          showLoading={true}
          transition={true}
          initialQuery={{
            time_period: 'future',
            page_size: 200,
            ...query
          }}>
          <Response component={FutureList} />
        </Fetch>
      </div>
    );
  }
}

export class PastEvents extends Component {
  render(){
    let { params } = this.props;
    let query = {};
    if(params){
      if(params.projectSlug) query.project_slug = params.projectSlug;
      else if(params.programSlug) query.program_slug = params.programSlug;
    }
    return(
      <div className="event-list">
        <h1 className="event-list__heading centered">Past Events</h1>
        <Fetch name="eventList.past"
          component={PastList}
          fetchOnMount={true}
          endpoint="event"
          isSiteWide={!params}
          initialQuery={{
            time_period: 'past',
            page_size: 15,
            page: 1,
            ...query
          }}/>
      </div>
    );
  }
}
