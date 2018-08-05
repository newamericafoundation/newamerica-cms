import './HorizontalNav.scss';

import { NavLink } from 'react-router-dom';
import React, { Component } from 'react';
import { Slider } from './Slider';

const NavItem = ({ url, label, exact=false, active }) => (
  <h5 className="link">
    <NavLink exact={exact} className={`horizontal-nav__link ${active ? 'active' : ''}`} to={url}>
      {label}
    </NavLink>
  </h5>
);

export default class Nav extends Component {
  getItems = () => {
    let { items, exact } = this.props;
    return items.filter(item => item !== false).map((item, i)=>(
      <li key={i}><NavItem exact={exact} {...item}/></li>
    ));
  }

  render(){
    return (
      <div className={`horizontal-nav ${this.props.className || ''}`}>
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
                {this.getItems()}
              </Slider>
        </ul>
      </div>
    );
  }
}
