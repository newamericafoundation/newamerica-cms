import { NAME } from '../constants';
import { Component } from 'react';
import { Fetch, Response } from '../../components/API';
import { TypeFilter, SubprogramFilter, DateFilter, TopicFilter, FilterGroup } from '../../components/Publications';
import { PublicationsList } from '../../components/Publications';

// must pass an response object from Fetch of Response component, history and location to FilterGroup
const Filters = (props) => (
  <FilterGroup
    history={props.history}
    location={props.location}
    response={props.response}
    programUrl={props.program.url}>
    <TypeFilter key="typefilter" types={props.program.content_types.sort((a,b) => a.name > b.name)} expanded={props.initialQuery.content_type != undefined} label="Type"/>
    {props.program.subprograms &&
    <SubprogramFilter key="subprogramfilter" subprograms={props.program.subprograms} label="Project"/>}
    <DateFilter key="datefilter" label="Date"/>
    {props.program.topics &&
    <TopicFilter key="topicfilter" topics={props.program.topics} label="Topic"/>}
  </FilterGroup>
);

export default class Publications extends Component {
  state = {
    filtersOpen: false
  }
  componentWillMount(){
    if(window.scrollY > 300){
      window.scrollTo(0, 0);
    }
  }
  initialQuery = () => {
    let { programType, program, location } = this.props;
    let program_id = programType == 'program' ? 'program_id' : 'subprogram_id';

    let initQuery = {
      [program_id]: program.id,
      image_rendition: 'max-300x240',
      page_size: 8,
      page: 1
    }

    let params = new URLSearchParams(location.search.replace('?', ''));
    if(programType=='program' && params.get('projectId'))
      initQuery.subprogram_id = params.get('projectId');

    let slug = location.pathname.match(/.+\/(.+)\/$/i)[1];
    let type = program.content_types.find((t)=>(t.slug === slug ));
    if(type) initQuery.content_type = type.api_name;

    return initQuery;
  }

  toggleMobileFilters = () => {
    this.setState({ filtersOpen: !this.state.filtersOpen });
  }

  render(){
    let { program, history, location, programType } = this.props;

    return (
      <div className="program__publications row gutter-45 margin-top-lg-35">
        <div className={`program__publications__open-mobile-filter col-12 margin-top-15`}>
          <a className="button--text" onClick={this.toggleMobileFilters}>{this.state.filtersOpen ? 'Hide Filters' : 'Show Filters'}</a>
        </div>
        <div className={`col-lg-3 margin-top-5 margin-bottom-15 program__publications__filter-col${this.state.filtersOpen ? ' open' : ''}`}>
          <Fetch component={Filters} name={`${NAME}.publications`}
            endpoint={'post'}
            fetchOnMount={true}
            eager={true}
            program={program}
            history={history}
            location={location}
            initialQuery={this.initialQuery()}/>
        </div>
        <div className='col-12 col-lg-9 program__publications__list-col'>
          <Response name={`${NAME}.publications`} component={PublicationsList}/>
        </div>
      </div>
    );
  }
}
