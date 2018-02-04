import { NavLink } from 'react-router-dom';
import { Component } from 'react';

const NavItem = ({ url, label, exact=false }) => (
  <li>
    <NavLink exact className={`button--text program__nav__link`} to={url}>
      {label}
    </NavLink>
  </li>
);

export default class Nav extends Component {
  render(){
    return (
      <div className={`our-people__nav program__nav`}>
        <ul className="inline">
          <NavItem url={`/our-people/`} label="All People"/>
          <NavItem url={`/board/`} label="Board of Directors"/>
          <NavItem url={`/leadership/`} label="Leadership"/>
          <NavItem url={`/program-staff/`} label="Program Staff"/>
          <NavItem url={`/central-staff/`} label="Central Staff"/>
          <NavItem url={`/board-emeriti/`} label="Board Emeriti"/>
        </ul>
      </div>
    );
  }
}
