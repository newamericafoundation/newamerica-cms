import React, { Component } from 'react';
import { Route } from 'react-router-dom'
import { Fetch } from '../../components/API'
import { ImageAside, Reel, Body, NavItem } from '../components';
import Programs from './Programs';
import { NAME } from '../constants';
import { PlusX } from '../../components/Icons';

class Jobs extends Component {
  state = {
    expanded: {}
  }

  toggleExpand = (i) => {
    this.setState({ expanded: { ...this.state.expanded, [i]: !this.state.expanded[i] }});
  }

  render(){
    let { response: { results } } = this.props;
    let { expanded } = this.state

    return (
      <section className="padding-80">
        <div className="container--1080 home__fellowships">
          <div className="menu-list">
            {results.sort((a,b)=>(a.title > b.title ? 1 : -1)).map((j,i)=>(
              <div key={`fellowship-${i}`} className={`${expanded[i] ? 'expanded ' : ''}home__fellowship`}>
                <PlusX x={expanded[i]} />
                <h2 onClick={()=>{ this.toggleExpand(i) }}>{j.title}</h2>
                <div>
                  <span className="home__fellowship__more__label">
                    <h4 className="inline">Location: </h4>
                    <h6 className="inline">{j.city ? `${j.city}, ` : ''}{j.state} </h6>
                  </span>
                  <span className="home__fellowship__more__label">
                    <h4 className="inline">Department:</h4>
                    <h6 className="inline">{j.department}</h6>
                  </span>
                  <span className="home__fellowship__more__label">
                    <h4 className="inline">Type:</h4>
                    <h6 className="inline">{j.type}</h6>
                  </span>
                </div>
                <div className="home__fellowship__more">
                  <div className="margin-0 home__fellowship__more__description"
                    dangerouslySetInnerHTML={{__html: j.description}} />
                  <div className="home__fellowship__more__button">
                    <a className="button" href={`http://newamerica.applytojob.com/apply/${j.board_code}/`} target="_blank">Apply</a>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    );
  }
}

class Fellowships extends Component {
  state = {
    expanded: {}
  }

  toggleExpand = (i) => {
    this.setState({ expanded: { ...this.state.expanded, [i]: !this.state.expanded[i] }});
  }

  render(){
    let { data : { fellowships_list: { resource_kit } } } = this.props;
    let { expanded } = this.state;

    return (
      <section className="padding-80">
        <div className="container--1080 home__fellowships">
          <div className="menu-list">
            {resource_kit[0].resources.map((f,i)=>(
              <div key={`fellowship-${i}`} className={`${expanded[i] ? 'expanded ' : ''}home__fellowship`}>
                <PlusX x={expanded[i]} />
                <h2 onClick={()=>{ this.toggleExpand(i) }}>{f.value.name}</h2>
                <div className="home__fellowship__more">
                  <div dangerouslySetInnerHTML={{__html: f.value.description}} />
                  {f.value.resource !== '/' && <a className="button" href={f.value.resource}>See Fellowship Page</a>}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    );
  }
}

class Nav extends Component {
  render(){
    return (
      <div className={`container--1080 our-funding__nav margin-top-15`}>
        <ul className="inline">
          <li><NavItem url={`/jobs/`} exact={true} label="Jobs"/></li>
          <li><NavItem url={`/jobs/fellowships/`} exact={true} label="Fellowships"/></li>
        </ul>
      </div>
    );
  }
}

export default class JobsAndFellowships extends Component {
  findSubpage = (slug) => {
    let { response: { results } } = this.props;
    return results.subpages.find(s=>s.slug===slug);
  }
  render(){
    return (
      <div className="home__panels__content">
        <Nav />
        <Route exact path="/jobs/" render={()=>(
          <Fetch endpoint={`jobs`}
            fetchOnMount={true}
            name={`${NAME}.jobs`}
            component={Jobs} />
        )}/>
        <Route exact path="/jobs/fellowships/" render={()=>(
          <Fellowships data={this.findSubpage('fellowships').data} />
        )}/>
      </div>
    );
  }
}
