import { BrowserRouter as Router, Route, Switch, Redirect, Link } from 'react-router-dom';
import { CSSTransitionGroup } from 'react-transition-group'
import { Component } from 'react';
import { connect } from 'react-redux';
import { Fetch, Response } from '../components/API';
import { NAME, ID } from './constants';
import Article from './components/Article';
import EditionGrid from './components/EditionGrid';
import Header from './components/Header';
import ScrollToTop from './components/ScrollToTop';
import actions from '../actions';

class Routes extends Component {
  isFetching = false;
  getNextEdition = (edition) => {
    let { response: { results, hasNext, count }, setQueryParam, offset, fetchAndAppend } = this.props;
    let index = results.indexOf(edition);
    let nextEdition = results[index+1];
    if(nextEdition) return nextEdition;
    if(offset+3>count) return null;
    if(!this.isFetching && hasNext){
      this.isFetching = true;
      setQueryParam('offset', offset+3);
      fetchAndAppend(()=>{ this.isFetching = false });
      return undefined;
    }
    return nextEdition;
  }

  getPrevEdition = (edition) => {
    let { response: { results, hasPrevious }, setQueryParam, offset, fetchAndPrepend } = this.props;
    let index = results.indexOf(edition);
    let prevEdition = results[index-1];
    if(prevEdition) return prevEdition;
    if(offset===0) return null;
    if(!this.isFetching && hasPrevious){
      this.isFetching = true;
      setQueryParam('offset', offset-3);
      fetchAndPrepend(()=>{ this.isFetching = false });
      return undefined;
    }
  }

  getEdition = (editionSlug) => {
    let { response: { results }} = this.props;
    return results.find((e)=>(e.slug==editionSlug)) || results[0];
  }

  getArticle = (edition, articleSlug) => {
    return edition.articles.find((a)=>(a.slug==articleSlug));
  }

  render(){
    let { response: { results }, location, match } = this.props;
    let edition = this.getEdition(match.params.edition);

    return (
      <div>
      {results.length &&
        <div>
          <ScrollToTop location={location} />
          <Header page={match.params.article ? 'article' : 'edition' }/>
          <Route exact path="/weekly" render={()=>(<Redirect to={`/weekly/${edition.slug}`}/>)} />
          <CSSTransitionGroup
            transitionName="weekly-page-fade"
            transitionEnterTimeout={500}
            transitionLeaveTimeout={300}>
            <Switch key={location.key} location={location}>
              <Route exact
                path="/weekly/:edition"
                render={()=>(
                  <EditionGrid edition={edition}/>
                )}/>
              <Route exact
                path="/weekly/:edition/:article"
                render={(props)=>{
                  return <Article article={this.getArticle(edition, props.match.params.article)} />
                }}/>
            </Switch>
          </CSSTransitionGroup>
        </div>}</div>
    );
  }
}

class APP extends Component {
  getEdition = (match) => {
    let { params: { edition }} = match;
    if(!edition) return +this.props.latestEdition;
    if(!isNaN(edition)) return +edition;
    return +match.params.edition.split('-')[1];
  }

  getOffset = (match) => {
    let { latestEdition } = this.props;
    let edition = this.getEdition(match);
    return Math.floor((latestEdition - edition)/3)*3
  }

  render() {
    let { latestEdition } = this.props;

    return (
      <Router>
        <Route path="/weekly/:edition?/:article?" render={({ location, match }) => {
          let offset = this.getOffset(match);
          return <Fetch
            name={NAME}
            endpoint='weekly'
            fetchOnMount={true}
            component={Routes}
            location={location}
            offset={offset}
            match={match}
            initialQuery={{
              offset
            }}/>
          }}/>
      </Router>
    );
  }
}

export default { APP, NAME, ID };
