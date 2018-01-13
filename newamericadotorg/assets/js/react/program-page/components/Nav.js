import { Component } from 'react';
import { NavLink } from 'react-router-dom';

const NavItem = ({ url, label }) => (
  <li>
    <NavLink className="button--text" to={url} activeStyle={{fontWeight: 'bold'}}>
      {label}
    </NavLink>
  </li>
);


export default class Nav extends Component {

  render(){
    let { program } = this.props;
    return (
      <div className="program__nav margin-bottom-35">
        <ul className="inline">
          <NavItem url={`${program.url}about/`} label="About" />
          <NavItem url={`${program.url}publications/`} label="Publications" />
        </ul>
      </div>
    );
  }
}
