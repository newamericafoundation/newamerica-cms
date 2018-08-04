import './HeaderEditionList.scss';

import React, { Component } from 'react';
import { CSSTransition, TransitionGroup } from 'react-transition-group';
import Image from '../../components/Image';

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
          <h4 className="white margin-top-0 margin-bottom-10">{edition.number}</h4>
          <h6 className="white margin-0">{edition.story_excerpt}</h6>
        </div>
      </div>
    </a>
  </div>
);

const EditionList = ({ query, editions }) => (
  <TransitionGroup className="edition-list-fade-wrapper">
    <Fade key={query.page}
      className="weekly-edition__header__edition-list weekly-edition__edition-list row gutter-10 margin-top-25">
      <div>
        {editions.map((e,i)=>(
          <EditionListItem edition={e} key={`edition-${e.slug}`}/>
        ))}
      </div>
    </Fade>
  </TransitionGroup>
);

export default EditionList;
