import { Component } from 'react';
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
                    <label className="bold">Location: </label>
                    <label>{j.city ? `${j.city}, ` : ''}{j.state} </label>
                  </span>
                  <span className="home__fellowship__more__label">
                    <label className="bold">Department:</label>
                    <label>{j.department}</label>
                  </span>
                  <span className="home__fellowship__more__label">
                    <label className="bold">Type:</label>
                    <label>{j.type}</label>
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
    let { response: { results } } = this.props;
    let { expanded } = this.state
    return (
      <section className="padding-80">
        <div className="container--1080 home__fellowships">
          <div className="menu-list">
            {results.map((f,i)=>(
              <div key={`fellowship-${i}`} className={`${expanded[i] ? 'expanded ' : ''}home__fellowship`}>
                <PlusX x={expanded[i]} />
                <h2 onClick={()=>{ this.toggleExpand(i) }}>{f.title}</h2>
                <div className="home__fellowship__more">
                  <p className="margin-0 home__fellowship__more__description">{f.description}</p>
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
          <li><NavItem url={`/fellowships/`} exact={true} label="Fellowships"/></li>
        </ul>
      </div>
    );
  }
}

export default class JobsAndFellowships extends Component {
  render(){
    return (
      <div className="home__panels__content">
        <Nav />
        <Route path="/jobs/" render={()=>(
          <Fetch endpoint={`jobs`}
            fetchOnMount={true}
            name={`${NAME}.jobs`}
            component={Jobs} />
        )}/>
        <Route path="/fellowships/" render={()=>(
          <Fetch endpoint={`program/fellowships`}
            fetchOnMount={true}
            name={`${NAME}.fellowships`}
            component={Fellowships} />
        )}/>
      </div>
    );
  }
}
