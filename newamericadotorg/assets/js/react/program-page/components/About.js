import { Component } from 'react';
import { Link, NavLink } from 'react-router-dom';

export default class About extends Component {
  componentWillMount(){
    if(window.scrollY > 300){
      window.scrollTo(0, 0);
    }
  }
  render(){
    let { about, about_us_pages, program } = this.props;

    return (
      <div className={`program__about margin-top-10 ${about_us_pages ? 'with-menu' : ''}`}>
        <div className="row">
          {about_us_pages &&
            <div className="program__about__menu col-md-2 margin-bottom-35">
              <div className="menu-list--padding-15">
                <label className="block">
                  <NavLink exact to={`${program.url}about/`}>About Us</NavLink>
                </label>
              {about_us_pages.map((p,i)=>(
                  <label key={i} className="block">
                    <NavLink to={`${program.url}${p.slug}/`}>{p.title}</NavLink>
                  </label>
              ))}
              </div>
            </div>
          }
          <div className="program__about__body post-body col-md-8" dangerouslySetInnerHTML={{__html: about.body || about}} />
        </div>
      </div>
    );
  }
}
