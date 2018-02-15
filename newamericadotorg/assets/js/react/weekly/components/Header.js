import { Component } from 'react';
import { connect } from 'react-redux';
import { Route, Link } from 'react-router-dom';
import { Fetch } from '../../components/API';
import Image from '../../components/Image';
import EditionList from './EditionList';

const EditionHeader = ({ response: { results }, edition, editionListOpen, toggleEditionList }) => (
  <div className="container">
    <div className="weekly-edition__header__nav">
      <div className="weekly-edition__header__nav__btn" onClick={toggleEditionList}>
        <label className={`button--text with-caret--${editionListOpen ? 'up' : 'down'} margin-0 white`}>Past Editions</label>
      </div>
    </div>
    <div className="weekly-edition__header__edition-list weekly-edition__edition-list row gutter-10 margin-top-25">
      {results.map((e,i)=>(
        <div key={`edition-${i}`} className="col-sm-6 col-lg-4">
          <a href={e.url}>
            <div className="weekly-edition__edition-list__edition">
              <div className="weekly-edition__edition-list__edition__image">
                <Image image={e.story_image} />
              </div>
              <div className="weekly-edition__edition-list__edition__text">
                <label className="block bold white">{e.number}</label>
                <label className="block white">{e.story_excerpt}</label>
              </div>
            </div>
          </a>
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
  constructor(props) {
    super(props);
    this.state = {
      editionListOpen: false
    };
  }

  toggleEditionList = () => {
    this.setState({ editionListOpen: !this.state.editionListOpen });
  }

  closeEditionList = () => {
    this.setState({ editionListOpen: false });
  }

  componentDidUpdate(prevProps){
    let { match } = this.props;
    if(match.params.articleSlug && !prevProps.match.params.articleSlug) this.closeEditionList();
  }

  render(){
    let { edition } = this.props;
    let { editionListOpen } = this.state;
    return(
      <header className={`weekly-edition__header${editionListOpen ? ' open' : ''}`}>
        <Route path="/weekly/:edition/" exact render={()=>(
          <Fetch name="weekly.editionList"
            component={EditionHeader}
            endpoint="weekly"
            fetchOnMount={true}
            edition={edition}
            editionListOpen={this.state.editionListOpen}
            toggleEditionList={this.toggleEditionList}
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
