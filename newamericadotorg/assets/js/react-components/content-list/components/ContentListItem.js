import { Component } from 'react';
import Author from '../../author/components/Author';

const Details = ({ post: { date, programs, content_type } }) => (
  <div className="content-list__item__details col-md-3">
    <label className="content-list__item__details__date">
      {date}
    </label>
    {programs &&
      <label className="content-list__item__details__program-content">
        {programs.map((p,i)=>(
          <span key={`program-${i}`}>
            <a href={p.url}>{p.name}</a>
            {i<programs.length-2 && ', '}
            {i==programs.length-2 && ' and '}
          </span>
        ))}
      </label>
    }
    <label className="content-list__item__details__content-type">
      {content_type.name}
    </label>
  </div>
);

const Heading = ({ post: { url, title, story_excerpt, authors }}) => (
  <div className="content-list__item__heading col-md-6">
    <a className="content-list__item__heading__link-wrapper" href={url}>
      <h4 className= "content-list__item__heading__heading">
        {title}
      </h4>
    </a>
    <p className= "content-list__item__heading__excerpt">
      {story_excerpt}
    </p>
    <div className="content-list__item__heading__authors container">
      <div className="row no-gutters">
        {authors.map((a,i)=>(
          <Author key={`author-${i}`} author={a} classes="ultra-compact col-md-4 col-xl-3 content-list__item__heading__author"/>
        ))}
      </div>
    </div>
  </div>
);

const Image = ({ post: { story_image }}) => (
  <div className="content-list__item__image-wrapper col-md-3">
    <img src={story_image} className="content-list__item__image" />
  </div>
);

const ContentListItem = ({ post }) => (
  <div className="row content-list__item">
    <Details post={post} />
    <Heading post={post} />
    <Image post={post} />
  </div>
);

export default ContentListItem;
