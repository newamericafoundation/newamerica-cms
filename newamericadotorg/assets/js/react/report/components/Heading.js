import { Component } from 'react';

class Heading extends Component {
  render(){
    let { report } = this.props;
    return (
      <div className="report__heading row gutter-45">
        <div className="col-12 col-md-10 col-lg-11 col-xl-10 offset-md-1 offset-lg-0p5 offset-xl-1">
          <div className="report__heading__title margin-60">
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
          <div className="report__heading__image" style={{ backgroundImage: `url(${report.story_image})` }}/>
          <div className="report__heading__image__caption margin-top-5 margin-top-lg-10"><label className="caption">Source: Lorem Ipsum Dolor Sit Amet / Caption</label></div>
        </div>
      </div>
    );
  }
}

export default Heading;
