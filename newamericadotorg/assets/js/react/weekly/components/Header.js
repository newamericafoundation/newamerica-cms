import { Component } from 'react';
import { connect } from 'react-redux';
import { Route, Link } from 'react-router-dom';
import { CSSTransition, TransitionGroup } from 'react-transition-group';
import { Fetch } from '../../components/API';
import Image from '../../components/Image';
import { Arrow } from '../../components/Icons';
import EditionList from './EditionList';

const Fade = ({children, ...props}) => (
  <CSSTransition
    {...props}
    timeout={300}
    classNames="edition-list-fade">
    {children}
  </CSSTransition>
);

const EditionListItem = ({ edition }) => (
  <div className="col-sm-6 col-lg-4">
    <a href={edition.url}>
      <div className="weekly-edition__edition-list__edition">
        <div className="weekly-edition__edition-list__edition__image">
          <Image image={edition.story_image} />
        </div>
        <div className="weekly-edition__edition-list__edition__text">
          <label className="block bold white">{edition.number}</label>
          <label className="block white">{edition.story_excerpt}</label>
        </div>
      </div>
    </a>
  </div>
);

const EditionHeader = ({ response: { results, hasNext, hasPrevious, params: { query }}, edition, editionListOpen, toggleEditionList, prevEditionPage, nextEditionPage }) => (
  <div className="container">
    <div className="weekly-edition__header__nav">
      <div className="weekly-edition__header__nav__btn" onClick={toggleEditionList}>
        <label className={`button--text with-caret--${editionListOpen ? 'up' : 'down'} margin-0 white`}>Past Editions</label>
      </div>
      {editionListOpen && <div className="weekly-edition__header__page">
          {hasPrevious && <label className="prev-page button--text white margin-0" onClick={()=>{prevEditionPage(hasPrevious)}}><Arrow direction={"left white"}/><span>Prev.</span></label>}
          {hasNext && <label className="next-page button--text white margin-0" onClick={()=>{nextEditionPage(hasNext)}}><span>Next</span><Arrow direction={"right white"}/></label>}
        </div>}
    </div>
    <TransitionGroup className="edition-list-fade-wrapper">
      <Fade key={query.page}
        className="weekly-edition__header__edition-list weekly-edition__edition-list row gutter-10 margin-top-25">
        <div>
          {results.map((e,i)=>(
            <EditionListItem edition={e} key={`edition-${i}`}/>
          ))}
        </div>
      </Fade>
    </TransitionGroup>
  </div>
);

const ArticleHeader = ({ edition }) => (
  <div className="container">
    <div className="weekly-edition__header__nav">
      <div className="weekly-edition__header__nav__btn">
        <Link className="button--text with-caret--left white" to={edition.url}>{edition.number}</Link>
      </div>
      <label className="button--text white margin-0 weekly-edition__header__nav__heading">New America Weekly</label>
    </div>
  </div>
);


export default class Header extends Component {
  constructor(props) {
    super(props);
    this.state = {
      editionListOpen: false,
      page: 1
    };
  }

  toggleEditionList = () => {
    this.setState({ editionListOpen: !this.state.editionListOpen });
  }

  closeEditionList = () => {
    this.setState({ editionListOpen: false });
  }

  prevEditionPage = (hasPrev) => {
    if(!hasPrev) return;
    this.setState({ page : this.state.page-=1 });
  }

  nextEditionPage = (hasNext) => {
    if(!hasNext) return;
    this.setState({ page : this.state.page+=1 });
  }

  componentDidUpdate(prevProps){
    let { match } = this.props;
    if(match.params.articleSlug && !prevProps.match.params.articleSlug) this.closeEditionList();
  }

  render(){
    let { edition } = this.props;
    let { editionListOpen } = this.state;
    return(
      <header id="weekly__header" className={`weekly-edition__header${editionListOpen ? ' open' : ''}`}>
        <Route path="/weekly/:edition/" exact render={()=>(
          <Fetch name="weekly.editionList"
            component={EditionHeader}
            endpoint="weekly"
            fetchOnMount={true}
            eager={true}
            edition={edition}
            editionListOpen={this.state.editionListOpen}
            toggleEditionList={this.toggleEditionList}
            prevEditionPage={this.prevEditionPage}
            nextEditionPage={this.nextEditionPage}
            initialQuery={{
              page_size: 9,
              page: this.state.page
            }}/>
        )}/>
        <Route path="/weekly/:edition/:article/" exact render={()=>(
          <ArticleHeader edition={edition} />
        )} />
      </header>
    );
  }
}
