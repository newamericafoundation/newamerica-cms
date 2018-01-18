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
import { TopicsList, Topic } from './components/Topics';

class ProgramPage extends Component {
  topicRoutes = (topics, ancestors=[]) => {
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
    let { response: { results }, programId } = this.props;
    return (
      <div className="container">
        <Router>
          <div className="program__content">
            <Heading program={results} />
            <Route path='/:program/:subpage?' render={(props)=>(<Nav {...props} program={results}/>)}/>
            <Route path='/:program/' exact render={()=>(<StoryGrid story_grid={results.story_grid} />)} />
            <Route path='/:program/about' render={()=>(<About about={results.about} />)} />
            <Route path='/:program/our-people/' render={(props)=>(<People {...props} program={results} /> )} />
            <Route path='/:program/events/' render={(props)=>(<Events {...props} program={results} /> )} />
            <Route path='/:program/topics/' exact render={(props)=>(<TopicsList {...props} program={results} /> )} />
            {this.topicRoutes(results.topics)}
            <Route path='/:program/publications/' render={(props)=>(<Publications {...props} program={results} /> )} />
            {results.content_types.map((c,i)=>(
              <Route path={`/:program/${c.slug}/`} render={(props)=>(<Publications {...props} program={results} /> )} />
            ))}
          </div>
        </Router>
      </div>
    );
  }
}

class APP extends Component {
  static propTypes = {
    programId: PropTypes.string.isRequired
  }

  render() {
    let { programId } = this.props;
    return (
      <Fetch component={ProgramPage}
        name={NAME}
        endpoint={`program/${programId}`}
        fetchOnMount={true}
        programId={programId}
      />
    );
  }
}

export default { NAME, ID, APP };
