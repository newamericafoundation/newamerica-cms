import './Authors.scss';

import React from 'react';

const AuthorInfo = ({ author }) => (
  <>
    <div className="report__author-button__image">
      {author.profile_image && <img src={author.profile_image} alt={author.profile_image_alt} />}
      {!author.profile_image && <i className="fa fa-user"/>}
    </div>
    <div className="report__author-button__text">
      <h4 className="margin-0">
        {author.first_name}&nbsp;{author.last_name}
      </h4>
      {author.position &&
      <h6 className="caption margin-top-5 margin-bottom-0">
        {author.position}
      </h6>}
    </div>
  </>
);

const Author = ({ author, md }) => (
 <div className={`report__author-button ${author.former && `report__author-button--no-link`}`} style={{ marginBottom: md ? '15px' : '30px' }}>
    {!author.former ? (
      <a href={author.url} className="report__author-button__inner">
        <AuthorInfo author={author}/>
      </a>
    ) : (
      <div className="report__author-button__inner">
        <AuthorInfo author={author}/>
      </div>
    )}
 </div>
);

const Authors = ({ authors, md=false }) => (
  <div className="report__authors row gutter-30">
    {authors.map((a,i) => (
      <div className={`${md ? ' ' : 'col-md-6 col-lg-4 ' }col-12`} key={`author-${i}`}>
        <Author author={a} md={md}/>
      </div>
    ))}
  </div>
);

export default Authors;
