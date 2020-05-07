import React from 'react';
import './Breadcrumb.scss';

export const Breadcrumb = ({ path }) => {
  const pages = path.map(page => {
    return (
      <li key={page.id} className="breadcrumb__item">
        <a href={page.url}>{page.title}</a>
      </li>
    );
  });

  return (
    <ul className="h6 breadcrumb margin-bottom-5 margin-bottom-md-15">
      {pages}
    </ul>
  );
};
