import './AboutTab.scss';
import React from 'react';
import Authors from '../../report/components/Authors';
import Body from './Body';

const AboutTab = (props) => {
  const {
    data: { survey_home_page },
  } = props;

  return (
    <div className="surveys-about-tab">
      {survey_home_page.about && (
        <Body
          title="About This Project"
          body={survey_home_page.about}
        />
      )}

      {survey_home_page.methodology && (
        <Body
          title="Methodology"
          body={survey_home_page.methodology}
        />
      )}

      {survey_home_page.about_submission && (
        <Body
          title="Submit a Report"
          body={survey_home_page.about_submission}
        />
      )}

      {survey_home_page.partner_logo && (
        <Body title="Made Possible By" body="">
          <img src={survey_home_page.partner_logo} alt="Partner" />
        </Body>
      )}

      {survey_home_page.page_author && survey_home_page.page_author[0].first_name && (
        <Body title="Authors" body="">
          <Authors authors={survey_home_page.page_author} md={true} />
        </Body>
      )}
    </div>
  );
};

export default AboutTab;
