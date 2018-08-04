import './Programs.scss';

import React, { Component } from 'react';
import { connect } from 'react-redux';

class Programs extends Component {
  getEven = (even, p, i) => {
    let isEven = i % 2 === 0;
    if(isEven !== even && even != 'all') return null;
    return (
      <div className="card program-card" key={`program-${i}`}>
        <div className="program-card__description">
          <h1 className="link card__text__title"><a href={p.url}><u>{p.title}</u></a></h1>
          <p>{p.description}</p>
        </div>
        {p.subprograms &&
          <div className="program-card__subprograms">
            <h4>Initiative & Projects</h4>
            <ul className="inline program-card__subprograms__list">
              {p.subprograms.map((s,i)=>(
                <li key={`program-${i}`}>
                  <h6 className="inline link">
                    <a href={s.url}><u>{s.title}</u></a>
                  </h6>
                </li>
              ))}
            </ul>
          </div>}
      </div>
    );
  }


  desktopCols = () => {
    /** split list on mobile columns **/
    let { response: { results } } = this.props;
    return (
      <div className="row gutter-10">
        <div className="col-md-6">
          {results.map((p,i)=>{
            return this.getEven(true,p,i);
          })}
        </div>
        <div className="col-md-6">
          {results.map((p,i)=>{
            return this.getEven(false,p,i);
          })}
        </div>
      </div>
    );
  }

  mobileCols = () => {
    let { response: { results } } = this.props;
    return (
      <div className="row gutter-10">
        <div className="col-md-6">
          {results.map((p,i)=>{
            return this.getEven('all',p,i);
          })}
        </div>
      </div>
    );
  }

  render(){
    let { windowWidth } = this.props;
    return (
      <div className="home__panel__promo home__panel__programs">
        <div className="container--1080">
          {windowWidth >= 768 && this.desktopCols()}
          {windowWidth < 768 && this.mobileCols()}
        </div>
      </div>
    );
  }
}

const mapStateToProps = (state) => ({
  windowWidth: state.site.windowWidth
});

export default Programs = connect(mapStateToProps)(Programs);
