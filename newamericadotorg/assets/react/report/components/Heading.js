import './Heading.scss';

import React, { Component } from 'react';
import Image from '../../components/Image';
import { Report } from '../../components/Icons';
import { Link } from 'react-router-dom'

class Heading extends Component {
  render(){
    let { report } = this.props;
    let { authors } = report;
    let _authors = [...authors];
    if(_authors.length > 3) {
      _authors = _authors.splice(0,3);
      _authors.push({ first_name: authors.length - 3, last_name: 'more', url:"#authors" });
    }
    return (
      <React.Fragment>
        <div className="report__heading container">
          <div className="report__heading__bug centered margin-bottom-35">
            <Report />
            <h4 className="centered margin-top-5 margin-bottom-0">Report</h4>
          </div>
          <div className="report__heading__title">
            <h1 className="margin-0 centered">{report.title}</h1>
            {report.subheading &&
              <h6 className="subtitle centered margin-top-25 margin-bottom-0">{report.subheading}</h6>
            }
          </div>
          <div className='report__heading__authors centered'>
          <h6 className="margin-0 centered inline">By: </h6>
            {_authors.map((a,i)=>(
              <React.Fragment key={`author-${i}`}>
                <h6 className="margin-0 centered inline">
                  <a href={a.url} style={{ fontWeight: a.last_name==='more' ? 'bold' : 'regular'}}>{a.first_name}&nbsp;{a.last_name}</a>
                </h6>
                {(_authors.length > 2 && i < _authors.length-2) && ', '}
                {(_authors.length==2 && i === 0) && ' and '}
                {(_authors.length > 2 && i === _authors.length-2) && ', and '}
              </React.Fragment>
            ))}
          </div>
          <div className='report__heading__programs margin-top-15'>
            {report.programs.map((p,i)=>(
              <h5 className="margin-0 centered" key={`program-${i}`}>
                <a href={p.url}>{p.name}</a>
              </h5>
            ))}
          </div>
        </div>
        {report.story_image &&
          <div className="report__cover-image post-heading__image">
            <div className="post-heading__image__wrapper">
              <Image thumbnail={report.story_image_thumbnail} image={report.story_image.url}/>
            </div>

            {report.story_image.source &&
              <div className="container">
                <h6 className="caption margin-bottom-0 margin-top-15">{report.story_image.source}</h6>
              </div>
            }
          </div>
        }
      </React.Fragment>
    );
  }
}

export default Heading;
