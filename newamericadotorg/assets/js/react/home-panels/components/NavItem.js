import React from 'react';
import { NavLink } from 'react-router-dom';

const NavItem = ({ url, label, exact=false }) => (
  <h5 className="inline link">
    <NavLink exact className={`button--text horizontal-nav__link`} to={url}>
      {label}
    </NavLink>
  </h5>
);

export default NavItem;
