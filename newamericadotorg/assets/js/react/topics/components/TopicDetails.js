import { Component } from 'react';
import { Link } from 'react-router-dom';
import { Fetch } from '../../components/API';
import { Author } from '../../components/Content';
import { NAME } from '../constants';

const SubTopics = ({topic}) => (
  <div className="topic__details__subtopics">
    {topic.subtopics.length > 0 &&
      <h4 className="margin-bottom-5 topic__details__subtopic-label">Subtopics</h4>
    }
    {topic.subtopics.map((t,i)=>(
      <Link className="tag with-gutter" to={t.url}>{t.title}</Link>
    ))}
  </div>
);

class TopicText extends Component {
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
    let { topic } = this.props;
    let expandedClass = this.state.expanded ? 'expanded' : '';
    return (
      <div className="topic__details__text-wrapper col-lg-8">
          <h1 className="topic__details__title margin-5">{topic.title}</h1>
          <SubTopics topic={topic} />
          <article className={`topic__details__body ${expandedClass}`}>
            <div ref={(div)=>{this.body=div;}}
              className="topic__details__body__wrapper"
              dangerouslySetInnerHTML={{__html: topic.body }} />
          </article>
          {this.state.readMore &&
            <a onClick={this.toggleReadMore} className="button transparent">
              Read {this.state.expanded ? 'Less' : 'More'}
            </a>
          }
      </div>
    );
  }
}

const AuthorsList = ({ response: { results }}) => (
  <div className="topic__details__author-list col-lg-4">
    {results.length > 0 && <div className="container"><h4 className="margin-bottom-5">Experts</h4></div>}
    <div className="post-authors">
    <div className="post-authors__list">
      {results.map((a,i)=>(
        <Author classes="compact sm-compact" author={a}/>
      ))}
    </div>
    </div>
  </div>
);

const TopicDetails = ({topic}) => (
  <section className="topic__details container--wide">
    <div className="row">
      <TopicText topic={topic} />
      <Fetch name={NAME + '.authors'}
        fetchOnMount={true}
        endpoint={'author'}
        component={AuthorsList}
        initialQuery={{
          topic_id: topic.id
        }}/>
    </div>
  </section>
);

export default TopicDetails;
