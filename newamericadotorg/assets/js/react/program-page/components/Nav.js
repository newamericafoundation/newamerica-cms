import { Component } from 'react';
import { NavLink } from 'react-router-dom';

const NavItem = ({ url, label, active }) => (
  <li>
    <NavLink className={`button--text program__nav__link ${active ? 'active' : ''}`} to={url}>
      {label}
    </NavLink>
  </li>
);


export default class Nav extends Component {

  render(){
    let { program, match } = this.props;
    let subpage = match.params.subpage;
    return (
      <div className={`program__nav ${subpage ? 'active' : ''}`}>
        <ul className="inline">
          <NavItem url={`${program.url}about/`} label="About"/>
          <NavItem url={`${program.url}publications/`} label="Publications" active={program.content_types.find((c)=>(c.slug===subpage))}/>
          <NavItem url={`${program.url}our-people/`} label="Our People"/>
          <NavItem url={`${program.url}events/`} label="Events"/>
          <NavItem url={`${program.url}topics/`} label="Topics"/>
        </ul>
      </div>
    );
  }
}
