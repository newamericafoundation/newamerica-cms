import './AboutTab.scss';
import React, { Component } from 'react';
import Authors from '../../report/components/Authors';
import Body from './Body';

class AboutTab extends Component {
  constructor(props) {
    super(props);
  }
  render() {
    const {
      data: { survey_home_page },
    } = this.props;

    const submitReport = `
      <p>
        Know of a survey report that should be added to our list?
        <a href='mailto:nguyens@newamerica.org'>
          Send us an email
        </a>
      </p>
      `;
    const logo = `
      <img
        src="https://www.gavi.org/sites/default/files/investing/funding/donor-contributions-pledges/bmgf-topspace2.png"
        alt=""
      />
    `;
    return (
      <div className="surveys-about-tab">
        <Body
          title="About This Project"
          body={survey_home_page.about}
        />
        <Body
          title="Methodology"
          body={survey_home_page.methodology}
        />
        <Body title="Submit a Report" body={submitReport} />
        <Body title="Made Possible By" body={logo} />
        <Body title="Made Possible By" body="">
          <Authors authors={survey_home_page.page_author} md={true} />
        </Body>
      </div>
    );
  }
}

export default AboutTab;
