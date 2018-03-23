/* DocumentMeta defined in ./components/Nav.js */

import { NAME, ID } from './constants';
import { Component } from 'react';
import PropTypes from 'prop-types';
import { Fetch } from '../components/API';
import { Route, Switch, Redirect } from 'react-router-dom';
import GARouter from '../ga-router';
import Publications from './components/Publications';
import Nav from './components/Nav';
import Heading from './components/Heading';
import About from './components/About';
import Events from './components/Events';
import StoryGrid from './components/StoryGrid';
import People from './components/People';
import Subprograms from './components/Subprograms';
import Subscribe from './components/Subscribe';
import { TopicsList, Topic } from './components/Topics';

class ProgramPage extends Component {
  // only transition images on first load
  state = {
    loaded: false
  }
  componentDidMount(){
    setTimeout(()=>{ this.setState({ 'loaded': true }); }, 1500);
  }
  topicRoutes = (topics, ancestors=[]) => {
    if(!topics) return;
    let { response: { results }} = this.props;
    let routes = [];

    topics.map((t,i)=>{
      routes.push(
        <Route key={`${t.slug}-${i}`} path={t.url} exact render={(props)=>(
          <Topic {...props} program={results} ancestors={ancestors} topic={t}/>
        )} />
      );
      let subtopics = this.topicRoutes(t.subtopics, [...ancestors, t]);
      routes = routes.concat(subtopics);
    });

    return routes;
  }

  aboutRoutes = (pages, root) => {
    if(!pages) return;
    let { response: { results }} = this.props;

    return pages.map((p,i) => (
      <Route key={`page-${i}`} path={`/${root}/${p.slug}/`} exact render={(props)=>(<About program={results} about={p} about_us_pages={pages} />)} />
    ));
  }

  contentSlugs = () => {
    let { response: { results }} = this.props;

    if(!results.content_types) return '';
    if(results.content_types.length === 0) return '';
    return '|' + results.content_types.map((c)=>(c.slug)).join('|');
  }

  render(){
    let { response: { results }, programType } = this.props;
    let root = programType == 'program' ? ':program' : ':program/:subprogram';

    return (
      <div className="container">
        <GARouter>
          <div className="program__content">
            <Heading program={results} />
            <Route path={`/${root}/:subpage?`} render={(props)=>(<Nav {...props} program={results}/>)}/>
            <Route path={`/${root}/`} exact render={()=>(<StoryGrid program={results} loaded={this.state.loaded} story_grid={results.story_grid} />)} />
            {results.about && <Route path={`/${root}/about`} exact render={()=>(<About program={results} about={results.about} about_us_pages={results.about_us_pages} />)} /> }
            {this.aboutRoutes(results.about_us_pages, root)}
            <Route path={`/${root}/our-people/`} render={(props)=>(<People programType={programType} {...props} program={results} /> )} />
            <Route path={`/${root}/events/`} render={(props)=>(<Events programType={programType} {...props} program={results} /> )} />
            <Route path={`/${root}/projects/`} render={(props)=>(<Subprograms {...props} program={results} /> )} />
            <Route path={`/${root}/(publications${this.contentSlugs()})/`} render={(props)=>(<Publications programType={programType} {...props} program={results} /> )} />
            {results.topics &&
              <Route path={`/${root}/topics/`} exact render={(props)=>(<TopicsList {...props} program={results} /> )} />}
            {this.topicRoutes(results.topics)}
            <Route path={`/${root}/subscribe/`} render={(props)=>(<Subscribe {...props} subscriptions={results.subscriptions} /> )} />
          </div>
        </GARouter>
      </div>
    );
  }
}

class APP extends Component {
  static propTypes = {
    programId: PropTypes.string.isRequired,
    programType: PropTypes.string.isRequired
  }

  render() {
    let { programId, programType } = this.props;
    return (
      <Fetch component={ProgramPage}
        name={NAME}
        endpoint={`${programType}/${programId}`}
        fetchOnMount={true}
        programType={programType}
      />
    );
  }
}

export default { NAME, ID, APP };
