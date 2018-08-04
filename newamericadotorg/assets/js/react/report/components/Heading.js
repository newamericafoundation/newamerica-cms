import React, { Component } from 'react';
import Image from '../../components/Image';
import { Doc } from '../../components/Icons';

class Heading extends Component {
  render(){
    let { report } = this.props;
    return (
      <div className="container">
      <div className="report__heading row gutter-30">
        <div className="col-12">
          <div className="report__heading__title margin-80">
            <div className="report__heading__bug centered">
              <Doc />
              <h4 className="centered margin-top-10 margin-bottom-25">Report</h4>
            </div>
            <div className='report__heading__programs centered'>
              <h5 className="inline">
                <a href={report.programs[0].url}>{report.programs[0].name}</a>
              </h5>
              {report.subprograms.length>0 && <h5 className="inline">
                ,&nbsp;
                <a className="" href={report.subprograms[0].url}>
                  {report.subprograms[0].name}
                </a>
              </h5>}
            </div>
            <h1 className="margin-25 centered">{report.title}</h1>
            {report.subheading &&
              <h6 className="subtitle centered">{report.subheading}</h6>
            }
          </div>
          {report.story_image &&
            <div className="report__heading__image post-heading__image">
              <div className="post-heading__image__wrapper">
                <Image thumbnail={report.story_image_thumbnail} image={report.story_image.url}/>
              </div>
              {report.story_image.source && <h6 className="caption inline">{report.story_image.source}</h6>}
            </div>
          }
        </div>
      </div>
      </div>
    );
  }
}

export default Heading;
