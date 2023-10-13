import './ArticleListing.scss';

import { Link } from 'react-router-dom';
import React, { Component } from 'react';
import { createPortal } from 'react-dom';
import { Fetch } from  '../../components/API';
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
import { format as formatDate, parseISO } from 'date-fns/esm';
import { Overlay } from '../../report/components/OverlayMenu';
import Subscribe from '../../program-page/components/Subscribe'


const Featured = (props) => {
  if (props.response.isFetching) {
    return null;
  }
  let { response: {results}, addFeatured, addSubscription} = props;
  if (!results.featured_pages && !results.subscriptions) { return null; }
  if (results.subscriptions) {
    results.subscriptions.forEach(sub => addSubscription(sub));
  }
  if (results.featured_pages) {
    results.featured_pages.forEach(article => addFeatured(article))
  }
  return null;
};

const Lead = ({ article }) => (
  <div className="weekly-edition__lead margin-bottom-60">
    <a href={article.url}>
      <div className="weekly-edition__lead__image">
        <Image image={article.story_image_lg} alt={article.story_image_alt}/>
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
        <Image image={article.story_image_sm} alt={article.story_image_alt} />
      </div>
      <h3 className="margin-15">
        {article.title}
      </h3>
    </a>
    <ArticleAuthors authors={article.authors} />
    {article.date && (
      <div className="margin-top-10">{formatDate(parseISO(article.date), 'MMM. do, yyyy')}</div>
    )}
  </div>
);

class ThreadSubscribeCard extends Component {
  state = {
    email: null,
    open: false,
  }

  fixBody = () => {
    const top = window.pageYOffset;
    document.body.style.overflow = 'hidden';
    document.body.style.position = 'fixed';
    document.body.style.top = -top + 'px';
  };

  unfixBody = () => {
    document.body.style.overflow = 'auto';
    document.body.style.position = 'static';
    if (document.body.style.top)
      window.scrollTo(0, -document.body.style.top.replace('px', ''));

    document.body.style.top = null;
  };

  closeModal = () => {
    this.unfixBody();
    this.setState({open: false});
  }

  openModal = () => {
    this.fixBody();
    this.setState({open: true});
  }

  render() {
    let { subscriptions } = this.props;
    return (
      <>
        <div className="weekly-subscribe margin-bottom-60">
          <div className="weekly-subscribe__wrapper" onClick={this.openModal}>
            <div>
              <Separator text="Subscribe"/>
              <h1 className="margin-25 margin-top-lg-60">
                Policy. Equity. Culture. Your inbox.
                <br /><br />
                Get The Thread monthly newsletter.
              </h1>
              <button onClick={this.openModal} className="button margin-lg-25">Subscribe</button>
            </div>
          </div>
        </div>

        {this.state.open && createPortal(
          <Overlay
            title="Subscribe"
            open={this.state.open}
            close={this.closeModal}
          ><Subscribe subscriptions={this.props.subscriptions} /></Overlay>,
          document.body
        )}
      </>
    );
  }
}

class ArticleListing extends Component {
  state = {
    scrollPosition: 0,
    featuredArticles: [],
    featuredArticleSlugs: new Set(),
    subscriptions: [],
    subscriptionTitles: new Set(),
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

    const addSubscription = subscription => {
      let { subscriptions, subscriptionTitles} = this.state;
      if (subscriptionTitles.has(subscription.title)) { return; }

      subscriptionTitles.add(subscription.title);
      subscriptions.push(subscription);
      this.setState({
        subscriptions: subscriptions,
        subscriptionTitles: subscriptionTitles,
      });
    }

    const addFeatured = article => {
      let {featuredArticleSlugs, featuredArticles} = this.state;
      if (featuredArticleSlugs.has(article.slug)) { return; }

      featuredArticles.push(article);
      featuredArticleSlugs.add(article.slug);
      this.setState({
        featuredArticleSlugs: featuredArticleSlugs,
        featuredArticles: featuredArticles,
      });
    }
    const { articles, transition, scrollPosition, canLoadMore, onLoadMore, isFetching} = this.props;
    const leadArticle = articles[0];

    let allArticles = this.state.featuredArticles.concat(
      articles.slice(1, articles.length).filter(a => !this.state.featuredArticleSlugs.has(a.slug))
    );

    const otherArticlesFirstRow = allArticles.slice(0, 2);
    const otherArticles = allArticles.slice(2, allArticles.length);

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
              <h1 className="centered promo margin-top-0 margin-bottom-25">The Thread</h1>
              <p className="centered margin-0">Where policy, equity, and culture come together.</p>
            </div>
            <div className="row margin-top-25 margin-bottom-35 gutter-10 weekly-edition__articles">
              <div className="col-12">
                <Lead article={leadArticle} />
              </div>

              <Fetch
                name="thread-detail"
                key="thread-detail"
                endpoint="thread/detail"
                fetchOnMount={true}
                renderIfNoResults={false}
                component={Featured}
                addFeatured={addFeatured}
                addSubscription={addSubscription}
              />

              {otherArticlesFirstRow.map((a,i) => (
                <div key={`artcile-${i}-pongus`} className="col-6 col-md-4">
                  <Article key={`article-${i}`} article={a} index={i}/>
                </div>
              ))}
              <div className="col-6 col-md-4">
                <ThreadSubscribeCard subscriptions={this.state.subscriptions} />
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
