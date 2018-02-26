import { NAME } from '../constants';
import { Component } from 'react';
import { Fetch, Response } from '../../components/API';
import { TypeFilter, SubprogramFilter, DateFilter, TopicFilter, FilterGroup } from '../../components/Filters';
import { PublicationsList, PublicationsWrapper } from '../../components/Publications';

// must pass an response object from Fetch of Response component, history and location to FilterGroup
const Filters = (props) => (
  <FilterGroup
    history={props.history}
    location={props.location}
    response={props.response}
    programUrl={props.program.url}>
    <TypeFilter types={props.program.content_types.sort((a,b) => a.name > b.name ? 1 : -1)} expanded={props.initialQuery.content_type != undefined} label="Type"/>
    {props.program.subprograms &&
    <SubprogramFilter subprograms={props.program.subprograms} expanded={props.response.params.query.subprogram_id!==undefined} label="Project"/>}
    <DateFilter label="Date" expanded={props.response.params.query.after!==undefined} />
    {props.program.topics &&
    <TopicFilter topics={props.program.topics} label="Topic" expanded={props.response.params.query.topic_id!==undefined}/>}
  </FilterGroup>
);

export default class Publications extends PublicationsWrapper {
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
    if(params.get('after'))
      initQuery.after = params.get('after');
    if(params.get('before'))
      initQuery.before = params.get('before');

    let slug = location.pathname.match(/.+\/(.+)\/$/i)[1];
    let type = program.content_types.find((t)=>(t.slug === slug ));
    if(type){
      initQuery.content_type = type.api_name;
      if(type.api_name == 'otherpost')
        initQuery.other_content_type_title = type.title;
    }

    return initQuery;
  }

  render(){
    let { program, history, location, programType } = this.props;

    return (
      <PublicationsWrapper
          filters={
            <Fetch name={`${NAME}.publications`}
              component={Filters}
              endpoint={'post'}
              fetchOnMount={true}
              eager={true}
              program={program}
              history={history}
              location={location}
              initialQuery={this.initialQuery()}/>
          }
          publications={
            <Response name={`${NAME}.publications`} component={PublicationsList}/>
          }
      />
    );
  }
}
