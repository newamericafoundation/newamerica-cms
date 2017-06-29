import { Link } from 'react-router-dom';
import { Component } from 'react';
import actions from '../../actions';

const LeadHeading = ({ article }) => (
  <div className="weekly-edition-grid__lead__text">
      <h1 className="weekly-edition-grid__lead__text__title">{article.title}</h1>
  </div>
);


const Lead = ({ article, edition }) => (
  <div className="weekly-edition-grid__lead weekly-edition-grid__col col">
    <Link to={`/weekly/${edition.slug}/${article.slug}`} className="weekly-edition-grid__lead-wrapper">
      <div className="weekly-edition-grid__lead__image-wrapper">
        <div style={{ backgroundImage: `url(${article.story_image_sm})`}} className="weekly-edition-grid__lead__image scroll-target"/>
      </div>
      <div className="weekly-edition-grid__lead__edition-title">
        <label>{edition.title}</label>
      </div>
      <LeadHeading article={edition.articles[0]} />
    </Link>
  </div>
);

const ArticleListItem = ({ item, edition }) => (
  <div className="weekly-edition-grid__article-list__item col-6">
    <Link to={`/weekly/${edition.slug}/${item.slug}`}>
      <div className="weekly-edition-grid__article-list__item__image"
        style={{backgroundImage: `url(${item.story_image_sm})`}}></div>
      <h2 className="weekly-edition-grid__article-list__item__title">
        {item.title}
      </h2>
    </Link>
  </div>
);

const ArticleList = ({ articles, edition }) => (
  <div className="weekly-edition-grid__article-list weekly-edition-grid__col col">
    <div className="row gutter-15">
      {articles.map((a,i) => (
        <ArticleListItem item={a} edition={edition}/>
      ))}
    </div>
  </div>
);

const EditionList = ({ editions }) => (
  <div className="weekly-edition-grid__edition-list weekly-edition-grid__col col"></div>
);

class EditionGrid extends Component {
  componentDidMount(){
    actions.reloadScrollEvents('.scroll-target');
  }
  componentDidUpdate(){
    actions.reloadScrollEvents('.scroll-target');
  }

  render(){
    let { edition } = this.props;
    let attrs =  {
      'data-scroll-enter-offset':'-25',
      'data-scroll-leave-offset': '-100vh'
    }
    return(
      <section className="weekly-edition-grid scroll-target container" {...attrs}>
        <div className="row">
          <Lead article={edition.articles[0]} edition={edition} />
          <ArticleList articles={edition.articles.slice(1,edition.articles.length)} edition={edition}/>
          <EditionList />
        </div>
      </section>
    );
  }
}

export default EditionGrid;
