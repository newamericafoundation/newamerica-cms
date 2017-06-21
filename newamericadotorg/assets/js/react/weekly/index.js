import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
import { CSSTransitionGroup } from 'react-transition-group'
import { Component } from 'react';
import { connect } from 'react-redux';
import { Fetch, Response } from '../components/API';
import { NAME, ID } from './constants';
import Article from './components/Article';
import EditionGrid from './components/EditionGrid';
import Header from './components/Header';
import ScrollToTop from './components/ScrollToTop';

const EditionGridList = ({ edition }) => (
  <section className="weekly-edition-grid-list container">
    <EditionGrid edition={edition} />
  </section>
);

class Routes extends Component {
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
                render={()=>(<EditionGridList edition={edition}/>)}/>
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
  render() {
    let { latestEdition } = this.props;

    return (
      <Router>
        <Route path="/weekly/:edition?/:article?" render={({ location, match }) => (
          <Fetch
            name={NAME}
            endpoint='weekly'
            fetchOnMount={true}
            component={Routes}
            location={location}
            match={match}
            initialQuery={{
              offset: latestEdition - this.getEdition(match)
            }}/>
          )}/>
      </Router>
    );
  }
}

export default { APP, NAME, ID };
