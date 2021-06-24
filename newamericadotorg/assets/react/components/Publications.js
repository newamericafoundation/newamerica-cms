import './Publications.scss';

import React, { Component, cloneElement } from 'react';
import { connect } from 'react-redux';
import { LoadingDots } from './Icons';
import { PublicationListItem, Person, EventItem } from './ContentCards';
import { Link } from 'react-router-dom';

export class PublicationsList extends Component {
  loadMore = () => {
    let { fetchAndAppend, setQuery, response } = this.props;
    if(!response.hasNext || response.isFetching) return;
    this.isLoadingMore = true;
    setQuery(response.nextParams);
    fetchAndAppend(this.triggerScrollEvents);
  }

  triggerScrollEvents = () => {
    setTimeout(()=>{
      this.isLoadingMore = false;
      this.props.dispatch({
        type: 'TRIGGER_SCROLL_EVENTS',
        component: 'site'
      });
    });
  }

  render(){
    let { response, fetchAndAppend, card_type } = this.props;
    let { results, isFetching, hasNext } = response;
    if(results.length===0 && !isFetching){
      if(card_type == 'future_events'){
        return (
          <div className="margin-top-60 centered">
            <h6 className="inline">No upcoming events. </h6>
            <h5 className="link">
              <Link to={{ search: '?period=past' }}>See past events</Link>
            </h5>
            .
          </div>
        );
      }
      return (
        <h4 className="centered">No results found</h4>
      );
    }

    if(isFetching && !this.isLoadingMore){
      return (
        <div className="program__publications-list-wrapper">
          <div className="program__publications-list margin-top-60">
              <LoadingDots />
          </div>
        </div>
      );
    }

    return (
      <div className="program__publications-list-wrapper">
        <div className="program__publications-list">
            {card_type == 'future_events'
            ? (<div className="program__events__upcoming margin-top-35 row gutter-10">
                {results.map((e, i) => (
                  <div key={`event-${i}`} className="col-md-4 col-12">
                    <EventItem event={e} />
                  </div>
                ))}
              </div>)
            : results.map((post, i ) => {
              if(post.content_type.api_name == 'person')
                return ( <Person key={`post-${i}`} person={post} /> );
              return ( <PublicationListItem key={`post-${i}`} post={post} /> );
            })}
        </div>
        {hasNext &&
        <div className="program__publications-list-load-more margin-top-10">
          <a className={`button${isFetching ? ' is-fetching' : ''}`} onClick={this.loadMore}>
            <span className="load-more-label">Load More</span>
            {isFetching && <span className="loading-dots--absolute">
              <span>.</span><span>.</span><span>.</span>
            </span>}
          </a>
        </div>}
      </div>
    );
  }
}

export class PublicationsWrapper extends Component {
  state = {
    filtersOpen: false
  }


  toggleMobileFilters = () => {
    this.setState({ filtersOpen: !this.state.filtersOpen });
  }
  render(){
    let { filters, publications } = this.props;
    return (
      <div className="program__publications row gutter-45 margin-top-lg-35">
        <div className={`program__publications__open-mobile-filter col-12 margin-top-35`}>
          <a className={`button--text with-caret--${this.state.filtersOpen ? 'up' : 'down'}`}
            onClick={this.toggleMobileFilters}>
            Filters
          </a>
        </div>
        <div className={`col-lg-3 margin-top-5 margin-bottom-15 program__publications__filter-col${this.state.filtersOpen ? ' open' : ''}`}>
          {filters}
        </div>
        <div className='col-12 col-lg-9 program__publications__list-col'>
          {publications}
        </div>
      </div>
    );
  }
}
