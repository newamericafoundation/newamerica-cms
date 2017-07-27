import { NAME, ID } from './constants';
import { Component } from 'react';
import { BrowserRouter as Router, Link, Route } from 'react-router-dom';
import { Fetch, Response } from '../components/API';
import Topic from './components/Topic';


const TopicRoutes = ({ match, topic, ancestors }) => {
  return (
    <div>
      <Route exact path={match.url} render={(props)=>(<Topic topic={topic} ancestors={ancestors} />)} />
      <Route path={`${match.url}/:slug`} render={({ match })=>(
        <TopicRoutes match={match}
          ancestors={[...ancestors, topic]}
          topic={topic.subtopics.find((s)=>(s.slug==match.params.slug))} />
      )} />
    </div>
  );
}


class Routes extends Component {
  render() {
    let { response : { results } } = this.props;
    let re = new RegExp(`\/${results.program.slug}\/(.+)\/.+`, 'i');
    let match = window.location.href.match(re);
    return (
       <Router>
        <TopicRoutes ancestors={[]} topic={results} match={{
          params: { slug: results.slug, program: results.program.title },
          url: `/${results.program.slug}/${match[1]}/${results.slug}`
        }} />
      </Router>
    );
  }
}

class APP extends Component {
  render(){
    let { parentTopicId } = this.props;
    return (
      <Fetch name={NAME + '.topics'}
        endpoint={`topic/${parentTopicId}`}
        component={Routes}
        fetchOnMount={true} />
    );
  }
}


export default { APP, NAME, ID };
