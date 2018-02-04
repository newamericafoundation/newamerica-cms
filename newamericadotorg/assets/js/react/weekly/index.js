import { BrowserRouter as Router, Route, Switch, Redirect, Link } from 'react-router-dom';
import { CSSTransitionGroup } from 'react-transition-group'
import { Component } from 'react';
import { connect } from 'react-redux';
import { Fetch, Response } from '../components/API';
import { NAME, ID } from './constants';
import getNestedState from '../../utils/get-nested-state';
import LoadingIcon from '../components/LoadingIcon';
import Article from './components/Article';
import EditionGrid from './components/EditionGrid';
import Header from './components/Header';
import Preload from './components/Preload';
import LoadingPage from './components/LoadingPage';
import ScrollToTop from './components/ScrollToTop';
import * as REDUCERS from './reducers';


class ArticleResponse extends Component {
  getArticle = () => {
    let edition = this.props.response.results;
    let articleSlug = this.props.match.params.article;
    return edition.articles.find((a)=>(a.slug==articleSlug));
  }

  render(){
    let { response: { results }, dispatch } = this.props;
    return(
      <Article article={this.getArticle()} edition={results} dispatch={dispatch} />
    );
  }
}

class EditionResponse extends Component {
  render(){
    let { response: { results }, dispatch } = this.props;
    return <EditionGrid edition={results} dispatch={dispatch} />
  }
}

const Loading = () => (
  <div className="weekly-loading-icon">
    <LoadingIcon />
  </div>
);

const Main = ({ location, match }) => (
  <CSSTransitionGroup
    transitionName="weekly-page-fade"
    transitionEnterTimeout={1850}
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
    let { response: { results }, location, match, isReady } = this.props;
    let edition = this.getEdition(match.params.edition);
    return (
      <div>
        <Preload match={match}/>
        {/* <ScrollToTop location={location} /> */}
        {edition && <Route path="/weekly" render={()=>(
            <Fetch name="weekly.edition"
              endpoint={`weekly/${edition.id}`}
              fetchOnMount={true}
              eager={true} />
          )}/>
        }
        <Route path="/weekly/:edition" render={()=>(<Header isArticle={match.params.article ? true : false}/>)} />
        {isReady && <Main location={location} match={match}/>}
        {!isReady && <Route path="/weekly/:edition" component={Loading}/> }
      </div>
    );
  }
}

Routes = connect((state)=>({
  isReady: getNestedState(state, 'weekly.edition.isReady')
}))(Routes);

class APP extends Component {
  render() {
    return (
      <Router>
        <main>
          <Route exact path="/weekly" component={LoadingPage} />
          <Route path="/weekly/:edition?/:article?" render={({ location, match }) => (
              <Fetch name='weekly.editionList'
                endpoint='weekly'
                fetchOnMount={true}
                component={Routes}
                location={location}
                match={match}/>
            )}/>
        </main>
      </Router>
    );
  }
}

export default { APP, NAME, ID, REDUCERS };
