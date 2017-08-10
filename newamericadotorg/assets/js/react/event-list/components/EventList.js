import { Component } from 'react';
import { Fetch, Response } from '../../components/API'
import InfiniteLoadMore from '../../components/InfiniteLoadMore';
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

const PastList = ({ response, fetchAndAppend, setQueryParam, className }) => (
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

    <List items={response.results} cols='col-4 col-md-3 col-lg-5ths'/>
  </InfiniteLoadMore>
)

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
