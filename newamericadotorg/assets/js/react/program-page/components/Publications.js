import { NAME } from '../constants';
import { Component } from 'react';
import { Fetch, Response } from '../../components/API';
import { TypeFilter, SubprogramFilter, DateFilter, TopicFilter, FilterGroup } from '../../components/Publications';
import { PublicationsList } from '../../components/Publications';

// must pass an API Component (Fetch or Response) props to Filters
const Filters = (props) => (
  <FilterGroup>
    <TypeFilter types={props.program.content_types} {...props} expanded={true} label="Type"/>
    {props.program.subprograms &&
    <SubprogramFilter subprograms={props.program.subprograms} {...props} label="Project"/>}
    <DateFilter {...props} label="Date"/>
    {props.program.topics &&
    <TopicFilter {...props} topics={props.program.topics} label="Topic"/>}
  </FilterGroup>
);

export default class Publications extends Component {
  componentWillMount(){
    if(window.scrollY > 300){
      window.scrollTo(0, 0);
    }
  }

  initialQuery = () => {
    let { programType, program, location } = this.props;
    let params = new URLSearchParams(location.search.replace('?', ''));
    let slug = location.pathname.match(/.+\/(.+)\/$/i)[1];
    let type = program.content_types.find((t)=>(t.slug === slug ));

    let initQuery = {
      [programType == 'program' ? 'program_id' : 'subprogram_id']: program.id,
      image_rendition: 'max-300x240',
      content_type: type ? type.api_name : '',
      page_size: 8,
      page: 1
    }

    if(programType=='program'){
      initQuery.subprogram_id = params.get('projectId') || '';
    }

    return initQuery;
  }

  render(){
    let { program, history, location, programType } = this.props;

    return (
      <div className="program__publications row gutter-45 scroll-target margin-top-35" data-scroll-trigger-point="bottom" data-scroll-bottom-offset="65">
        <div className="col-3 program__publications__filter-col">
          <Fetch component={Filters} name={`${NAME}.publications`}
            endpoint={'post'}
            fetchOnMount={true}
            program={program}
            history={history}
            location={location}
            initialQuery={this.initialQuery()}/>
        </div>
        <div className='col-9 program__publications__list-col'>
          <Response name={`${NAME}.publications`} component={PublicationsList}/>
        </div>
      </div>
    );
  }
}
