import { Component } from 'react';
import { Response } from '../../components/API';
import { connect } from 'react-redux';

const ProgramsTab = ({ response: { results }}) => {
  return(
    <div className="menu-list programs-tab">
      {results.programs.map((p, i)=>(
        <label className="block">
          <a href={`/${p.slug}`}>{p.title}</a>
        </label>
      ))}
    </div>
  );
};

const AboutTab = () => (
  <div className="menu-list about-tab">
    <label className="block">
      <a href="/our-story">Our Story</a>
    </label>
    <label className="block">
      <a href="/our-people">Our People</a>
    </label>
    <label className="block">
      <a href="/our-funding">Our Funding</a>
    </label>
    <label className="block">
      <a href="/press">Press</a>
    </label>
    <label className="block">
      <a href="/jobs">Jobs</a>
    </label>
  </div>
);



class Menus extends Component {
  constructor(props) {
    super(props);
    this.state = { selectedTab: false };
  }

  componentDidUpdate(){
    if(!this.props.isOpen) this.setState({ selectedTab: false });
  }

  switchTab = (selectedTab) => {
      this.setState({ selectedTab });
  }

  render() {
    let { isOpen } = this.props;
    let { selectedTab } = this.state;
    return(
      <div className={`mobile-menu ${selectedTab ? `secondary-tab ${selectedTab.toLowerCase()}-tab-open` : ''} ${isOpen ? 'open' : ''}`}>
        <div className="mobile-menu__heading">
          <div className="logo__wrapper"><div className="logo sm"></div></div>
          <label className="tab-link-back button--text with-caret--left margin-0 block" onClick={()=>{this.switchTab(false);}}>
            {selectedTab}
          </label>
        </div>
        <div className="mobile-menu__menus">
          <div className="mobile-menu__primary">
            <div className="menu-list">
              <label className="block">
                <a href="/publications/">Publications</a>
              </label>
              <label className="block">
                <a href="/events/">Events</a>
              </label>
              <label className="block tab-link">
                <a onClick={()=>{this.switchTab('Programs');}}>Programs</a>
              </label>
              <label className="block tab-link">
                <a onClick={()=>{this.switchTab('About');}}>About</a>
              </label>
            </div>
          </div>
          <div className="mobile-menu__secondary">
            <AboutTab />
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
