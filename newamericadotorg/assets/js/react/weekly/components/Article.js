import Heading from './Heading';

const Article = ({ article }) => (
  <main>
    <Heading post={article} page="article" />
    <section className="container--full-width weekly-article-content-wrapper">
    	<section className="container container--wide weekly-article-content">
    		<div className="row">
    		 	<aside className="post-authors col-sm-2"></aside>
    			<article className="post-body weekly-body with-dropcap col-sm-8" dangerouslySetInnerHTML={{__html: article.body}}></article>
    			<aside className="post-social weekly-social col-sm-2">
    				<div className="post-social__sticky-wrapper">
    					<label className="post-label lg">Share</label>
    				</div>
    			</aside>
    		</div>
    	</section>
    </section>
  </main>
);

export default Article
