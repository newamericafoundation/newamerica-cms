import { NAME, PAGE_SIZE, IMAGE_RENDITION } from '../constants';
import { Component } from 'react';
import Heading from './Heading';
import { Fetch } from '../../components/API';
import Select from '../../components/Select';

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
      let { subprogram, subprogramId, contentType, history } = this.props;

      return (
        <div className="content-list__heading-filter-wrapper">
          <Heading title={contentType.title || 'Publications'} />
          {subprogram.content_types.length > 1 && <div className="content-list__filters">
              <Select
                name="Publication Type"
                className="content-list__filters__filter publication-type"
                valueAccessor="slug"
                labelAccessor="title"
                options={subprogram.content_types}
                defaultOption={contentType.slug}
                onChange={(option)=>{
                  console.log(option);
                  let val = option ? option.slug : 'publications';
                  history.push(subprogram.url+val+'/?'+this.getParams());
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
      image_rendition: IMAGE_RENDITION,
      content_type: props.contentType.api_name,
      subprogram_id: props.subprogramId || '',
      page_size: PAGE_SIZE,
      page: 1
    }} />
);
