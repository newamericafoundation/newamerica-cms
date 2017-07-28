import { Link } from 'react-router-dom';
import { Component } from 'react';
import { Author } from '../../components/Content';
import { Fetch } from '../../components/API';
import { NAME } from '../constants';
import ContentList from './ContentList';
import TopicFilter from './TopicFilter';

const AuthorsList = ({ response: { results }}) => {
  return (
    <div className="topic__details__author-list col-4">
      {results.length > 0 && <h4 className="narrow-bottom-margin">Experts</h4>}
      <div className="row no-gutters">
        {results.map((a,i)=>(
          <Author classes="compact" author={a}/>
        ))}
      </div>
    </div>
  );
}

class Topic extends Component {
constructor(props){
  super(props);
  this.state = {
    expanded: false,
    readMore: false
  };
}
componentDidMount(){
  if(this.body.offsetHeight >= 400) this.setState({ readMore: true });
}
toggleReadMore = () => {
  this.setState({ expanded: !this.state.expanded })
}
render(){
    let { topic, ancestors } = this.props;
    return (
      <main className="">
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
        <section className="topic">
          <div className="topic__details container--wide">
            <div className="row">
              <div className="topic__details__text-wrapper col-7">
                  <h1 className="topic__details__title narrow-margin">{topic.title}</h1>
                  <div className="topic__details__subtopics">
                    {topic.subtopics.length > 0 &&
                      <h4 className="narrow-bottom-margin topic__details__subtopic-label">Subtopics</h4>
                    }
                    {topic.subtopics.map((t,i)=>(
                      <Link className="tag with-gutter" to={t.url}>{t.title}</Link>
                    ))}
                  </div>
                  <div className={`topic__details__body ${this.state.expanded ? 'expanded' : ''}`}>
                    <div className="topic__details__body__wrapper"
                      ref={(div)=>{this.body=div;}}
                      dangerouslySetInnerHTML={{__html: topic.body }}></div>
                  </div>
                  {this.state.readMore && <a onClick={this.toggleReadMore} className="button transparent">Read {this.state.expanded ? 'Less' : 'More'}</a>}
              </div>
              <Fetch name={NAME + '.authors'}
                fetchOnMount={true}
                endpoint={'author'}
                component={AuthorsList}
                initialQuery={{
                  topic_id: topic.id
                }}
              />
            </div>
          </div>
          <div className="topic__content container--wide">
            <TopicFilter topicId={topic.id} />
            <ContentList />
          </div>
        </section>
      </main>
    );
  }
}

export default Topic;
