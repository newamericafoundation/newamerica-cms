import { NAME, ID } from './constants';
import { Component } from 'react';
import PropTypes from 'prop-types';
import { Fetch } from '../components/API';
import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
import Publications from './components/Publications';
import Nav from './components/Nav';
import Heading from './components/Heading';
import About from './components/About';
import Events from './components/Events';
import StoryGrid from './components/StoryGrid';
import People from './components/People';
import Subprograms from './components/Subprograms';
import { TopicsList, Topic } from './components/Topics';

class ProgramPage extends Component {
  routes = () => {
  }
  topicRoutes = (topics, ancestors=[]) => {
    if(!topics) return;
    let { response: { results }} = this.props;
    let routes = [];

    topics.map((t,i)=>{
      routes.push(
        <Route path={t.url} exact render={(props)=>(
          <Topic {...props} program={results} ancestors={ancestors} topic={t}/>
        )} />
      );
      let subtopics = this.topicRoutes(t.subtopics, [...ancestors, t]);
      routes = routes.concat(subtopics);
    });

    return routes;
  }

  render(){
    let { response: { results }, programType } = this.props;
    let root = programType == 'program' ? ':program' : ':program/:subprogram';
    return (
      <div className="container">
        <Router>
          <div className="program__content">
            <Heading program={results} />
            <Route path={`/${root}/:subpage?`} render={(props)=>(<Nav {...props} program={results}/>)}/>
            <Route path={`/${root}/`} exact render={()=>(<StoryGrid story_grid={results.story_grid} />)} />
            {results.about && <Route path={`/${root}/about`} render={()=>(<About about={results.about} />)} /> }
            <Route path={`/${root}/our-people/`} render={(props)=>(<People programType={programType} {...props} program={results} /> )} />
            <Route path={`/${root}/events/`} render={(props)=>(<Events programType={programType} {...props} program={results} /> )} />
            <Route path={`/${root}/subprograms/`} render={(props)=>(<Subprograms {...props} program={results} /> )} />
            <Route path={`/${root}/publications/`} render={(props)=>(<Publications programType={programType} {...props} program={results} /> )} />
            {results.content_types.map((c,i)=>(
              <Route path={`/${root}/${c.slug}/`} render={(props)=>(<Publications {...props} program={results} /> )} />
            ))}
            {results.topics &&
              <Route path={`/${root}/topics/`} exact render={(props)=>(<TopicsList {...props} program={results} /> )} />}
            {this.topicRoutes(results.topics)}
          </div>
        </Router>
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
