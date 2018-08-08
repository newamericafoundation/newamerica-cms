import './index.scss';

import { BrowserRouter as Router, Route } from 'react-router-dom';
import React, { Component } from 'react';
import { Fetch } from '../components/API';
import { NAME, ID } from './constants';
import HorizontalNav from '../components/HorizontalNav';
import InfiniteLoadMore from '../components/InfiniteLoadMore';
import { PersonsList } from '../components/People';
import DocumentMeta from 'react-document-meta';
import GARouter from '../ga-router';

class InfinitePersonsList extends Component {
  nextPage = () => {
    let { setQueryParam, fetchAndAppend, response } = this.props;
    if(!response.hasNext) return false;

    setQueryParam('page', response.page+1);
    return fetchAndAppend;
  }

  render(){
    let { results, hasNext, isFetching, page } = this.props.response;
    return (
      <InfiniteLoadMore
        onNextPage={this.nextPage}
				response={this.props.response}
        infiniteOnMount={true}
        bottomOffset={-document.documentElement.clientHeight*0.5}>
        <PersonsList response={this.props.response} />
      </InfiniteLoadMore>
    );
  }
}


class OurPeople extends Component {
  getRole = () => {
    let { match: { params }} = this.props;
    switch(params.peoplePage){
      case 'board':
      case 'board-emeriti':
        return 'Board Member';
      case 'program-staff':
        return 'Program Staff';
      case 'central-staff':
        return 'Central Staff';
      case 'our-fellows':
        return false;
      default:
        return false;
    }
  }

  getTitle = () => {
    let { match: { params }} = this.props;
    switch(params.peoplePage){
      case 'board':
        return 'Board of Directors';
      case 'board-emeriti':
        return 'Board Emeriti';
      case 'program-staff':
        return 'Program Staff';
      case 'central-staff':
        return 'Central Staff';
      case 'leadership':
        return 'Leadership';
      case 'our-fellows':
        return 'Fellows';
      default:
        return false;
    }
  }

  query = () => {
    let { match : { params : { peoplePage } } } = this.props
    let q = {
      page_size: 12,
      page: 1
    };

    let role = this.getRole();
    if(role) q.role = role;
    if(peoplePage==='our-people') q.include_fellows = true;
    if(peoplePage==='leadership') q.leadership = true;
    if(peoplePage==='board-emeriti') q.former = true;

    return q;
  }

  render(){
    let { match } = this.props;
    let title = this.getTitle();
    let endpoint = title == 'Fellows' ? 'fellow' : 'author';
    return (
      <DocumentMeta title={`Our People${title ? ': ' + title : ''}`}>
        <section className="beige home__panel__our-people">
          <div className="container">
            <HorizontalNav items={[
              { url: '/our-people/', label: 'All People'},
              { url: '/board/', label: 'Board of Directors' },
              { url: '/leadership/', label: 'Leadership' },
              { url: '/program-staff/', label: 'Program Staff' },
              { url: '/our-fellows/', label: 'Fellows' },
              { url: '/central-staff/', label: 'Central Staff' },
              { url: '/board-emeriti/', label: 'Board Emeriti' }
            ]}/>
            <Fetch name={NAME}
              endpoint={endpoint}
              fetchOnMount={true}
              eager={true}
              loadingState={<PersonsList response={{ results: [{},{},{},{},{},{},{},{},{},{},{}]}} />}
              component={InfinitePersonsList}
              initialQuery={this.query()}/>
            </div>
        </section>
      </DocumentMeta>
    );
  }
}


class APP extends Component {
  render(){
    return (
      <GARouter>
        <Route path="/:peoplePage?/" component={OurPeople}/>
      </GARouter>
    );
  }
}


export default { APP, NAME, ID };
