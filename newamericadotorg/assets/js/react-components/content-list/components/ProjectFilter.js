import { NAME } from '../constants';
import { Component } from 'react';
import Heading from './Heading';
import Fetch from '../../api/components/Fetch';
import Select from '../../Select';

class Filter extends Component {
    componentWillReceiveProps(nextProps){
      let { setQuery, contentType } = this.props;

      if(
        nextProps.contentType.api_name !== contentType.api_name
      ){
        setQuery({
          content_type: nextProps.contentType.api_name,
          page: 1
        }, true);
      }
    }

    getParams = () => {
      let params = new URLSearchParams();
      return params.toString();
    }

    render(){
      let { project, projectId, contentType, history } = this.props;

      return (
        <div className="content-filters__filters-wrapper">
          <Heading title={contentType.title || 'Publications'} />
          {project.content_types.length > 1 && <div className="content-filters">
              <Select
                name="Publication Type"
                className="content-filters__filter publication-type"
                valueAccessor="slug"
                labelAccessor="title"
                options={project.content_types}
                defaultOption={contentType.slug}
                onChange={(option)=>{
                  let val = option ? option.slug : 'publications';
                  history.push('/'+project.url+'/'+val+'/?'+this.getParams());
                }}
              />
            </div>}
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
      content_type: props.contentType.api_name,
      project_id: props.projectId || '',
      page_size: 15,
      page: 1
    }} />
);
