import { Component } from 'react';
import { Fetch, Response } from '../../components/API'
import InfiniteLoadMore from '../../components/InfiniteLoadMore';
import EventListItem from './EventListItem';

export const List = ({ results, colxl2=false }) => (
  <div className="content-portrait-grid event-list row gutter-10">
    {results.map((r,i)=>(
      <EventListItem event={r} colxl2={colxl2} />
    ))}
  </div>
);

const FutureList = ({ className, response }) => (
  <div className={'event-lists__upcoming-events ' + className}>
    <List results={response.results}/>
  </div>
);

const PastList = ({ response, fetchAndAppend, setQueryParam, className }) => (
  <InfiniteLoadMore
    className={'event-lists__past-events ' + className }
    infiniteOnMount={true}
    isFetching={response.isFetching}
    hasNext={response.hasNext}
    data={response.results}
    upperBoundOffset={-(document.documentElement.clientHeight*1.5)}
    onNextPage={()=>{
      if(!response.hasNext) return false;
      setQueryParam('page', response.page+1);
      return fetchAndAppend;
    }}>
    <List results={response.results} colxl2={true}/>
  </InfiniteLoadMore>
)

export class FutureEvents extends Component {
  render(){
    return(
      <div className="event-list">
        <h1 className="event-list__heading centered">Upcoming Events</h1>
        <Fetch
          name="upcomingEvents"
          component={FutureList}
          fetchOnMount={true}
          endpoint="event"
          initialQuery={{
            time_period: 'future',
            page_size: 200
          }}/>
      </div>
    );
  }
}

export class PastEvents extends Component {
  render(){
    return(
      <div className="event-list">
        <h1 className="event-list__heading centered">Past Events</h1>
        <Fetch
          name="pastEvents"
          component={PastList}
          fetchOnMount={true}
          endpoint="event"
          initialQuery={{
            time_period: 'past',
            page_size: 12,
            page: 1
          }}/>
      </div>
    );
  }
}
