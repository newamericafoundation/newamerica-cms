import { Component } from 'react';

class Heading extends Component {
  render(){
    let { report } = this.props;
    return (
      <div className="report__heading row gutter-45">
        <div className="col-12 col-xl-10 offset-xl-1 offset-0">
          <div className="report__heading__title ">
            <div className='report__heading__logo'>
              <div className='logo bug white-transparent' style={{ width: '40px', height: '32px' }}/>
              <div className='report__heading__logo__program'>
                <label className='bold'>{report.programs[0].name}</label>
              </div>
              {/*report.subprograms.length && <div className='report__heading__logo__program'>
                <label>{report.programs[0].name}</label>
              </div>*/}
            </div>
            <h1 className="white margin-0 centered">{report.title}</h1>
            {report.subheading &&
              <label className="block centered white">{report.subheading}</label>
            }
          </div>
          <div className="report__heading__image" style={{ backgroundImage: `url(${report.story_image})` }}/>
          <div className="report__heading__image__caption"><label className="caption">Source: Lorem Ipsum Dolor Sit Amet / Caption</label></div>
        </div>
      </div>
    );
  }
}

export default Heading;
