import { Component } from 'react';
import { SET_ANY_STATE } from '../constants';

const SubprogramsTab = ({subprograms}) => (
  <div className="tabs__tab">
    {subprograms.map((p)=>(
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

const Toggles = ({ switchTab, program, selectedTab, closeMenu }) => (
  <div className="inline-toggles-wrapper">
    <div className="inline-toggles">
      {program.subprograms.length > 0 &&
        <div className={`inline-toggles__item${selectedTab=='Subprograms' ? ' selected' : ''}`}>
          <a onClick={()=>{switchTab('Subprograms')}}>Subprograms</a>
        </div>}
      {program.topics.length > 0 &&
        <div className={`inline-toggles__item${selectedTab=='Topics' ? ' selected' : ''}`}>
          <a onClick={()=>{switchTab('Topics')}}>Topics</a>
        </div>}
      {program.subpages.find((p)=>(p.slug=='events')) &&
        <div className='inline-toggles__item'>
          <a href={`/${program.slug}/events`}>Events</a>
        </div>}
      <div className='inline-toggles__item'>
        <a onClick={closeMenu} href="#publications">Publications</a>
      </div>
      {program.subpages.find((p)=>(p.slug=='about-us')) &&
        <div className='inline-toggles__item'>
          <a href={`/${program.slug}/about-us`}>About</a>
        </div>}
      <div className='inline-toggles__item'>
        <a onClick={closeMenu} href="#subscribe">Subscribe</a>
      </div>
    </div>
  </div>
);

export default class Menu extends Component {
  constructor(props) {
    super(props);
    this.state = { selectedTab: 'Subprograms' };
  }

  switchTab = (selectedTab) => {
      this.setState({ selectedTab });
  }

  closeMenu = () => {
    this.props.dispatch({
      type: SET_ANY_STATE,
      component: 'program.mobileMenuIsOpen',
      state: false
    });
  }

  render(){
    let { response: { results }} = this.props;
    let { selectedTab } = this.state;
    return (
      <div className="tabs">
        <Toggles program={results} selectedTab={selectedTab} switchTab={this.switchTab} closeMenu={this.closeMenu}/>
        <div className="tabs-wrapper">
          {selectedTab == 'Subprograms' && <SubprogramsTab subprograms={results.subprograms}/>}
          {selectedTab == 'Topics' && <TopicsTab topics={results.topics}/>}
        </div>
      </div>
    );
  }
}
