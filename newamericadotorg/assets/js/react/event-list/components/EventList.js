import { Component } from 'react';
import { Fetch, Response } from '../../components/API'
import InfiniteLoadMore from '../../components/InfiniteLoadMore';
import EventListItem from './EventListItem';

export const List = ({ items, cols, children }) => (
  <div className="content-portrait-grid event-list row gutter-10">
    {items.map((r,i)=>(
      <EventListItem item={r} cols={cols} />
    ))}
    {children}
  </div>
);

const FutureList = ({ response }) => (
  <List items={response.results} cols='col-4 col-md-3'>
    {(response.results.length===0 && !response.isFetching) &&
      <label className="active lg block centered">No upcoming events. Check back soon!</label>
    }
  </List>
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

    <List items={response.results} cols='col-4 col-md-3 col-xl-2'/>
  </InfiniteLoadMore>
)

export class FutureEvents extends Component {
  render(){
    return(
      <div className="event-list">
        <h1 className="event-list__heading centered">Upcoming Events</h1>
        <Fetch name="upcomingEvents"
          className="event-lists__upcoming-events"
          endpoint="event"
          fetchOnMount={true}
          showLoading={true}
          transition={true}
          initialQuery={{
            time_period: 'future',
            page_size: 200
          }}>
          <Response component={FutureList} />
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
        <Fetch name="pastEvents"
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
