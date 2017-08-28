import { Component } from 'react';
import { Response } from '../../components/API';

const TabSelector = ({ switchTab, selectedTab, options }) => (
  <div className="inline-toggles">
    {options.map((o,i)=>(
      <div className={`inline-toggles__item ${selectedTab==o ? 'selected' : ''}`}>
        <a onClick={()=>{ switchTab(o)} }>{o}</a>
      </div>
    ))}
  </div>
);


const PublicationTab = () => (
  <div className="tabs__tab row gutter-10">
    <div className="col-6">
      <div className="tabs__tab__list-item">
        <a href="/books">Books</a>
      </div>
      <div className="tabs__tab__list-item">
        <a href="/blogs">Blog Posts</a>
      </div>
      <div className="tabs__tab__list-item">
        <a href="/policy-papers">Policy Papers</a>
      </div>
      <div className="tabs__tab__list-item">
        <a href="/in-the-news">In the News</a>
      </div>
      <div className="tabs__tab__list-item">
        <a href="/podcasts">Podcasts</a>
      </div>
      <div className="tabs__tab__list-item">
        <a href="/press-releases">Press Releases</a>
      </div>
    </div>
    <div className="col-6">
      <div className="tabs__tab__list-item">
        <a href="/events">Events</a>
      </div>
      <div className="tabs__tab__list-item">
        <a href="/weekly">Weekly</a>
      </div>
      <div className="tabs__tab__list-item">
        <a href="/in-depth">In Depth</a>
      </div>
    </div>
  </div>
);

const ProgramsTab = ({ response: { results }}) => {
  let programs = [...results];
  let halfIndex = Math.round(programs.length/2);
  let programsTail = programs.splice(halfIndex, programs.length-halfIndex);
  return(
    <div className="tabs__tab programs-tab row">
      <div className="col-md-6 col-12">
      {programs.map((p, i)=>(
        <div className="tabs__tab__list-item">
          <a href={`/${p.slug}`}>{p.name}</a>
        </div>
      ))}
      </div>
      <div className="col-md-6 col-12">
      {programsTail.map((p, i)=>(
        <div className="tabs__tab__list-item">
          <a href={`/${p.slug}`}>{p.name}</a>
        </div>
      ))}
      </div>
    </div>
  );
};

const AboutTab = () => (
  <div className="tabs__tab">
    <div className="tabs__tab__list-item">
      <a href="/our-story">Our Story</a>
    </div>
    <div className="tabs__tab__list-item">
      <a href="/our-people">Our People</a>
    </div>
    <div className="tabs__tab__list-item">
      <a href="/our-funding">Our Funding</a>
    </div>
    <div className="tabs__tab__list-item">
      <a href="/press">Press</a>
    </div>
    <div className="tabs__tab__list-item">
      <a href="/jobs">Jobs</a>
    </div>
  </div>
);



export default class Tabs extends Component {
  constructor(props) {
    super(props);
    this.state = { selectedTab: 'Our Work' };
  }

  switchTab = (selectedTab) => {
      this.setState({ selectedTab });
  }

  render() {
    let { selectedTab } = this.state;
    return(
      <div className="tabs">
        <TabSelector selectedTab={selectedTab} switchTab={this.switchTab} options={['Our Work', 'Programs', 'About']}/>
        <div className="tabs-wrapper">
          {selectedTab == 'Our Work' && <PublicationTab />}
          {selectedTab == 'Programs' && <Response name="programData" component={ProgramsTab}/>}
          {selectedTab == 'About' && <AboutTab />}
        </div>
      </div>
    );
  }
}
