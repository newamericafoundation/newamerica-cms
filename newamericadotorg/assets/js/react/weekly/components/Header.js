import './Header.scss';

import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Route, Link } from 'react-router-dom';
import { Fetch, Response } from '../../components/API';
import { Arrow } from '../../components/Icons';
import HeaderEditionList from './HeaderEditionList';

const EditionHeaderNavButtons = ({hasPrevious, hasNext, prevEditionPage, nextEditionPage}) => (
  <div className="weekly-edition__header__page">
      {hasPrevious &&
        <h5 className="prev-page inline white margin-0" onClick={()=>{prevEditionPage(hasPrevious)}}>
          <Arrow direction={"left white"}/><span>Prev.</span>
        </h5>
      }
      {hasNext &&
        <h5 className="next-page inline white margin-0" onClick={()=>{nextEditionPage(hasNext)}}>
          <span>Next</span><Arrow direction={"right white"}/>
        </h5>
      }
  </div>
);

const EditionHeader = ({ response: { results, hasNext, hasPrevious, params: { query }}, edition, editionListOpen, toggleEditionList, prevEditionPage, nextEditionPage }) => (
  <div className="container">
    <div className="weekly-edition__header__nav">
      <div className="weekly-edition__header__nav__btn" onClick={toggleEditionList}>
        <a className={`button--text with-caret--${editionListOpen ? 'up' : 'down'} white`}>Past Editions</a>
      </div>
      {editionListOpen &&
        <EditionHeaderNavButtons
          hasPrevious={hasPrevious}
          hasNext={hasNext}
          prevEditionPage={prevEditionPage}
          nextEditionPage={nextEditionPage} />
      }
      <HeaderEditionList query={query} editions={results} />
    </div>

  </div>
);

class ArticleHeader extends Component {
  componentDidMount(){
    this.props.reloadScrollEvents();
  }
  render(){
    let { edition } = this.props;
    return (
      <div className="container">
        <div className="weekly-edition__header__nav scroll-target" data-scroll-offset="125">
          <div className="weekly-edition__header__nav__sticky">
            <div className="container">
              <div className="weekly-edition__header__nav__btn">
                <Link className="button--text with-caret--left white" to={edition.url}>{edition.number}</Link>
              </div>
              <h5 className="inline white margin-0 weekly-edition__header__nav__heading">New America Weekly</h5>
            </div>
          </div>
        </div>
      </div>
    );
  }
};


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

  reloadScrollEvents = () => {
    this.props.dispatch({
      type: 'RELOAD_SCROLL_EVENTS',
      component: 'site'
    });
  }

  render(){
    let { edition, match: { params } } = this.props;
    let { editionListOpen } = this.state;
    return(
      <header id="weekly__header" className={`weekly-edition__header${editionListOpen ? ' open' : ''}${params.articleSlug ? ' article-header': ''}`}>
        <Fetch name="weekly.editionList"
          component={null}
          endpoint="weekly"
          fetchOnMount={true}
          eager={true}
          initialQuery={{
            page_size: 9,
            page: this.state.page
          }}/>
        <Route path="/weekly/:edition/" exact render={()=>(
          <Response name="weekly.editionList"
              component={EditionHeader}
              edition={edition}
              editionListOpen={this.state.editionListOpen}
              toggleEditionList={this.toggleEditionList}
              prevEditionPage={this.prevEditionPage}
              nextEditionPage={this.nextEditionPage}/>
        )}/>
        <Route path="/weekly/:edition/:article/" exact render={()=>(
          <ArticleHeader edition={edition} reloadScrollEvents={this.reloadScrollEvents} />
        )} />
      </header>
    );
  }
}
