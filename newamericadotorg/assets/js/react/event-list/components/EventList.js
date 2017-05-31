import { Component } from 'react';
import { Fetch, Response } from '../../components/API'
import InfiniteLoadMore from '../../components/InfiniteLoadMore';
import EventListItem from './EventListItem';

const List = ({ response: { results } }) => (
  <div className="content-portrait-grid event-list__list row gutter-10">
    {results.map((r,i)=>(
      <EventListItem event={r} />
    ))}
  </div>
);

const PastList = ({ response, fetchAndAppend, setQueryParam }) => (
  <InfiniteLoadMore
    className="event-list__past-events"
    infiniteOnMount={true}
    isFetching={response.isFetching}
    hasNext={response.hasNext}
    data={response.results}
    upperBoundOffset={-(document.documentElement.clientHeight*1)}
    onNextPage={()=>{
      if(!response.hasNext) return false;
      setQueryParam('page', response.page+1);
      return fetchAndAppend;
    }}>
    <List response={response} />
  </InfiniteLoadMore>
)

export class FutureEvents extends Component {
  render(){
    return(
      <div className="event-list">
        <h1 className="event-list__heading centered">Upcoming Events</h1>
        <Fetch
          name="upcomingEvents"
          component="div"
          fetchOnMount={true}
          endpoint="event"
          initialQuery={{
            time_period: 'future',
            page_size: 200
          }}>
          <Response name="upcomingEvents" component={List} />
        </Fetch>
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
          component="div"
          fetchOnMount={true}
          endpoint="event"
          initialQuery={{
            time_period: 'past',
            page_size: 12,
            page: 1
          }}>
          <Response name="pastEvents" component={PastList} />
        </Fetch>
      </div>
    );
  }
}
