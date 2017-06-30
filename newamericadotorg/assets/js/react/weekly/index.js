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

class ArticleResponse extends Component {
  getArticle = () => {
    let edition = this.props.response.results;
    let articleSlug = this.props.match.params.article;
    return edition.articles.find((a)=>(a.slug==articleSlug));
  }

  render(){
    let edition = this.props.response.results;
    return(
      <Article article={this.getArticle()} edition={edition} />
    );
  }
}

const EditionResponse = ({ response: { results }, key }) => (
  <EditionGrid edition={results} key={key} />
);

const Main = ({ location, match }) => (
  <CSSTransitionGroup
    transitionName="weekly-page-fade"
    transitionEnterTimeout={800}
    transitionLeaveTimeout={800}>
    <Switch key={match.params.article ? 'article' : 'edition'} location={location}>
      <Route exact
        path="/weekly/:edition"
        render={()=>(
          <Response name="weekly.edition" component={EditionResponse}/>
        )}/>
      <Route exact
        path="/weekly/:edition/:article"
        render={(props)=>(
          <Response name="weekly.edition" match={props.match} component={ArticleResponse}/>
        )}/>
    </Switch>
  </CSSTransitionGroup>
);

class Routes extends Component {

  getEdition = (editionSlug) => {
    let { response: { results }} = this.props;
    return results.find((e)=>(e.slug==editionSlug)) || results[0];
  }

  render(){
    let { response: { results }, location, match } = this.props;
    let edition = this.getEdition(match.params.edition);

    return (
      <div>
      {results.length &&
        <div>
          <ScrollToTop location={location} />
          <Header />
          <Route exact path="/weekly" render={()=>(<Redirect to={`/weekly/${edition.slug}`}/>)} />
          <Route path="/weekly/:edition" render={()=>(
            <Fetch name="weekly.edition"
              endpoint={`weekly/${edition.id}`}
              fetchOnMount={true} />
          )}/>
          <Main location={location} match={match}/>
        </div>}</div>
    );
  }
}

class APP extends Component {
  render() {
    return (
      <Router>
        <Route path="/weekly/:edition?/:article?" render={({ location, match }) => (
            <Fetch name='weekly.editionList'
              endpoint='weekly'
              fetchOnMount={true}
              component={Routes}
              location={location}
              match={match}/>
          )}/>
      </Router>
    );
  }
}

export default { APP, NAME, ID };
