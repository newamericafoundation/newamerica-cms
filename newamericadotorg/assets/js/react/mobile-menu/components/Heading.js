import './Heading.scss';

import React from 'react';

const Heading = ({selectedTab, switchTab}) => (
  <div className="mobile-menu__heading">
    <div className="logo__wrapper"><a href="/"><div className="logo sm"></div></a></div>
    <a className="tab-link-back button--text with-caret--left margin-0 block" onClick={()=>{switchTab(false);}}>
      {selectedTab}
    </a>
  </div>
);

export default Heading;
