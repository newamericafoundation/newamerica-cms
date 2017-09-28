import { NAME, PAGE_SIZE, IMAGE_RENDITION } from '../constants';
import { Component } from 'react';
import Heading from './Heading';
import { Fetch } from '../../components/API';
import Select from '../../components/Select';
import DatePicker from './DatePicker';

class Filter extends Component {
    componentWillReceiveProps(nextProps){
      let { setQuery, contentType, projectId, before, after } = this.props;

      if(
        nextProps.contentType.id !== contentType.id ||
        nextProps.projectId != projectId ||
        nextProps.before != before ||
        nextProps.after != after
      ){
        setQuery({
          content_type_id: nextProps.contentType.id || '',
          project_id: nextProps.projectId || '',
          before: nextProps.before || '',
          after: nextProps.after || '',
          page: 1
        }, true);
      }
    }

    getParams = () => {
      let { projectId, before, after } = this.props;
      let params = new URLSearchParams();

      if( projectId )
        params.set('project_id', projectId);
      if(before)
        params.set('before', before);
      if(after)
        params.set('after', after);

      return params;
    }

    render(){
      let { program, projectId, match, contentType, history, before, after } = this.props;
      let project = program.projects.find(p => p.id==projectId);

      return (
        <div className="content-list__heading-filter-wrapper">
          <Heading title={contentType.title || 'Publications'} />
          <div className="content-list__filters">
            <Select
              name="Publication Type"
              className="content-list__filters__filter publication-type"
              options={program.content_types}
              defaultOption={contentType}
              valueAccessor="slug"
              labelAccessor="title"
              onChange={(option)=>{
                let val = option ? option.slug : 'publications';
                history.push(`/${program.slug}/${val}/?${this.getParams().toString()}`);
              }}/>
            {program.projects.length > 0 &&
              <Select
              name="Projects"
              className="content-list__filters__filter program wide"
              options={program.projects}
              defaultOption={project}
              valueAccessor="id"
              labelAccessor="title"
              onChange={(option)=>{
                let params = this.getParams();
                let val = option ? params.set('project_id', option.id) : params.delete('project_id');
                history.push(match.url+'?'+params.toString());
              }}/>}
              <DatePicker
                className="content-list__filters__filter"
                startDate={after}
                endDate={before}
                onDatesChange={({startDate, endDate})=>{
                  let params = this.getParams();
                  if(startDate) params.set('after', startDate);
                  else params.delete('after');
                  if(endDate) params.set('before', endDate);
                  else params.delete('before');
                  history.push(match.url+'?'+params.toString());
                }}
              />
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
      image_rendition: IMAGE_RENDITION,
      program_id: props.programId,
      content_type_id: props.contentType.id || '',
      project_id: props.projectId || '',
      before: props.before || '',
      after: props.after || '',
      page_size: PAGE_SIZE,
      page: 1
    }} />
);
