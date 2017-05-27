import { NAME } from '../constants';
import { Select, Filter } from './SiteFilter';
import Heading from './Heading';
import Fetch from '../../api/components/Fetch';

class ProgramFilter extends Filter {
    componentWillReceiveProps(nextProps){
      let { setQuery, contentType, projectId, fetchData } = this.props;

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
      let { programId, program, match, contentType, projectId, history } = this.props;

      return (
        <div className="content-filters__filters-wrapper">
          <Heading title={contentType.title} />
          <div className="content-filters__filter">
            <Select
              options={program.content_types}
              valueAccessor="slug"
              nameAccessor="title"
              selected={contentType.slug}
              allValue="publications"
              onchange={(e)=>{
                history.push('/'+program.slug+'/'+e.target.value+'/?'+this.getParams());
              }}
            />
          </div>
          <div className="content-filters__filter">
            <Select
              options={program.projects}
              selected={projectId}
              allValue=""
              onchange={(e)=>{
                let val = e.target.value ? '?project_id='+e.target.value : '';
                history.push(match.path+val);
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
    component={ProgramFilter}
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

export default Container;
