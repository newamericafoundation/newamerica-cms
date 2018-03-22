import { BrowserRouter as Router, Route } from 'react-router-dom';
import { Component } from 'react';
import { Fetch } from '../components/API';
import { NAME, ID } from './constants';
import Nav from './components/Nav';
import InfiniteLoadMore from '../components/InfiniteLoadMore';
import { PersonsList } from '../components/People';
import DocumentMeta from 'react-document-meta';

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
        bottomOffset={-document.documentElement.clientHeight*0.75}>
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
      default:
        return false;
    }
  }

  query = () => {
    let { match : { params : { peoplePage } } } = this.props
    let q = {
      page_size: 6,
      page: 1
    };

    let role = this.getRole();
    if(role) q.role = role;
    if(peoplePage==='leadership') q.leadership = true;
    if(peoplePage==='board-emeriti') q.former = true;

    return q;
  }

  render(){
    let { match } = this.props;
    let leadership = match.params.peoplePage == 'leadership' ? true : null;
    let former = match.params.peoplePage == 'board-emeriti';
    let role = this.getRole();
    let title = this.getTitle();
    return (
      <DocumentMeta title={`Our People${title ? ': ' + title : ''}`}>
        <section className="home__panel__promo home__panel__our-people">
          <div className="container">
            <Nav />
            <Fetch name={NAME}
              endpoint={'author'}
              fetchOnMount={true}
              eager={true}
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
      <Router>
        <Route path="/:peoplePage?/" component={OurPeople}/>
      </Router>
    );
  }
}


export default { APP, NAME, ID };
