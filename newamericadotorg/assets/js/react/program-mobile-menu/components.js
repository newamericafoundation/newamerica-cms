import { Component } from 'react';

const ProjectsTab = ({projects}) => (
  <div className="tabs__tab">
    {projects.map((p)=>(
      <div className="tabs__tab__list-item">
        <a href={p.url}>{p.title}</a>
      </div>
    ))}
  </div>
);

const TopicsTab = ({topics}) => (
  <div className="tabs__tab">
    {topics.map((t)=>(
      <div className="tabs__tab__list-item">
        <a href={t.url}>{t.title}</a>
      </div>
    ))}
  </div>
);

const Toggles = ({ switchTab, program, selectedTab }) => (
  <div className="inline-toggles-wrapper">
    <div className="inline-toggles">
      <div className={`inline-toggles__item${selectedTab=='Projects' ? ' selected' : ''}`}>
        <a onClick={()=>{switchTab('Projects')}}>Projects</a>
      </div>
      <div className={`inline-toggles__item${selectedTab=='Topics' ? ' selected' : ''}`}>
        <a onClick={()=>{switchTab('Topics')}}>Topics</a>
      </div>
      {program.subpages.find((p)=>(p.slug=='events')) &&
        <div className='inline-toggles__item'>
          <a href={`/${program.slug}/events`}>Events</a>
        </div>
      }
      <div className='inline-toggles__item'>
        <a href="#publications">Publications</a>
      </div>
      {program.subpages.find((p)=>(p.slug=='about-us')) &&
        <div className='inline-toggles__item'>
          <a href={`/${program.slug}/about-us`}>About</a>
        </div>
      }
      <div className='inline-toggles__item'>
        <a href="#subscribe">Subscribe</a>
      </div>
    </div>
  </div>
);

export default class Menu extends Component {
  constructor(props) {
    super(props);
    this.state = { selectedTab: 'Projects' };
  }

  switchTab = (selectedTab) => {
      this.setState({ selectedTab });
  }

  render(){
    let { response: { results }} = this.props;
    let { selectedTab } = this.state;
    return (
      <div className="tabs">
        <Toggles program={results} selectedTab={selectedTab} switchTab={this.switchTab}/>
        <div className="tabs-wrapper">
          {selectedTab == 'Projects' && <ProjectsTab projects={results.projects}/>}
          {selectedTab == 'Topics' && <TopicsTab topics={results.topics}/>}
        </div>
      </div>
    );
  }
}
