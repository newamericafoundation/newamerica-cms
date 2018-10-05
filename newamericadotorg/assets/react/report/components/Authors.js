import './Authors.scss';

import React from 'react';

const Author = ({ author }) => (
 <div className="report__author-button">
   <a href={author.url} style={{ display: 'block' }}>
      <div className="report__author-button__image">
        {author.profile_image && <img src={author.profile_image.url} />}
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
    </a>
 </div>

);

const Authors = ({ authors }) => (
  <div className="report__authors row gutter-30">
    {authors.map((a,i) => (
      <div className="col-md-6 col-lg-4 col-12" key={`author-${i}`}>
        <Author author={a} />
      </div>
    ))}
  </div>
);

export default Authors;
