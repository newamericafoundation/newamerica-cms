import { Link } from 'react-router-dom';
import { Component } from 'react';
import smoothScroll from '../../../utils/smooth-scroll';
import { Response } from '../../components/API';
import { CSSTransition } from 'react-transition-group';
import { reloadScrollEvents, setMenuState } from '../actions';
import { connect } from 'react-redux';
import ScrollToTop from './ScrollToTop';
import Image from '../../components/Image';
import Separator from '../../components/Separator';

const ArticleAuthors = ({ authors }) => (
  <label className="block subtitle">
    <span>By: </span>
    {authors.map((a,i)=>(
      <span key={`author-${i}`}>{a.first_name} {a.last_name}</span>
    ))}
  </label>
);

const Lead = ({ article }) => (
  <div className="weekly-edition__lead margin-bottom-60">
    <Link to={article.url}>
      <div className="weekly-edition__lead__image">
        <Image image={article.story_image_lg} />
      </div>
      <h1>{article.title}</h1>
      <h3>{article.story_excerpt}</h3>
      <ArticleAuthors authors={article.authors} />
    </Link>
  </div>
);

const Article = ({ article, index }) => (
  <div className="weekly-edition__articles__article margin-bottom-60"
    style={{'transitionDelay': `${600 + 50*index}ms`, 'WebkitTransitionDelay': `${600 + 50*index}ms` }}>
    <Link to={article.url}>
      <div className="weekly-edition__articles__article__image">
        <Image image={article.story_image_sm} />
      </div>
      <h3>
        {article.title}
      </h3>
      <ArticleAuthors authors={article.authors} />
    </Link>
  </div>
);

export default class Edition extends Component {
  componentDidMount(){
    //this.props.dispatch(reloadScrollEvents());
  }
  componentWillLeave() {
    console.log('leave!');
  }
  render(){
    let { edition } = this.props;
    let articles = edition.articles.slice(1,edition.articles.length);
    let attrs =  {
      'data-scroll-top-offset':'-25',
      'data-scroll-bottom-offset': '-100vh'
    }
    return(
      <section className="weekly-edition weekly-frame">
        <div className="container--1080">
        <div className="weekly-edition__heading margin-bottom-80">
          <h1 className="centered promo margin-top-0 margin-bottom-25">New America Weekly</h1>
          <p className="centered margin-0">Our weekly digital magazine, which prizes our diversity—and how it reflects the America we're becoming.</p>
        </div>
        <Separator text={edition.number}/>
        <CSSTransition
          classNames="weekly-edition-stagger"
          timeout={600}>
          <div className="row gutter-10 scroll-target" {...attrs} key={edition.id}>
            <div className="col-12">
              <Lead article={edition.articles[0]} edition={edition} />
            </div>
            {articles.map((a,i) => (
              <div key={`artcile-${i}`} className="col-6 col-md-4">
                <Article key={`article-${i}`} article={a} index={i}/>
              </div>
            ))}
          </div>
        </CSSTransition>
        <ScrollToTop />
        </div>
      </section>
    );
  }
}
