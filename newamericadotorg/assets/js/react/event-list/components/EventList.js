import { Component } from 'react';
import { Fetch, Response } from '../../components/API'
import InfiniteLoadMore from '../../components/InfiniteLoadMore';
import EventListItem from './EventListItem';

const ListWrapper = ({ className, children }) => (
  <div className={'event-list__past-events ' + className}>{children}</div>
);

const List = ({ response: { results }, colxl2=false }) => (
  <div className="content-portrait-grid event-list__list row gutter-10">
    {results.map((r,i)=>(
      <EventListItem event={r} colxl2={colxl2} />
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
    upperBoundOffset={-(document.documentElement.clientHeight*1.5)}
    onNextPage={()=>{
      if(!response.hasNext) return false;
      setQueryParam('page', response.page+1);
      return fetchAndAppend;
    }}>
    <List response={response} colxl2={true}/>
  </InfiniteLoadMore>
)

export class FutureEvents extends Component {
  render(){
    return(
      <div className="event-list">
        <h1 className="event-list__heading centered">Upcoming Events</h1>
        <Fetch
          name="upcomingEvents"
          component={ListWrapper}
          fetchOnMount={true}
          endpoint="event"
          initialQuery={{
            time_period: 'future',
            page_size: 200
          }}>
          <Response component={List} />
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
          component={ListWrapper}
          fetchOnMount={true}
          endpoint="event"
          initialQuery={{
            time_period: 'past',
            page_size: 12,
            page: 1
          }}>
          <Response component={PastList} />
        </Fetch>
      </div>
    );
  }
}
