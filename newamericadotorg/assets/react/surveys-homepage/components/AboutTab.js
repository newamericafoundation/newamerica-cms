import './AboutTab.scss';
import React from 'react';
import Authors from '../../report/components/Authors';
import Body from './Body';

const AboutTab = (props) => {
  const {
    data: { survey_home_page },
  } = props;

  const submitReport = `
    <p>
      Know of a survey report that should be added to our list?
      <a href='mailto:nguyens@newamerica.org'>
        Send us an email
      </a>
    </p>
    `;

  return (
    <div className="surveys-about-tab">
      <Body
        title="About This Project"
        body={survey_home_page.about}
      />
      <Body title="Methodology" body={survey_home_page.methodology} />
      <Body
        title="Submit a Report"
        body={survey_home_page.submissions}
      />
      <Body title="Made Possible By" body="">
        <img src={survey_home_page.partner_logo} alt="Partner" />
      </Body>
      <Body title="Authors" body="">
        <Authors authors={survey_home_page.page_author} md={true} />
      </Body>
    </div>
  );
};

export default AboutTab;
