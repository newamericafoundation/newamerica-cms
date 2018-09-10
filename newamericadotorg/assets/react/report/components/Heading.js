import './Heading.scss';

import React, { Component } from 'react';
import Image from '../../components/Image';
import { Doc } from '../../components/Icons';
import { Link } from 'react-router-dom'

class Heading extends Component {
  render(){
    let { report } = this.props;
    let { authors } = report;
    return (
      <div className="container">
        <div className="report__heading">
          <div className="report__heading__bug centered margin-bottom-35">
            <Doc />
            <h4 className="centered margin-top-15 margin-bottom-0">Report</h4>
          </div>
          <div className="report__heading__title margin-bottom-35">
            <h1 className="margin-0 centered">{report.title}</h1>
            {report.subheading &&
              <h6 className="subtitle centered margin-top-10">{report.subheading}</h6>
            }
          </div>
          <div className='report__heading__authors centered'>
            {authors.map((a,i)=>(
              <React.Fragment key={`author-${i}`}>
                <h6 className="margin-0 centered inline">
                  <a href={a.url}>{a.first_name}&nbsp;{a.last_name}</a>
                </h6>
                {(authors.length > 2 && i < authors.length-2) && ', '}
                {(authors.length==2 && i === 0) && ' and '}
                {(authors.length > 2 && i === authors.length-2) && ', and '}
              </React.Fragment>
            ))}
          </div>
          <div className='report__heading__programs'>
            {report.programs.map((p,i)=>(
              <h5 className="margin-0 centered" key={`program-${i}`}>
                <a href={p.url}>{p.name}</a>
              </h5>
            ))}
          </div>
        </div>
        {report.story_image &&
          <div className="report__heading__image post-heading__image">
            <div className="post-heading__image__wrapper">
              <Image thumbnail={report.story_image_thumbnail} image={report.story_image.url}/>
            </div>
            {report.story_image.source && <h6 className="caption margin-bottom-0 margin-top-25">{report.story_image.source}</h6>}
          </div>
        }
      </div>
    );
  }
}

export default Heading;
