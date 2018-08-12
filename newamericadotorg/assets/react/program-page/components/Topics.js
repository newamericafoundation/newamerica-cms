import './Topics.scss';

import { NAME } from '../constants';
import { Link, BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
import React, { Component } from 'react';
import { Fetch, Response } from  '../../components/API';
import { PersonsList } from '../../components/People';
import { PublicationListItem } from '../../components/ContentCards';
import CardSm from './CardSm';

const Breadcrumbs = ({ ancestors }) => (
  <div className="program__topic__breadcrumbs">
    {ancestors.map((t,i)=>(
      <h6 key={`crumb-${i}`} className="program__topic__breadcrumbs__crumb inline">
        <Link to={t.url}>{t.title}</Link><span>/</span>
      </h6>
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
    <div className="section-separator__text"><h6 className="inline">{text}</h6></div>
    <div className="section-separator__line"></div>
  </div>
);

class PublicationsList extends Component {
  render(){
    let { response: { results, hasNext, isFetching }, topic, program } = this.props;
    if(results.length===0 || isFetching) return null;
    return (
      <div className="program__topic__publications">
        <Separator text="Recent Publications" />
        {results.map((p,i)=>(
          <PublicationListItem key={`post-${i}`} post={p} key={`publication-${i}`} />
        ))}
        {hasNext &&
          <div className="program__topic__publications__view-all margin-top-15">
            <Link className="button--text" to={`/${program.slug}/publications/?topicId=${topic.id}`}>View All</Link>
          </div>}
      </div>
    );
  }
}

const Featured = ({ publications }) => (
  <div className="topic__featured-publications">
    <Separator text="Featured Publications" />
    <div className="row gutter-10">
      {publications.map((p,i)=>(
        <div className="col-12 col-md-4" key={`featured-${i}`}>
          <CardSm post={p} />
        </div>
      ))}
    </div>
  </div>
);

const PersonsListWrapper = (props) => {
  if(props.response.isFetching) return null
  return <PersonsList {...props} />
}

export class Topic extends Component {

  componentWillMount(){
    if(window.scrollY > 300 || window.pageYOffset > 300) window.scrollTo(0, 245);
  }

  render(){
    let { ancestors, topic, program, match } = this.props;
    return(
      <div className="program__topic">
        {ancestors.length > 0 && <Breadcrumbs program={program} ancestors={ancestors} />}
        <h1 className="margin-bottom-35">{topic.title}</h1>
        <Subtopics program={program} subtopics={topic.subtopics} />
        {topic.body && <Body body={topic.body} />}
        <Fetch name={`${NAME}.topic.authors`}
            key={`${match.path}-authors`}
            endpoint="author"
            fetchOnMount={true}
            component={PersonsListWrapper}
            renderIfNoResults={false}
            initialQuery={{
              topic_id: topic.id,
              include_fellows: true
            }}>
            <Separator text="Topic Experts" />
          </Fetch>
          {topic.featured_publications.length > 0 &&
            <Featured publications={topic.featured_publications} />
          }
          <Fetch name={`${NAME}.topic.publications`}
              key={`${match.path}-pubs`}
              endpoint="post"
              fetchOnMount={true}
              component={PublicationsList}
              topic={topic}
              program={program}
              initialQuery={{
                page_size: 4,
                topic_id: topic.id,
                image_rendition: 'fill-300x230'
              }}/>
      </div>
    );
  }
}

export class TopicRoutes extends Component {
  topicRoutes = (topics, ancestors=[]) => {
    if(!topics) return;
    let { program } = this.props;
    let routes = [];
    topics.map((t,i)=>{
      routes.push(
        <Route exact path={t.url} key={`${t.slug}-${i}`} render={(props)=>(
            <Topic {...props} program={program} ancestors={ancestors} topic={t}/>
        )}/>
      );
      let subtopics = this.topicRoutes(t.subtopics, [...ancestors, t]);
      routes = routes.concat(subtopics);
    });
    return routes;
  }

  render() {
    let { response: { results }} = this.props;
    let routes = this.topicRoutes(results);
    return (
      <div className="program__topics-wrapper">
        {routes}
      </div>
    );
  }
}

export class TopicDetail extends Component {
  render(){
    return (
      <Response name={`${NAME}.topics`} component={TopicRoutes} program={this.props.program} />
    );
  }
}

class Topics extends Component {

  render(){
    let { program, response: { results }, root } = this.props;

    return (
      <div className="program__topics-wrapper">
          <Route path={`/${root}/topics/`} exact render={()=>(
            <div className="program__topics menu-list with-arrow--right margin-top-35">
              {results.sort((a,b) => a.title > b.title ? 1 : -1).map((topic,i)=>(
                <h2 key={`topic-${i}`}>
                  <Link to={topic.url}>{topic.title}</Link>
                  <div className="icon-arrow">
                    <div />
                    <div />
                    <div />
                  </div>
                </h2>
              ))}
            </div>
          )}/>
      </div>
    );
  }
}

export class TopicsList extends Component {

  render(){
    let { program, root } = this.props;

    return (
      <Response name={`${NAME}.topics`} component={Topics} program={program} root={root}/>
    );
  }
}
