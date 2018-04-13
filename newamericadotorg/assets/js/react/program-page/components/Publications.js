import { NAME } from '../constants';
import { Component } from 'react';
import { Fetch, Response } from '../../components/API';
import { TypeFilter, SubprogramFilter, DateFilter, TopicFilter, CategoryFilter, FilterGroup } from '../../components/Filters';
import { PublicationsList, PublicationsWrapper } from '../../components/Publications';

const TopicFilterWrapper = ({ response: { results }, topicId, expanded, location, history }) => (
  <TopicFilter topics={results} label="Topic" topicId={topicId} expanded={expanded} location={location} history={history} />
);

// must pass an response object from Fetch of Response component, history and location to FilterGroup
const Filters = (props) => (
  <FilterGroup
    history={props.history}
    location={props.location}
    response={props.response}
    programUrl={props.program.url}>
    <TypeFilter types={props.program.content_types.sort((a,b) => a.name > b.name ? 1 : -1)} expanded={props.initialQuery.content_type !== undefined} label="Type"/>
    {props.categories &&
      <CategoryFilter categories={props.categories.sort((a,b) => a.name > b.name ? 1 : -1)} expanded={props.initialQuery.category !== undefined} label="Category"/>}
    {(props.program.subprograms && !props.categories) &&
    <SubprogramFilter subprograms={props.program.subprograms} expanded={props.response.params.query.subprogram_id!==undefined} label="Project"/>}
    {props.program.topics &&
      <Response name={`${NAME}.topics`}
        component={TopicFilterWrapper}
        program={props.program}
        history={props.history}
        location={props.location}
        topicId={props.initialQuery.topic_id}
        expanded={props.response.params.query.topic_id!==undefined}/>}
    <DateFilter label="Date" expanded={props.response.params.query.after!==undefined} />
  </FilterGroup>
);

export default class Publications extends PublicationsWrapper {
  state = {
    categories: undefined,
    initQuery: {}
  }
  componentWillMount(){
    if(window.scrollY > 400 || window.pageYOffset > 400){
      window.scrollTo(0, 0);
    }
    this.setState({ initQuery: this.initialQuery(this.props) })
  }

  componentWillReceiveProps(nextProps){
    if(JSON.stringify(nextProps.location) != JSON.stringify(this.props.location))
      this.setState({ initQuery: this.initialQuery(nextProps) })
  }

  setCategories = (cats) =>{
    this.setState({ categories: cats });
  }

  initialQuery = (props) => {
    let { programType, program, location } = props;
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
    if(params.get('topicId'))
      initQuery.topic_id = params.get('topicId');
    if(params.get('category'))
      initQuery.category = params.get('category');

    let slug = location.pathname.match(/.+\/(.+)\/$/i)[1];
    let type = program.content_types.find((t)=>(t.slug === slug ));
    if(type){
      initQuery.content_type = type.api_name;
      if(type.api_name == 'otherpost'){
        initQuery.other_content_type_title = type.title;
        if(type.categories)
          this.setState({ categories: type.categories });
      } else {
        this.setState({ categories: undefined });
      }
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
              categories={this.state.categories}
              location={location}
              initialQuery={this.state.initQuery}/>
          }
          publications={
            <Response name={`${NAME}.publications`} component={PublicationsList}/>
          }
      />
    );
  }
}
