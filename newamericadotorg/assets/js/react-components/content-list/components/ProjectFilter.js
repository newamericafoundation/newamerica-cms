import { NAME } from '../constants';
import { Select, Filter } from './SiteFilter';
import Heading from './Heading';
import Fetch from '../../api/components/Fetch';

class ProjectFilter extends Filter {
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
          <Heading title={contentType.title} />
          <div className="content-filters__filter">
            <Select
              options={project.content_types}
              valueAccessor="slug"
              nameAccessor="title"
              selected={contentType.slug}
              allValue="publications"
              onchange={(e)=>{
                history.push('/'+project.url+'/'+e.target.value+'/?'+this.getParams());
              }}
            />
          </div>
        </div>
      )
    }
}

const Container = (props) => (
  <Fetch {...props}
    name={NAME}
    endpoint="post"
    component={ProjectFilter}
    fetchOnMount={true}
    initialQuery={{
      image_rendition: 'fill-225x125',
      content_type: props.contentType.api_name,
      project_id: props.projectId || '',
      page_size: 15,
      page: 1
    }} />
);

export default Container;
