import { NAME } from '../constants';
import { Component } from 'react';
import Heading from './Heading';
import { Fetch } from '../../components/API';
import Select from '../../components/Select';

class Filter extends Component {
    componentWillReceiveProps(nextProps){
      let { setQuery, contentType, projectId } = this.props;

      if(
        nextProps.contentType.api_name !== contentType.api_name ||
        nextProps.projectId != projectId
      ){
        setQuery({
          content_type: nextProps.contentType.api_name,
          project_id: nextProps.projectId || '',
          page: 1
        }, true);
      }
    }

    getParams = () => {
      let { projectId } = this.props;
      let params = new URLSearchParams();

      if( projectId )
        params.append('project_id', projectId);

      return params.toString();
    }

    render(){
      let { program, projectId, match, contentType, history } = this.props;
      let project = program.projects.find(p => p.id==projectId);

      return (
        <div className="content-filters__filters-wrapper">
          <Heading title={contentType.title || 'Publications'} />
          <div className="content-filters">
            <Select
              name="Publication Type"
              className="content-filters__filter publication-type"
              options={program.content_types}
              defaultOption={contentType}
              valueAccessor="slug"
              labelAccessor="title"
              onChange={(option)=>{
                let val = option ? option.slug : 'publications';
                history.push('/'+program.slug+'/'+val+'/?'+this.getParams());
              }}/>
            {program.projects.length > 0 &&
              <Select
              name="Projects"
              className="content-filters__filter program wide"
              options={program.projects}
              defaultOption={project}
              valueAccessor="id"
              labelAccessor="title"
              onChange={(option)=>{
                let val = option ? '?project_id='+option.id : '';
                history.push(match.path+val);
              }}/>}
          </div>
        </div>
      )
    }
}

export default (props) => (
  <Fetch {...props}
    name={NAME}
    endpoint="post"
    component={Filter}
    fetchOnMount={true}
    initialQuery={{
      image_rendition: 'fill-225x125',
      program_id: props.programId,
      content_type: props.contentType.api_name,
      project_id: props.projectId || '',
      page_size: 15,
      page: 1
    }} />
);
