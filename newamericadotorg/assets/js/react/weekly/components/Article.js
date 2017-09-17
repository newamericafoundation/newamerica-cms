import Heading from './Heading';
import { Link } from 'react-router-dom';
import { Component } from 'react';
import { reloadScrollEvents } from '../actions';
import ScrollToTop from './ScrollToTop';

export default class Article extends Component {
  componentDidMount(){
    this.props.dispatch(reloadScrollEvents());
  }

  render(){
    let { article, edition } = this.props;
    return (
      <section className="weekly-article weekly-content">
          <section className="weekly-article__nav-wrapper scroll-target">
            <div className="weekly-article__nav">
              <label className="weekly-article__nav__text">
                <Link to={'/weekly/'+edition.slug}>
                  <i className="fa fa-long-arrow-left"></i>
                  {edition.title}
                </Link>
              </label>
            </div>
          </section>
          <Heading post={article} page="article" />
        	<section className="container--medium weekly-article-content">
        		<div className="row">
        			<article className="post-body weekly-body with-dropcap col-lg-9 col-md-8" dangerouslySetInnerHTML={{__html: article.body}}></article>
        			<aside className="post-social weekly-social col-lg-3 col-md-4">
        				<div className="post-social__sticky-wrapper">
        					<label className="post-label lg">Share</label>
        				</div>
        			</aside>
        		</div>
        	</section>
          <ScrollToTop />
      </section>
    );
  }
}
