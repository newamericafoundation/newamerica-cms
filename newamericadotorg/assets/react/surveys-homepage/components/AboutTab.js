import './AboutTab.scss';
import React from 'react';
import Authors from '../../report/components/Authors';
import Body from './Body';

const AboutTab = (props) => {
  const { data } = props;

  return (
    <div className="surveys-about-tab">
      {data.about && (
        <Body
          title="About This Project"
          body={data.about}
        />
      )}

      {data.methodology && (
        <Body
          title="Methodology"
          body={data.methodology}
        />
      )}

      {data.about_submission && (
        <Body
          title="Submit a Report"
          body={data.about_submission}
        />
      )}

      {data.partner_logo && (
        <Body title="Made Possible By" body="">
          <img src={data.partner_logo} alt="Partner" />
        </Body>
      )}

      {data.page_author && data.page_author[0].first_name && (
        <Body title="Authors" body="">
          <Authors authors={data.page_author} md={true} />
        </Body>
      )}
    </div>
  );
};

export default AboutTab;
