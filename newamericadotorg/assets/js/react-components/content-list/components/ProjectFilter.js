import { NAME } from '../constants';
import { Select, Filter } from './SiteFilter';
import Fetch from '../../api/components/Fetch';

class ProjectFilter extends Filter {
    componentWillMount(){
      let { setParam, contentType, programId, projectId, setFetchingStatus } = this.props;
      setParam('program_id', programId, false);
      setParam('project_id', projectId || '', false);
      setParam('content_type', contentType.api_name);
    }

    componentWillReceiveProps(nextProps){
      let { setParam, contentType, projectId, fetchData } = this.props;

      let shouldFetch = false;

      if(nextProps.contentType.api_name !== contentType.api_name){
        setParam('content_type', nextProps.contentType.api_name, false);
        shouldFetch = true;
      }

      if(nextProps.projectId != projectId){
        setParam('project_id', nextProps.projectId || '', false);
        shouldFetch = true;
      }

      if(shouldFetch) setParam('page', 1);
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
          <div className="content-filters__filter">
            <Select
              options={program.content_types}
              valueAccessor="slug"
              nameAccessor="title"
              selected={contentType.slug}
              all="publications"
              onchange={(e)=>{
                history.push('/'+program.slug+'/'+e.target.value+'/?'+this.getParams());
              }}
            />
          </div>
          <div className="content-filters__filter">
            <Select
              options={program.projects}
              selected={projectId}
              all=""
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
  <Fetch
    name={NAME}
    endpoint="post"
    eager={true}
    fetchOnMount={false}
    component={ProjectFilter}
    initialQuery={{
      image_rendition: 'fill-225x125',
      page_size: 15
    }}
    {...props}
    />
);

export default Container;
