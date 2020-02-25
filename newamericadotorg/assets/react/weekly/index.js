import './index.scss';

import { BrowserRouter as Router, Route, Switch, Redirect, Link } from 'react-router-dom';
import { CSSTransition, TransitionGroup } from 'react-transition-group'
import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Fetch, Response } from '../components/API';
import { NAME, ID } from './constants';
import getNestedState from '../../lib/utils/get-nested-state';
import LoadingIcon from '../components/LoadingIcon';
import Article from './components/Article';
import ArticleListing from './components/ArticleListing';
import Header from './components/Header';
import ScrollToTop from './components/ScrollToTop';
import bowser from 'bowser';
import GARouter from '../ga-router';
import store from '../store';
import { setResponse } from '../api/actions';

const browser = bowser.getParser(window.navigator.userAgent);
const isValidBrowser = browser.satisfies({
  macos: {
    chrome: '>57'
  },
  mobile: {
    chrome: '>57'
  }
});

const Slide = ({children, ...props}) => (
  <CSSTransition
    {...props}
    classNames="weekly-slide"
    timeout={600}>
    {children}
  </CSSTransition>
);

class Routes extends Component {
  constructor(props){
    super(props);
    this.state = {
      mounted: false
    }
  }
  componentDidMount(){
    this.setState({ mounted: true });
  }
  render(){
    let { response: { results }, location, match } = this.props;
    return (
      <main className={`${isValidBrowser ? 'transition-enabled' : ''}`}>
        <Route path="/weekly/:articleSlug?" render={(props)=>(
          <Header dispatch={this.props.dispatch} {...props} articles={results} />
        )} />
        <TransitionGroup className="weekly-slide-wrapper">
          <Slide key={match.params.articleSlug ? 'article' : 'index'}>
            <Switch location={location}>
              <Route
                path="/weekly/:articleSlug/"
                exact
                render={(props)=>(
                  <Article articles={results} {...props} />
                )}/>
              <Route
                path="/weekly/"
                exact
                render={(props)=>(
                  <ArticleListing transition={this.state.mounted} articles={results} {...props} />
                )}/>
            </Switch>
          </Slide>
        </TransitionGroup>
      </main>
    );
  }
}

class APP extends Component {
  componentDidMount(){
    if(window.initialState){
      store.dispatch(setResponse('weekly', {
        page: 1,
        hasNext: false,
        hasPrevious: false,
        count: 0,
        results: window.initialState
      }));
    }
  }
  render() {
    return (
      <GARouter>
        <Switch>
          <Route path="/admin/pages/" render={(props) => (
            <Redirect to="/weekly/" />
          )} />
          <Route path="/weekly/:articleSlug?/" render={({ location, match }) => {
            if(window.initialState) return <Response location={location} match={match} name='weekly' component={Routes} />
              return <Fetch name='weekly'
                endpoint="weekly"
                fetchOnMount={true}
                eager={true}
                component={Routes}
                location={location}
                match={match}/>
            }}/>
        </Switch>
      </GARouter>
    );
  }
}

export default { APP, NAME, ID };
