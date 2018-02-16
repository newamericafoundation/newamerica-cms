import { Component } from 'react';
import { Response } from '../../components/API';
import { connect } from 'react-redux';

const ProgramsTab = ({ response: { results }}) => {
  return(
    <div className="menu-list programs-tab">
      {results.programs.sort((a,b) => (a.title > b.title ? 1 : -1)).map((p, i)=>(
        <label key={`program-${i}`} className="block">
          <a href={`/${p.slug}`}>{p.title}</a>
        </label>
      ))}
    </div>
  );
};

const AboutTab = ({ response: { results }}) => (
  <div className="menu-list about-tab">
    {results.about_pages.map((a,i)=>(
      <label key={`about-${i}`} className="block">
        <a href={a.url}>{a.title}</a>
      </label>
    ))}
  </div>
);



class Menus extends Component {
  constructor(props) {
    super(props);
    this.state = { selectedTab: false };
  }

  componentDidUpdate(prevProps){
    if(this.props.isOpen !== prevProps.isOpen && this.props.isOpen === false) this.setState({ selectedTab: false });
  }

  switchTab = (selectedTab) => {
      this.setState({ selectedTab });
  }

  render() {
    let { isOpen } = this.props;
    let { selectedTab } = this.state;
    return(
      <div className={`mobile-menu ${selectedTab ? `secondary-tab-active ${selectedTab.toLowerCase()}-tab-open` : ''} ${isOpen ? 'open' : ''}`}>
        <div className="mobile-menu__heading">
          <div className="logo__wrapper"><a href="/"><div className="logo sm"></div></a></div>
          <label className="tab-link-back button--text with-caret--left margin-0 block" onClick={()=>{this.switchTab(false);}}>
            {selectedTab}
          </label>
        </div>
        <div className="mobile-menu__tabs-wrapper">
          <div className="mobile-menu__primary-tab">
            <div className="menu-list">
              <label className="block tab-link">
                <a onClick={()=>{this.switchTab('About');}}>About</a>
              </label>
              <label className="block tab-link">
                <a onClick={()=>{this.switchTab('Programs');}}>Programs</a>
              </label>
              <label className="block">
                <a href="/publications/">Publications</a>
              </label>
              <label className="block">
                <a href="/events/">Events</a>
              </label>
            </div>
          </div>
          <div className="mobile-menu__secondary-tab">
            <Response name="meta" component={AboutTab} />
            <Response name="meta" component={ProgramsTab}/>
          </div>
        </div>
      </div>
    );
  }
}

const mapStateToProps = (state) => ({
  isOpen: state.site.mobileMenuIsOpen
});

export default Menus = connect(mapStateToProps)(Menus);
