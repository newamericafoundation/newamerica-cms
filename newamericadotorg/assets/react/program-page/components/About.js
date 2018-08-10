import './About.scss';

import React, { Component } from 'react';
import { render } from 'react-dom';
import { Link, NavLink, Route } from 'react-router-dom';
import { APP as Resources, ID as resourcesDOMId }  from '../../blocks/resources';
import getProps from '../../../lib/utils/get-props';

class AboutBody extends Component {
  // hack for loading resources react component inside defined in django template
  addResourcesBlocks = () => {
    let resources = document.querySelectorAll(`.na-react__${resourcesDOMId}`);
    if(!resources) return;

    for(let r of resources){
      // already rendered
      if(r.hasChildNodes()) continue;
      let props = getProps(r);
      render(
        <Resources {...props} />, r
      );
    }
  }
  componentDidMount(){
    this.addResourcesBlocks();
  }

  componentDidUpdate(){
    this.addResourcesBlocks();
  }

  render(){
    let { body } = this.props;
    return (
      <div className="program__about__body post-body col-md-8"
          dangerouslySetInnerHTML={{ __html: body }} />
    );
  }
}

export default class About extends Component {
  componentWillMount(){
    if(window.scrollY > 300 || window.pageYOffset > 300){
      window.scrollTo(0, 0);
    }
  }

  getSubpageBody = (slug) => {
    let { about: { subpages }} = this.props;

    let p = subpages.find(s => s.slug === slug);
    if(!p) return null;
    else return p.body;
  }

  render(){
    let { about, program, root } = this.props;
    let { subpages } = about;
    
    return (
      <div className={`program__about margin-top-10 ${subpages.length > 0 ? 'with-menu' : ''}`}>
        <div className="row">
          {subpages.length>0 && <div className="program__about__menu col-md-2 margin-bottom-35">
            <span>
              <div className="">
                <h6 className="link margin-top-5 margin-bottom-15">
                  <NavLink exact to={`${program.url}about/`}>About</NavLink>
                </h6>
              {subpages.map((p,i)=>(
                  <h6 key={i} className="link margin-top-0 margin-bottom-15">
                    <NavLink to={p.url}>{p.title}</NavLink>
                  </h6>
              ))}
              </div>
            </span>
          </div>}
          <Route exact path={`/${root}/about/`} render={()=>(
            <AboutBody body={about.body}/>
          )}/>
          <Route exact path={`/${root}/about/:subpage`} render={({match})=>(
            <AboutBody body={this.getSubpageBody(match.params.subpage)}/>
          )}/>
        </div>
      </div>
    );
  }
}
