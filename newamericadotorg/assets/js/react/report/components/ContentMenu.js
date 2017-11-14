import { Link } from 'react-router-dom';
import { Component } from 'react';

class ContentMenu extends Component {
  state = { expanded: {} }
  constructor(props){
    super(props);
    props.report.sections.map((s)=>{
      this.state[s.title] = false;
    });
  }

  toggleExpanded = (title) => {
    this.setState({ expanded: { ...this.state.expanded, [title]: !this.state.expanded[title] }});
  }

  render(){
    let { report: { url, sections }, open, closeMenu, activeSection } = this.props;
    return (
      <div className={`report__content-menu ${open ? 'open' : ''}`}>
        {sections.map((s,i)=>(
          <span>
            <div className={`report__content-menu__item ${activeSection==s ? 'active' : ''}`}>
              <Link to={`${url}${s.slug}`} onClick={closeMenu}>
                <label className="white">{s.title}</label>
              </Link>
              {s.subsections.length>0 && <div className="report__content-menu__item__toggle fa fa-plus" onClick={()=>{this.toggleExpanded(s.title)}}/>}
            </div>
            <span className={'report__content-menu__item__subsections' + (this.state.expanded[s.title] ? ' expanded' : '')}>
            {s.subsections.map((sub,i)=>(
              <div className={`report__content-menu__item`} onClick={closeMenu}>
                <Link to={`${url}${sub.slug}`}>
                  <label className="report__content-menu__item__subsections__label block">{sub.title}</label>
                </Link>
              </div>
            ))}
            </span>
          </span>
        ))}
      </div>
    );
  }
}
export default ContentMenu;
