import './Tabs.scss';

import React from 'react';
import SearchInput from './SearchInput';
import { Response } from '../../components/API'

export const PrimaryTab = ({switchTab}) => (
  <div className="mobile-menu__primary-tab">
    <div className="menu-list">
      <SearchInput />
      <h6 className="tab-link">
        <a onClick={()=>{switchTab('About');}}>About</a>
      </h6>
      <h6 className="tab-link">
        <a onClick={()=>{switchTab('Programs');}}>Programs</a>
      </h6>
      <h6>
        <a href="/publications/">Publications</a>
      </h6>
      <h6>
        <a href="/events/">Events</a>
      </h6>
    </div>
  </div>
);

const ProgramsTab = ({ response: { results }}) => {
  return(
    <div className="menu-list programs-tab">
      {results.programs.sort((a,b) => (a.title > b.title ? 1 : -1)).map((p, i)=>(
        <h6 key={`program-${i}`}>
          <a href={`/${p.slug}`}>{p.title}</a>
        </h6>
      ))}
    </div>
  );
};

const AboutTab = ({ response: { results }}) => (
  <div className="menu-list about-tab">
    {results.about_pages.map((a,i)=>(
      <h6 key={`about-${i}`}>
        <a href={a.url}>{a.title}</a>
      </h6>
    ))}
  </div>
);

export const SecondaryTab = ({}) => (
  <div className="mobile-menu__secondary-tab">
    <Response name="meta" component={AboutTab} />
    <Response name="meta" component={ProgramsTab}/>
  </div>
);
