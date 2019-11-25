import { NAME } from '../constants';
import React, { Component } from 'react';
import { Fetch, Response } from '../../components/API';
import DocumentMeta from 'react-document-meta';
import { PublicationsList, PublicationsWrapper } from '../../components/Publications';
import { FilterGroup, TypeFilter, ProgramFilter, DateFilter } from '../../components/Filters';
import titlefy from '../../../lib/utils/titlefy';

// must pass an API Component (Fetch or Response) props to Filters
class Filters extends Component {
  render(){
    let { content_types, programs, response: { params: { query } }, history, response, location} = this.props;

    return (
      <FilterGroup history={history} location={location} response={response}>
        <TypeFilter label="Type" expanded={true} types={content_types.sort((a,b) => a.name > b.name ? 1 : -1)}/>
        <ProgramFilter label="Program" expanded={query.program_id != '' && query.program_id != null} programs={programs} />
        <DateFilter label="Date" />
      </FilterGroup>
    );
  }
}

export default class Publications extends Component {
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
      story_image_rendition: 'small',
      page_size: 8,
    }

    let params = new URLSearchParams(location.search.replace('?', ''));
    if(params.get('programId'))
      initQuery.program_id = params.get('programId');
    if(params.get('after'))
      initQuery.after = params.get('after');
    if(params.get('before'))
      initQuery.before = params.get('before');
    if(params.get('dataViz'))
      initQuery.data_viz = params.get('dataViz');

    if(type) initQuery.content_type = type.api_name;

    return initQuery;
  }

  render(){
    let { program, history, location, content_types, programs, match } = this.props;

    return (
      <DocumentMeta title={titlefy(match.params.contentType)}>
        <PublicationsWrapper
            filters={
              <Fetch name={`${NAME}.publications`}
                component={Filters}
                endpoint={'post'}
                fetchOnMount={true}
                eager={true}
                programs={programs}
                content_types={content_types}
                history={history}
                location={location}
                initialQuery={this.initialQuery()}/>
            }
            publications={
              <Response name={`${NAME}.publications`} component={PublicationsList}/>
            }
        />
      </DocumentMeta>
    );
  }
}
