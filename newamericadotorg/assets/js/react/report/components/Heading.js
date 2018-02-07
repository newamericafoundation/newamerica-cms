import { Component } from 'react';
import Image from '../../components/Image';

class Heading extends Component {
  render(){
    let { report } = this.props;
    return (
      <div className="container">
      <div className="report__heading row gutter-30">
        <div className="col-12">
          <div className="report__heading__title margin-80">
            <div className="report__heading__bug centered">
              <i className="fa fa-file-text-o lg"></i>
              <label className="bold block centered margin-top-10 margin-bottom-25">Report</label>
            </div>
            <div className='report__heading__programs centered'>
              <a className="button--text" href={report.programs[0].url}>{report.programs[0].name}</a>
              {report.subprograms.length>0 && <a className="button--text" href={report.subprograms[0].url}>
                {report.programs[0].name}
              </a>}
            </div>
            <h1 className="margin-25 centered">{report.title}</h1>
            {report.subheading &&
              <label className="subtitle centered">{report.subheading}</label>
            }
          </div>
          {report.story_image &&
            <div className="report__heading__image post-heading__image">
              <div className="post-heading__image__wrapper">
                <Image thumbnail={report.story_image_thumbnail} image={report.story_image.url}/>
              </div>
              {report.story_image.source && <label className="caption">{report.story_image.source}</label>}
            </div>
          }
        </div>
      </div>
      </div>
    );
  }
}

export default Heading;
