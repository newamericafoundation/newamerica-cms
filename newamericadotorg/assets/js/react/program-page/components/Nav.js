import { Component } from 'react';
import { NavLink } from 'react-router-dom';
import { Slider } from '../../components/Carousel';
import DocumentMeta from 'react-document-meta';
import titlefy from '../../../utils/titlefy';

const NavItem = ({ url, label, active }) => (
  <label className={`button--text link`}>
    <NavLink className={`program__nav__link ${active ? 'active' : ''}`} to={url}>
      {label}
    </NavLink>
  </label>
);


export default class Nav extends Component {
  items = () => {
    let { program, match } = this.props;
    let subpage = match.params.subpage;
    return [
      program.about && <li key={0}><NavItem url={`${program.url}about/`} label="About"/></li>,
      <li key={1}><NavItem url={`${program.url}our-people/`} label="Our People"/></li>,
      program.subprograms && <li key={2}><NavItem url={`${program.url}projects/`} label="Initiatives & Projects"/></li>,
      <li key={3}><NavItem url={`${program.url}publications/`} label="Publications" active={program.content_types.find((c)=>(c.slug===subpage))}/></li>,
      <li key={4}><NavItem url={`${program.url}events/`} label="Events"/></li>,
      program.topics && <li key={5}><NavItem url={`${program.url}topics/`} label="Topics"/></li>
    ];
  }

  getMeta = () => {
    let { match: { params: { subpage } }, program } = this.props;
    return {
      title: `${program.name}${subpage ? `: ${titlefy(subpage)}`: ''}`,
      description: program.description
    }

  }

  render(){
    let { program, match } = this.props;
    let subpage = match.params.subpage;
    return (
      <DocumentMeta {...this.getMeta()}>
        <div className={`program__nav ${subpage ? 'active' : ''}`}>
            <ul className="inline">
              <Slider
                  variableWidth={true}
                  infinite={false}
                  slide={'li'}
                  prevArrow={<div></div>}
                  nextArrow={<div></div>}
                  responsive={[
                    { breakpoint: 625, settings: { slidesToShow: 3, slidesToScroll: 3 } },
                    { breakpoint: 1000000, settings: 'unslick' }
                  ]}>
                    {this.items()}
                  </Slider>
            </ul>
        </div>
      </DocumentMeta>
    );
  }
}
