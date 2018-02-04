import { Link } from 'react-router-dom';
import { Component } from 'react';
import { connect } from 'react-redux';

class ContentMenu extends Component {
  state = { expanded: {}, lastScrollPosition: 0 }
  constructor(props){
    super(props);
    props.report.sections.map((s)=>{
      this.state.expanded[s.title] = s.title == props.activeSection.title;
    });
  }

  toggleExpanded = (title) => {
    this.setState({ expanded: { ...this.state.expanded, [title]: !this.state.expanded[title] }});
  }

  closeMenu = (title) => {
    let expanded = {};
    this.props.report.sections.map((s)=>{
      expanded[s.title] = s.title == title;
    });
    this.setState({ expanded });
    this.props.closeMenu();
  }

  render(){
    let { report: { url, sections }, open, closeMenu, activeSection } = this.props;
    return (
      <div className="report__content-menu">
        {sections.map((s,i)=>(
          <span className={this.state.expanded[s.title] ? 'expanded' : ''}>
            <div className={`report__content-menu__item${activeSection.slug==s.slug? ' active' : ''}`}>
              <Link to={`${url}${s.slug}/`} onClick={()=>{this.closeMenu(s.title);}}>
                <label className="white">{s.title}</label>
              </Link>
              {s.subsections.length>0 && <div className="report__content-menu__item__toggle fa fa-plus" onClick={()=>{this.toggleExpanded(s.title)}}/>}
            </div>
            <span className='report__content-menu__item__subsections'
              style={{ maxHeight: this.state.expanded[s.title] ? `${80*(s.subsections.length)}px` : 0}}>
            {s.subsections.map((sub,i)=>(
              <div className={`report__content-menu__item${activeSection.slug==s.slug? ' active' : ''}`} onClick={closeMenu}>
                <Link to={`${url}${s.slug}/#${sub.slug}`}>
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

const mapStateToProps = (state) => ({
  windowScrollPosition: state.site.scroll.position
});

export default connect(mapStateToProps)(ContentMenu);
