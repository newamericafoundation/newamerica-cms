import Heading from './Heading';
import { Link } from 'react-router-dom';
import { Component } from 'react';
import { reloadScrollEvents } from '../actions';

export default class Article extends Component {
  componentDidMount(){
    this.props.dispatch(reloadScrollEvents());
  }

  render(){
    let { article, edition } = this.props;
    return (
      <section className="weekly-article container">
        <section className="weekly-article__nav-wrapper scroll-target">
          <div className="weekly-article__nav container--wide">
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
      		 	<aside className="post-authors col-sm-2"></aside>
      			<article className="post-body weekly-body with-dropcap col-sm-8" dangerouslySetInnerHTML={{__html: article.body}}></article>
      			<aside className="post-social weekly-social col-sm-7">
      				<div className="post-social__sticky-wrapper">
      					<label className="post-label lg">Share</label>
      				</div>
      			</aside>
      		</div>
      	</section>
      </section>
    );
  }
}
