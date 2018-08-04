import { NavLink } from 'react-router-dom';
import React, { Component } from 'react';
import { Slider } from '../../components/Slider';

const NavItem = ({ url, label, exact=false }) => (
  <h5 className="inline link">
    <NavLink exact className={`horizontal-nav__link`} to={url}>
      {label}
    </NavLink>
  </h5>
);

export default class Nav extends Component {
  items = () => {

    return [
      <li key="1"><NavItem url={`/our-people/`} label="All People"/></li>,
      <li key="2"><NavItem url={`/board/`} label="Board of Directors"/></li>,
      <li key="3"><NavItem url={`/leadership/`} label="Leadership"/></li>,
      <li key="4"><NavItem url={`/program-staff/`} label="Program Staff"/></li>,
      <li key="5"><NavItem url={`/central-staff/`} label="Central Staff"/></li>,
      <li key="6"><NavItem url={`/board-emeriti/`} label="Board Emeriti"/></li>
    ];
  }
  render(){
    return (
      <div className={`our-people__nav horizontal-nav`}>
        <ul className="inline">
          <Slider
              variableWidth={true}
              infinite={false}
              slide={'li'}
              prevArrow={<div></div>}
              nextArrow={<div></div>}
              responsive={[
                { breakpoint: 625, settings: { slidesToShow: 3, slidesToScroll: 1 } },
                { breakpoint: 1000000, settings: 'unslick' }
              ]}>
                {this.items()}
              </Slider>
        </ul>
      </div>
    );
  }
}
