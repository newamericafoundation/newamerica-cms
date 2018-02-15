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
      <h1 className="margin-25">{article.title}</h1>
      <h3 className="margin-25">{article.story_excerpt}</h3>
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
      <h3 className="margin-15">
        {article.title}
      </h3>
      <ArticleAuthors authors={article.authors} />
    </Link>
  </div>
);

class Edition extends Component {
  state = {
    scrollPosition: 0
  }

  componentWillMount(){
    if(window.scrollY > 135)
      window.scrollTo(0, 70)
  }

  componentWillUpdate(prevProps){
    if(this.props.scrollPosition != 71 && this.state.scrollPosition != this.props.scrollPosition){
      this.setState({ scrollPosition: this.props.scrollPosition });
    }
  }
  render(){
    let { edition, transition, scrollPosition } = this.props;
    let articles = edition.articles.slice(1,edition.articles.length);
    return(
      <CSSTransition
        classNames="weekly-stagger"
        in={transition}
        appear={true}
        onExiting={(e,a)=>{ this.setState({ scrollPosition: scrollPosition }); }}
        timeout={600}>
        <section className="weekly-edition weekly-frame" style={{ top: `${-this.state.scrollPosition + 65 + 70}px`}}>
          <div className="container--1080">
          <div className="weekly-edition__heading margin-bottom-80">
            <h1 className="centered promo margin-top-0 margin-bottom-25">New America Weekly</h1>
            <p className="centered margin-0">Our weekly digital magazine, which prizes our diversity—and how it reflects the America we're becoming.</p>
          </div>
          <Separator text={edition.number}/>

            <div className="row margin-top-25 gutter-10 weekly-edition__articles" key={edition.id}>
              <div className="col-12">
                <Lead article={edition.articles[0]} edition={edition} />
              </div>
              {articles.map((a,i) => (
                <div key={`artcile-${i}`} className="col-6 col-md-4">
                  <Article key={`article-${i}`} article={a} index={i}/>
                </div>
              ))}
            </div>
          <ScrollToTop />
          </div>
        </section>
      </CSSTransition>
    );
  }
}

const mapStateToProps = (state) => ({
  scrollPosition : state.site.scroll.position
});

export default Edition = connect(mapStateToProps)(Edition);
