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
import bowser from 'bowser';
import GARouter from '../ga-router';

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
      <main class={`${bowser.chrome && bowser.osname == 'macOS' ? 'transition-enabled' : ''}`}>
        <Route path="/weekly/:editionSlug/:articleSlug?" render={(props)=>(
          <Header dispatch={this.props.dispatch} {...props} edition={results} />
        )} />
        <TransitionGroup className="weekly-slide-wrapper">
          <Slide key={match.params.articleSlug ? 'article' : 'edition'}>
            <Switch location={location}>
              <Route
                path="/weekly/:editionSlug/:articleSlug/"
                exact
                render={(props)=>(
                  <Article edition={results} {...props} />
                )}/>
              <Route
                path="/weekly/:editionSlug/"
                exact
                render={(props)=>(
                  <Edition transition={this.state.mounted} edition={results} {...props} />
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
      <GARouter>
        <Switch>
          <Route path="/admin/pages/" render={(props) => (
            <Redirect to={`/weekly/${editionSlug}/`} />
          )} />
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
      </GARouter>
    );
  }
}

export default { APP, NAME, ID };
