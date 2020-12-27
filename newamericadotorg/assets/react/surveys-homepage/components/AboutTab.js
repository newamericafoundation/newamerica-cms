import './AboutTab.scss';

import React, { Component } from 'react';
import Authors from '../../report/components/Authors';

class AboutTab extends Component {
  constructor(props) {
    super(props);
  }
  render() {
    const { data } = this.props;
    const tempSections = [
      {
        title: 'About This Project',
        body:
          '<div class="block-paragraph"><div class="rich-text"><p>The HigherEd Polling Dashboard comprises public opinion surveys on higher education that have been conducted in the U.S. since 2010. Surveys in the dashboard explore the general public’s opinion on issues pertaining to higher education such as funding, diversity, and value. Some focus on opinion of first-year college students, college and university presidents, and faculty. The dashboard is a helpful source for researchers, journalists, and the general public who are interested in understanding public opinion on higher education issues. It is, however, by no means an exhaustive source of public opinion surveys about higher education. If you know of a survey that could be added to the site, please email the survey to <a href="mailto:nguyens@newamerica.org"> nguyens@newamerica.org.</a></p></div></div>',
      },
      {
        title: 'Methodology',
        body:
          '<div class="block-paragraph"><div class="rich-text"><p>Surveys in the dashboard were collected by searching “higher education public opinion survey” in Google News. To be added, the survey needed to address the general public or other groups&#x27; opinion on at least one issue in higher education, be transparent about the methodology, and add the margins of error included where possible. Most of the surveys in the dashboard are nationally representative, but some surveys that look into a specific population such as students, faculty, or administrators, may only capture the responses of those surveyed. To capture relatively recent data, we chose 2010 as the first year in which to include surveys; those before 2010 were excluded.</p></div></div>',
      },
      {
        title: 'Submit a Report',
        body:
          '<div class="block-paragraph"><div class="rich-text"><p></p>Know of a survey or report that should be added to our list? <a href="mailto:nguyens@newamerica.org">Send us and email.</a></p></div></div>',
      },
      {
        title: 'Made Possible By',
        body:
          '<div class="block-paragraph"><div class="rich-text"><img src="https://shotatlife.org/wp-content/uploads/2016/02/bill-melinda-gates-foundation-logo-png-transparent.png" alt="Bill and Melinda Gates foundation logo"></div></div>',
      },
    ];
    return (
      <div className="surveys-about-tab">
        {tempSections.map((section, i) => (
          <div
            className="surveys-about-tab__section"
            key={`about-section${i}`}
          >
            <h2 className="surveys-about-tab__section-title">
              {section.title}
            </h2>
            <div
              className="surveys-about-tab__description"
              dangerouslySetInnerHTML={{ __html: section.body }}
            />
          </div>
        ))}

        <div className="surveys-about-tab__section">
          <h2 className="surveys-about-tab__section-title">
            Authors
          </h2>
          <Authors authors={data.authors} md={true} />
        </div>
      </div>
    );
  }
}

export default AboutTab;
