import { NAME, ID } from './constants';
import { Component } from 'react';
import { BrowserRouter as Router, Link, Route } from 'react-router-dom';
import { Fetch, Response } from '../components/API';

const Topic = ({ topic, ancestors }) => {
  return (
    <main>
      <section className="container--wide">
        <div className="breadcrumbs">
          <label className="breadcrumbs__item">
            <a href={topic.program.url}>{topic.program.title}</a>
          </label>
          <label className="breadcrumbs__item">
            <a href={`${topic.program.url}/topic/`}>Topic</a>
          </label>
          {ancestors.map((a,i)=>(
            <label className="breadcrumbs__item">
              <Link to={ a.url }>{ a.title }</Link>
            </label>
          ))}
        </div>
      </section>
      <section className="container--wide topic">
        <h1>{topic.title}</h1>
        {topic.subtopics.length > 0 &&
          <h4 className="narrow-margin topic__subtopic-label">Subtopics</h4>
        }
        {topic.subtopics.map((t,i)=>(
          <Link className="tag with-gutter" to={t.url}>{t.title}</Link>
        ))}
      </section>
    </main>
  );
}

const TopicRoutes = ({ match, topic, ancestors }) => {
  return (
    <div>
      <Route exact path={match.url} render={(props)=>(<Topic topic={topic} ancestors={ancestors} />)} />
      <Route path={`${match.url}/:slug`} render={(props)=>(
        <TopicRoutes match={props.match}
          ancestors={[...ancestors, topic]}
          topic={topic.subtopics.find((s)=>(s.slug==props.match.params.slug))} />
      )} />
    </div>
  );
}


class Routes extends Component {
  render() {
    let { response : { results } } = this.props;
    return (
       <Router>
        <TopicRoutes ancestors={[]} topic={results} match={{
          params: { slug: results.slug, program: results.program.title },
          url: `/${results.program.slug}/topic/${results.slug}`
        }} />
      </Router>
    );
  }
}

class APP extends Component {
  render(){
    let { parentTopicId } = this.props;
    console.log(this.props);
    return (
      <Fetch name={NAME}
        endpoint={`topic/${parentTopicId}`}
        component={Routes}
        fetchOnMount={true} />
    );
  }
}


export default { APP, NAME, ID };
