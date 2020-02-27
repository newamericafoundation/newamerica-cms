import './ArticleListing.scss';

import { Link } from 'react-router-dom';
import React, { Component } from 'react';
import smoothScroll from '../../../lib/utils/smooth-scroll';
import { Response } from '../../components/API';
import { CSSTransition } from 'react-transition-group';
import { reloadScrollEvents, setMenuState } from '../actions';
import { connect } from 'react-redux';
import ScrollToTop from './ScrollToTop';
import Image from '../../components/Image';
import Separator from '../../components/Separator';
import { Text } from '../../components/Inputs'
import ArticleAuthors from './Authors';

const Lead = ({ article }) => (
  <div className="weekly-edition__lead margin-bottom-60">
    <a href={article.url}>
      <div className="weekly-edition__lead__image">
        <Image image={article.story_image_lg} />
      </div>
      <h1 className="margin-25">{article.title}</h1>
      <h3 className="margin-25">{article.story_excerpt}</h3>
    </a>
    <ArticleAuthors authors={article.authors} />
  </div>
);

const Article = ({ article, index }) => (
  <div className="weekly-edition__articles__article margin-bottom-60"
    style={{'transitionDelay': `${600 + 50*index}ms`, 'WebkitTransitionDelay': `${600 + 50*index}ms` }}>
    <a href={article.url}>
      <div className="weekly-edition__articles__article__image">
        <Image image={article.story_image_sm} />
      </div>
      <h3 className="margin-15">
        {article.title}
      </h3>
    </a>
    <ArticleAuthors authors={article.authors} />

  </div>
);

const Subscribe = () => (
  <div className="weekly-subscribe margin-bottom-60">
    <div className="weekly-subscribe__wrapper">
      <div>
        <Separator text="Subscribe"/>
        <h1 className="margin-top-60 margin-bottom-25">
          Be the first to hear about the latest events and research from New America.
        </h1>
      </div>
      <form action="/subscribe/?email=value" method="get">
        <Text name="email" label="Email Address">
          <button type="submit" className="button--text input__submit with-caret--right">Go</button>
        </Text>
      </form>
    </div>
  </div>
)

class ArticleListing extends Component {
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
    const { articles, transition, scrollPosition, canLoadMore, onLoadMore, isFetching} = this.props;
    const leadArticle = articles[0];
    const otherArticlesFirstRow = this.props.articles.slice(1, 3);
    const otherArticles = this.props.articles.slice(3, this.props.articles.length);
    return(
      <CSSTransition
        classNames="weekly-stagger"
        in={transition}
        appear={true}
        onExiting={(e,a)=>{ this.setState({ scrollPosition: scrollPosition }); }}
        timeout={600}>
        <section className="weekly-edition weekly-frame" style={{ top: `${-this.state.scrollPosition + 65 + 70}px`}}>
          <div className="container">
            <div className="weekly-edition__heading margin-90">
              <h1 className="centered promo margin-top-0 margin-bottom-25">New America Weekly</h1>
              <p className="centered margin-0">Our weekly digital magazine, which prizes our diversity—and how it reflects the America we're becoming.</p>
            </div>
            <div className="row margin-top-25 margin-bottom-35 gutter-10 weekly-edition__articles">
              <div className="col-12">
                <Lead article={leadArticle} />
              </div>
              {otherArticlesFirstRow.map((a,i) => (
                <div key={`artcile-${i}`} className="col-6 col-md-4">
                  <Article key={`article-${i}`} article={a} index={i}/>
                </div>
              ))}
              <div className="col-6 col-md-4">
                <Subscribe />
              </div>
              {otherArticles.map((a,i) => (
                <div key={`artcile-${i}`} className="col-6 col-md-4">
                  <Article key={`article-${i}`} article={a} index={i}/>
                </div>
              ))}
            </div>
            {canLoadMore &&
              <div className="program__publications-list-load-more margin-top-10">
                <a className={`button${isFetching ? ' is-fetching' : ''}`} onClick={onLoadMore}>
                  <span className="load-more-label">Load More</span>
                  {isFetching && <span className="loading-dots--absolute">
                    <span>.</span><span>.</span><span>.</span>
                  </span>}
                </a>
            </div>}
          </div>
        </section>
      </CSSTransition>
    );
  }
}

const mapStateToProps = (state) => ({
  scrollPosition : state.site.scroll.position
});

export default ArticleListing = connect(mapStateToProps)(ArticleListing);
