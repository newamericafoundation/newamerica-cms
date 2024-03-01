import './FeaturedSections.scss';

import React, { Component } from 'react';
import { Highlight, DataViz, Resource } from '../../components/Icons';
import { Link } from 'react-router-dom';

function PossiblyExternalLink({children, ...props}) {
  // If the given link url is relative to the report path, return a
  // `Link` component to tie into react-router.  If it's an external
  // link, or a link to a part of the site outside of the report,
  // return an plain old `a` tag.

  let linkTarget = new URL(props.to);

  if (linkTarget.pathname.startsWith(location.pathname)) {
    let relativizedTarget = props.to.replace(location.origin, '');
    return (<Link {...props} to={relativizedTarget}>{children}</Link>);
  } else {
    return (<a href={props.to} className={props.className} style={props.style}>{children}</a>);
  }
}

const iconsMap = {
  'Highlight': Highlight,
  'Data Visualization': DataViz,
  'Resource': Resource
}

const FeaturedIcon = ({ featuredType, Icon }) => (
  <div className="report__featured-button__icon margin-top-25">
    <Icon className="circle-gray" /> <h6 className="inline" style={{ marginLeft: '15px' }}>{featuredType}</h6>
  </div>

);

const Featured = ({ section }) => (
  <div className="report__featured-button" style={{ marginBottom: '30px' }}>
    <PossiblyExternalLink to={section.url} style={{ display: 'block' }} className="ga-track-click" data-action="click_landing" data-label="report" data-value="featured_button">
      {section.label && <h4 className="margin-top-0 margin-bottom-10">
        {section.label}
      </h4>}
      <h6 className="paragraph margin-0" style={{ height: '40px', overflow: 'hidden' }}>{section.description || section.title}</h6>
      {!section.label && <h4 className="margin-top-10 margin-bottom-0 spacer">
        &nbsp;
      </h4>}
      <FeaturedIcon featuredType={section.type} Icon={iconsMap[section.type]} />
    </PossiblyExternalLink>
  </div>
);

const Sections = ({ featuredSections }) => (
  <div className="row gutter-30">
    {featuredSections.map((s,i)=>(
      <div className="col-md-6 col-lg-4 col-12" key={`section-${i}`}>
        <Featured section={s} />
      </div>
    ))}
  </div>
)


export default Sections;
