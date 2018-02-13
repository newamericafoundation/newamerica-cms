import { NAME } from '../constants';
import { Link, BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
import { Component } from 'react';
import { Fetch } from  '../../components/API';
import { PersonsList } from '../../components/People';
import { PublicationListItem } from '../../components/Publications';

const Breadcrumbs = ({ ancestors }) => (
  <div className="program__topic__breadcrumbs">
    {ancestors.map((t,i)=>(
      <label key={`crumb-${i}`} className="program__topic__breadcrumbs__crumb">
        <Link to={t.url}>{t.title}</Link><span>/</span>
      </label>
    ))}
  </div>
);

const Subtopics = ({ subtopics }) => (
  <div className="program__topic__subtopic">
    {subtopics.map((s,i)=>(
      <Link key={`subtopic-${i}`} className="tag" to={s.url}>{s.title}</Link>
    ))}
  </div>
);

const Body = ({ body }) => (
  <div className="program__topic__body">
    <Separator text="About the Topic" />
    <div className="program__topic__body__text" >
      <div className="post-body" dangerouslySetInnerHTML={{__html: body}}></div>
    </div>
  </div>
);

const Separator = ({ text }) => (
  <div className="section-separator">
    <div className="section-separator__text"><label>{text}</label></div>
    <div className="section-separator__line"></div>
  </div>
);

class PublicationsList extends Component {
  render(){
    let { response: { results, hasNext }, topic, program } = this.props;
    if(results.length===0) return null;
    return (
      <div className="program__topic__publications">
        <Separator text="Related Publications" />
        {results.map((p,i)=>(
          <PublicationListItem key={`post-${i}`} post={p} />
        ))}
        {hasNext &&
          <div className="program__topic__publications__view-all margin-top-15">
            <Link className="button--text" to={`/${program.slug}/publications/?topicId=${topic.id}`}>View All</Link>
          </div>}
      </div>
    );
  }
}

export class Topic extends Component {

  componentWillMount(){
    if(window.scrollY > 300) window.scrollTo(0, 290);
  }

  render(){
    let { ancestors, topic, program } = this.props;

    return(
      <div className="program__topic">
        {ancestors.length > 0 && <Breadcrumbs ancestors={ancestors} />}
        <h1 className="margin-bottom-35">{topic.title}</h1>
        <Subtopics subtopics={topic.subtopics} />
        {topic.body && <Body body={topic.body} />}
        <Fetch name={`${NAME}.topic.authors`}
            endpoint="author"
            fetchOnMount={true}
            component={PersonsList}
            initialQuery={{
              topic_id: topic.id
            }}>
            <Separator text="Topic Experts" />
          </Fetch>
        <Fetch name={`${NAME}.topic.publications`}
            endpoint="post"
            fetchOnMount={true}
            component={PublicationsList}
            topic={topic}
            program={program}
            initialQuery={{
              page_size: 4,
              topic_id: topic.id,
              image_rendition: 'max-300x240'
            }}/>
      </div>
    );
  }
}

export class TopicsList extends Component {
  render(){
    let { program } = this.props;
    return (
      <div className="program__topics menu-list with-arrow--right margin-top-35">
        {program.topics.map((topic,i)=>(
          <h2>
            <Link to={topic.url}>{topic.title}</Link>
            <div className="icon-arrow">
              <div />
              <div />
              <div />
            </div>
          </h2>
        ))}
      </div>
    );
  }
}
