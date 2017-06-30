import { Link } from 'react-router-dom';
import { Component } from 'react';
import actions from '../../actions';
import { Response } from '../../components/API';
import { CSSTransitionGroup } from 'react-transition-group'

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

const ArticleListItem = ({ item, edition, index }) => (
  <div className="weekly-edition-grid__article-list__item col-6"
    style={{'transitionDelay': `${50*index}ms`, 'WebkitTransitionDelay': `${50*index}ms` }}>
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
        <ArticleListItem item={a} edition={edition} index={i}/>
      ))}
    </div>
  </div>
);

class EditionList extends Component {
  componentDidMount(){
    let { activeEdition } = this.props;
    setTimeout(function(){
      actions.smoothScroll(`#id-${activeEdition.id}`, {
        el: '#edition-list-scroll',
        duration: 0,
        offset: -90
      });
    }, 0);
  }
  render(){
    let { response: { results }, activeEdition} = this.props;

    return (
      <div className="weekly-edition-grid__edition-list weekly-edition-grid__col col">
        <div className="weekly-edition-grid__edition-list__scroll-wrapper" id="edition-list-scroll">
          {results.map((e, i)=>(
            <div className={`weekly-edition-grid__edition-list__item ${activeEdition.id==e.id ? 'active' : ''}`} id={`id-${e.id}`}>
              <Link to={'/weekly/'+e.slug}>
              <label className="weekly-edition-grid__edition-list__item__label">Edition</label>
              <label className="weekly-edition-grid__edition-list__item__edition-number">
                {e.title.split(' ')[1] || e.title}
              </label>
              </Link>
            </div>
          ))}
        </div>
      </div>
    );
  }
}

class EditionGrid extends Component {
  componentDidMount(){
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
        <CSSTransitionGroup
          transitionAppear={true}
          transitionAppearTimeout={2000}
          transitionName="weekly-edition-stagger"
          transitionEnterTimeout={2000}
          transitionLeaveTimeout={600}>
        <div className="row" key={edition.id}>
          <Lead article={edition.articles[0]} edition={edition} />
          <ArticleList articles={edition.articles.slice(1,edition.articles.length)} edition={edition}/>
          <Response name="weekly.editionList" component={EditionList} activeEdition={edition} />
        </div>
      </CSSTransitionGroup>
      </section>
    );
  }
}

export default EditionGrid;
