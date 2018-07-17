import { Component } from 'react';
import { Response } from '../../components/API';
import { connect } from 'react-redux';
import { Search } from '../../components/Icons';

const ProgramsTab = ({ response: { results }}) => {
  return(
    <div className="menu-list programs-tab">
      {results.programs.sort((a,b) => (a.title > b.title ? 1 : -1)).map((p, i)=>(
        <h6 key={`program-${i}`}>
          <a href={`/${p.slug}`}>{p.title}</a>
        </h6>
      ))}
    </div>
  );
};

const AboutTab = ({ response: { results }}) => (
  <div className="menu-list about-tab">
    {results.about_pages.map((a,i)=>(
      <h6 key={`about-${i}`}>
        <a href={a.url}>{a.title}</a>
      </h6>
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
          <a className="tab-link-back button--text with-caret--left margin-0 block" onClick={()=>{this.switchTab(false);}}>
            {selectedTab}
          </a>
        </div>
        <div className="mobile-menu__tabs-wrapper">
          <div className="mobile-menu__primary-tab">
            <div className="menu-list">
              <div className="input">
                <form action="/search/?query=value" method="get">
                  <Search />
                  <input type="text" autoComplete="off" name="query" id="search-input" placeholder="Search" />
                  <button type="submit" className="button--text with-caret--right">Go</button>
                </form>
              </div>
              <h6 className="tab-link">
                <a onClick={()=>{this.switchTab('About');}}>About</a>
              </h6>
              <h6 className="tab-link">
                <a onClick={()=>{this.switchTab('Programs');}}>Programs</a>
              </h6>
              <h6>
                <a href="/publications/">Publications</a>
              </h6>
              <h6>
                <a href="/events/">Events</a>
              </h6>
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
