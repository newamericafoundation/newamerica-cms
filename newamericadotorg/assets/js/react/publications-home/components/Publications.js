import { NAME } from '../constants';
import { Component } from 'react';
import { Fetch, Response } from '../../components/API';
import { PublicationsList } from '../../components/Publications';
import { FilterGroup, TypeFilter, ProgramFilter, DateFilter } from '../../components/Publications';

// must pass an API Component (Fetch or Response) props to Filters
class Filters extends Component {
  render(){
    let { content_types, programs, response: { params: { query } }, history, response, location} = this.props;

    return (
      <FilterGroup history={history} location={location} response={response}>
        <TypeFilter key="typefilter" label="Type" expanded={true} types={content_types.sort((a,b) => a.name > b.name)}/>
        <ProgramFilter key="programfilter" label="Program" expanded={query.program_id != '' && query.program_id != null} programs={programs} />
        <DateFilter key="datefilter" label="Date" />
      </FilterGroup>
    );
  }
}

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
    let { location, content_types } = this.props;

    let slug = location.pathname.match(/^\/(.+)\/$/i)[1];
    let type = content_types.find((t)=>(t.slug === slug ));

    let initQuery = {
      image_rendition: 'max-300x240',
      page_size: 8,
      page: 1
    }

    let params = new URLSearchParams(location.search.replace('?', ''));
    if(params.get('programId'))
      initQuery.program_id = params.get('programId');

    if(type) initQuery.content_type = type.api_name;

    return initQuery;
  }

  toggleMobileFilters = () => {
    this.setState({ filtersOpen: !this.state.filtersOpen });
  }

  render(){
    let { program, history, location, content_types, programs } = this.props;

    return (
      <div className={`program__publications row gutter-45 margin-top-lg-35`}>
        <div className="program__publications__open-mobile-filter col-12 margin-top-15">
          <a className="button--text" onClick={this.toggleMobileFilters}>{this.state.filtersOpen ? 'Hide Filters' : 'Show Filters'}</a>
        </div>
        <div className={`col-lg-3 margin-top-5 margin-bottom-15 program__publications__filter-col${this.state.filtersOpen ? ' open' : ''}`}>
          <Fetch component={Filters} name={`${NAME}.publications`}
            endpoint={'post'}
            fetchOnMount={true}
            eager={true}
            programs={programs}
            content_types={content_types}
            history={history}
            location={location}
            initialQuery={this.initialQuery()}/>
        </div>
        <div className='col-lg-9 program__publications__list-col'>
          <Response name={`${NAME}.publications`} component={PublicationsList}/>
        </div>
      </div>
    );
  }
}
