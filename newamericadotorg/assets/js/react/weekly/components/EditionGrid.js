import { Link } from 'react-router-dom';

const LeadHeading = ({ article, edition }) => (
  <div className="weekly-edition-grid__lead__text">
      <h4 className="weekly-edition-grid__lead__text__edition">{edition.title}</h4>
      <h2 className="weekly-edition-grid__lead__text__title">{article.title}</h2>

  </div>
);


const Lead = ({ article, edition }) => (
  <div className="weekly-edition-grid__lead col-md-7">
    <Link to={`/weekly/${edition.slug}/${article.slug}`}>
      <div className="weekly-edition-grid__lead__image-wrapper">
        <div style={{ backgroundImage: `url(${article.story_image_sm})`}} className="weekly-edition-grid__lead__image with-inverse-overlay--black"/>
      </div>
      <LeadHeading article={edition.articles[0]} edition={edition} />
    </Link>
  </div>
);

const ArticleListItem = ({ item, edition }) => (
  <div className="weekly-edition-grid__article-list__item col-md-6">
    <Link to={`/weekly/${edition.slug}/${item.slug}`}>
      <div className="weekly-edition-grid__article-list__item__image"
        style={{backgroundImage: `url(${item.story_image_sm})`}}></div>
      <label className="lg active weekly-edition-grid__article-list__item__title">
      {item.title}
      </label>
    </Link>
  </div>
);

const ArticleList = ({ articles, edition }) => (
  <div className="weekly-edition-grid__article-list col-md-5">
    <div className="row">
      <div className="col-md-12">
        <label className="active lg weekly-edition-grid__article-list__also">Also in this Edition</label>
      </div>
    </div>
    <div className="row">
      {articles.map((a,i) => (
        <ArticleListItem item={a} edition={edition}/>
      ))}
    </div>
  </div>
);

const EditionGrid = ({ edition }) => (
  <div className="weekly-edition-grid row">
    <Lead article={edition.articles[0]} edition={edition} />
    <ArticleList articles={edition.articles.slice(1,edition.articles.length)} edition={edition}/>
  </div>
);

export default EditionGrid;
