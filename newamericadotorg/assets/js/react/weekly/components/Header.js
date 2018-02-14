import { Component } from 'react';
import { connect } from 'react-redux';
import { Route, Link } from 'react-router-dom';
import { Fetch } from '../../components/API';
import Image from '../../components/Image';
import EditionList from './EditionList';

const EditionHeader = ({ response: { results }, edition }) => (
  <div className="container">
    <div className="weekly-edition__header__nav">
      <div className="weekly-edition__header__nav__btn">
        <a className="button--text with-caret--down white">Past Editions</a>
      </div>
    </div>
    <div className="weekly-edition__header__edition-list weekly-edition__edition-list row gutter-10 margin-top-25">
      {results.map((e,i)=>(
        <div key={`edition-${i}`} className="col-sm-6 col-lg-4">
          <Link to={e.url}>
            <div className="weekly-edition__edition-list__edition">
              <div className="weekly-edition__edition-list__edition__image">
                <Image image={e.story_image} />
              </div>
              <div className="weekly-edition__edition-list__edition__text">
                <label className="block bold white">{e.number}</label>
                <label className="block white">{e.story_excerpt}</label>
              </div>
            </div>
          </Link>
        </div>
      ))}
    </div>
  </div>
);

const ArticleHeader = ({ edition }) => (
  <div className="container">
    <div className="weekly-edition__header__nav">
      <div className="weekly-edition__header__nav__btn">
        <Link className="button--text with-caret--left white" to={edition.url}>{edition.number}</Link>
      </div>
    </div>
  </div>
);


export default class Header extends Component {
  render(){
    let { edition } = this.props;
    return(
      <header className='weekly-edition__header'>
        <Route path="/weekly/:edition/" exact render={()=>(
          <Fetch name="weekly.editionList"
            component={EditionHeader}
            endpoint="weekly"
            fetchOnMount={true}
            edition={edition}
            initialQuery={{
              page_size: 9
            }}/>
        )}/>
        <Route path="/weekly/:edition/:article/" exact render={()=>(
          <ArticleHeader edition={edition} />
        )} />
      </header>
    );
  }
}
