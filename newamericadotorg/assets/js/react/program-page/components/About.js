import { Component } from 'react';
import { Link, NavLink } from 'react-router-dom';

export default class About extends Component {
  componentWillMount(){
    if(window.scrollY > 300){
      window.scrollTo(0, 0);
    }
  }
  render(){
    let { about, about_us_pages, root } = this.props;

    return (
      <div className={`program__about margin-top-10 ${about_us_pages ? 'with-menu' : ''}`}>
        <div className="row">
          {about_us_pages &&
            <div className="program__about__menu col-md-2">
              <div className="menu-list--padding-15">
              {about_us_pages.map((p,i)=>(
                  <label className="block">
                    <NavLink to={`/${root}/about/${p.slug}/`}>{p.title}</NavLink>
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
