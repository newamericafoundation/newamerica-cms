import './Authors.scss';

import React from 'react';

const ArticleAuthors = ({ authors }) => (
  <div className="weekly__authors-list margin-0">
    {authors.map((a,i)=>(
      <span key={`author-${i}`} className="weekly__authors-list__author">
        {i==0 && <h6 className="inline margin-0">By:&nbsp;</h6>}
        <h6 className="link inline margin-0"><a href={a.url}><u>{a.first_name} {a.last_name}</u></a></h6>
        {(authors.length == 2 && i == 0) && <h6 className="inline margin-0">&nbsp;and&nbsp;</h6>}
        {(authors.length > 2 && i < authors.length-2)  && <h6 className="inline margin-0">,&nbsp;</h6>}
        {(authors.length > 2 && i == authors.length-2)  && <h6 className="inline margin-0">,&nbsp;and&nbsp;</h6>}
      </span>
    ))}
  </div>
);

export default ArticleAuthors;
