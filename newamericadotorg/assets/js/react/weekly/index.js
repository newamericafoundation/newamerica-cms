import { BrowserRouter as Router, Route, Switch, Redirect, Link } from 'react-router-dom';
import { CSSTransition, TransitionGroup } from 'react-transition-group'
import { Component } from 'react';
import { connect } from 'react-redux';
import { Fetch, Response } from '../components/API';
import { NAME, ID } from './constants';
import getNestedState from '../../utils/get-nested-state';
import LoadingIcon from '../components/LoadingIcon';
import Article from './components/Article';
import Edition from './components/Edition';
import EditionList from './components/EditionList';
import Header from './components/Header';
import ScrollToTop from './components/ScrollToTop';

const Slide = ({children, ...props}) => (
  <CSSTransition
    {...props}
    classNames="weekly-slide"
    onExiting={(el, isAppearing) => {
      // if(el.classList.contains('weekly-edition')){
      //   el.scrollTop = window.scrollY + 65 - 75;
      //   console.log(window.scrollY);
      // }
    }}
    timeout={600}>
    {children}
  </CSSTransition>
);

class Routes extends Component {
  render(){
    let { response: { results }, location, match } = this.props;
    return (
      <main>
        <Route path="/weekly/:editionSlug/:articleSlug?" render={(props)=>(<Header {...props} edition={results} />)} />
        <TransitionGroup className="weekly-slide-wrapper">
          <Slide key={match.params.articleSlug ? 'article' : 'edition'}>
            <Switch location={location}>
              <Route
                path="/weekly/:editionSlug/:articleSlug/"
                render={(props)=>(
                  <Article edition={results} {...props} />
                )}/>
              <Route
                path="/weekly/:editionSlug/"
                render={(props)=>(
                  <Edition edition={results} {...props} />
                )}/>
            </Switch>
          </Slide>
        </TransitionGroup>
      </main>
    );
  }
}

class APP extends Component {
  render() {
    let { editionId, editionSlug } = this.props;
    return (
      <Router>
        <Switch>
          <Route path="/weekly/" exact render={(props) => (
            <Redirect to={`/weekly/${editionSlug}/`} />
          )} />
          <Route path="/weekly/:editionSlug?/:articleSlug?/" render={({ location, match }) => (
              <Fetch name='weekly.edition'
                endpoint={`weekly/${editionId}`}
                fetchOnMount={true}
                eager={true}
                component={Routes}
                location={location}
                match={match}/>
            )}/>
        </Switch>
      </Router>
    );
  }
}

export default { APP, NAME, ID };
