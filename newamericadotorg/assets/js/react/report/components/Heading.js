import { Component } from 'react';

class Heading extends Component {
  render(){
    let { report } = this.props;
    return (
      <div className="report__heading row gutter-45">
        <div className="col-12 col-lg-10 offset-lg-1 offset-0">
          <div className="report__heading__title ">
            <h1 className="white no-margin centered">{report.title}</h1>
            {report.subheading &&
              <p className="subheading--h1 white">{report.subheading}</p>
            }
          </div>
          <div className="report__heading__image" style={{ backgroundImage: `url(${report.story_image})` }}/>
        </div>
      </div>
    );
  }
}

export default Heading;
