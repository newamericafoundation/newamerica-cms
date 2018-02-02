import { Component } from 'react';

class Heading extends Component {
  state = {
    imageLoaded: false
  }

  onImageLoad = () => {
    this.setState({ imageLoaded: true });
  }

  render(){
    let { report } = this.props;
    return (
      <div className="report__heading row gutter-45">
        <div className="col-12 col-md-10 col-lg-11 col-xl-10 offset-md-1 offset-lg-0p5 offset-xl-1">
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
              <div className="temp-image" style={{
                paddingBottom: `45%`,
                backgroundImage: `url(${report.story_image_thumbnail})`
              }}/>
              <img className={`${this.state.imageLoaded ? 'loaded' : ''}`}
                src={report.story_image.url} onLoad={this.onImageLoad}/>
              {report.story_image.source && <label className="caption">{report.story_image.source}</label>}
            </div>
          }
        </div>
      </div>
    );
  }
}

export default Heading;
