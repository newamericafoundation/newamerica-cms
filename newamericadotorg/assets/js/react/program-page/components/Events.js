import { NAME } from '../constants';
import { Component } from 'react';
import { Fetch } from '../../components/API';
import { format as formatDate } from 'date-fns';
import { PublicationsList, LoadingDots } from './Publications';
import { Filter } from './PublicationsFilters';
import { NavLink } from 'react-router-dom';
import ScrollArea from 'react-scrollbar';

const EventItem = ({ event }) => (
  <div className="card event">
    <a href={event.url}>
      <div className={`card__image ${!event.story_image ? 'no-image' : ''}`}>
        <img className="card__image__background" src={event.story_image} />
      </div>
    </a>
    <div className="card__text">
      <a href={event.url}>
        <label className="margin-top-0 block">{formatDate(event.date, 'MMM. Do, YYYY')}</label>
        <label className="card__text__title bold block">{event.title}</label>
        <label className="subtitle block">{event.story_excerpt}</label>
        <label className="caption block">{event.city}, {event.state}</label>
      </a>
      <label className="event__rsvp button--text block margin-0">
        <a href={event.url}>RSVP</a>
      </label>
    </div>
  </div>
);

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
  state = { lastScrollPosition: 0, isLoadingMore: true }

  componentDidMount(){
    this.reloadScrollEvents();
  }

  componentDidUpdate(prevProps){
    let { location, program, setQuery, response } = this.props;

    if(location !== prevProps.location){
      this.reloadScrollEvents();
      if(window.scrollY > 300){
        window.scrollTo(0, 300);
      }
      // if(+document.body.style.top.replace('px', '') < -365){
      //   this.state.lastScrollPosition = 365;
      //   this.enableScroll();
      //   this.disableScroll(false);
      // }

    }
  }

  disableScroll = (update) => {
    // if(update !== false) this.state.lastScrollPosition = this.props.windowScrollPosition;
    // document.body.classList.add('scroll-disabled');
    // document.body.style.top = -this.state.lastScrollPosition + 'px';
  }

  enableScroll = () => {
    // document.body.classList.remove('scroll-disabled');
    // document.body.style.top = '';
    // window.scrollTo(0, this.state.lastScrollPosition);
  }

  reloadScrollEvents(){
    this.props.dispatch({
      type: 'RELOAD_SCROLL_EVENTS',
      component: 'site'
    });
  }

  render(){
    let { program, response } = this.props;

    return (
      <div className={`program__publications-filters scroll-target`}
        data-scroll-top-offset="-15"
        onMouseEnter={this.disableScroll}
        onTouchStart={this.disableScroll}
        onMouseLeave={this.enableScroll}
        onTouchEnd={this.enableScroll}>
        <div className={`program__publications-filters__sticky-wrapper ${response.isFetching ? 'is-fetching' : ''}`}>
          <ScrollArea className="program__publications-filters__scroll-area">
            <AbstractFilter {...this.props} label="Date" />
            {program.subprograms && <AbstractFilter {...this.props} label="Subprogram" />}
            {program.topics && <AbstractFilter {...this.props} label="Topic" />}
          </ScrollArea>
        </div>
      </div>
    )
  }
}

class Past extends Component {
  render(){
    return (
      <div className="program__publications row gutter-45 scroll-target margin-top-35" data-scroll-trigger-point="bottom" data-scroll-bottom-offset="65">
        <div className="col-3 program__publications__filter-col">
          <Filters {...this.props}/>
        </div>
        <div className='col-9 program__publications__list-col'>
          <PublicationsList {...this.props}/>
        </div>
      </div>
    );
  }
}

class EventsList extends Component {
  activeStyle = {
    fontWeight: 'bold',
    fontStyle: 'italic'
  }
  shouldComponentUpdate(nextProps){
    let { location, setQuery } = this.props
    if(location !== nextProps.location){
      let period = new URLSearchParams(nextProps.location.search.replace('?', '')).get('period') || 'future';
      setQuery({
        time_period: period,
        page: 1,
        image_rendition: period=='future' ? 'min-700x510' : 'max-300x240'
      }, true);
      return false;
    }

    return true;
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

export default class Events extends Component {
  render(){
    let { program, location, programType } = this.props;
    let params = new URLSearchParams(location.search.replace('?', ''));
    let period = params.get('period') || 'future';

    return (
      <Fetch name={`${NAME}.events`}
        component={EventsList}
        endpoint="event"
        fetchOnMount={true}
        period={period}
        location={location}
        program={program}
        initialQuery={{
          subprogram_id: params.get('subprogramId') || '',
          [programType == 'program' ? 'program_id' : 'subprogram_id']: program.id,
          time_period: period,
          page_size: 6,
          page: 1,
          image_rendition: period=='future' ? 'fill-700x510' : 'fill-300x240'
        }}/>
    );
  }
}
