import { Component } from 'react';
import { connect } from 'react-redux';
import { NAME, PAGE_SIZE, IMAGE_RENDITION } from '../constants';
import { Fetch } from '../../components/API';
import Heading from './Heading';
import Select from '../../components/Select';

// inherits action/dispatch setQuery prop from api.Fetch
class Filter extends Component {
  componentWillReceiveProps(nextProps){
    let { setQuery, contentType, programId } = this.props;

    if(
      nextProps.programId !== programId ||
      nextProps.contentType.api_name !== contentType.api_name
    ){
      setQuery({
        program_id: nextProps.programId || '',
        content_type: nextProps.contentType.api_name,
        page: 1
      }, true);
    }
  }

  getParams = () => {
    let { programId } = this.props;
    let params = new URLSearchParams();

    if( programId )
      params.append('program_id', programId);

    return params.toString();
  }

  render() {
    let { programs, content_types, contentType, history, match, programId } = this.props;
    let program = programs.find(p =>(p.id==programId));

    return (
      <section className="container--medium content-filters">
        <Heading title={contentType.title || 'Publications'} />
        <div className="content-filters">
          <Select
            name="Publication Type"
            className="content-filters__filter publication-type"
            options={content_types}
            valueAccessor="slug"
            labelAccessor="title"
            defaultOption={contentType}
            onChange={(option)=>{
              let val = option ? option.slug : 'publications'
              history.push('/'+val+'/?'+this.getParams());
            }}/>
          <Select
            options={programs}
            defaultOption={program}
            className="content-filters__filter program wide"
            name="Program"
            valueAccessor='id'
            labelAccessor='title'
            onChange={(option)=>{
              let val = option ? '/?program_id='+option.id : '/';
              history.push(match.path+val);
            }}/>
        </div>
      </section>
    );
  }
}

const mapStateToProps = (state) => ({
  programs: state.programData.results || [],
  content_types: state.contentTypes.results || []
});

Filter = connect(mapStateToProps)(Filter);

export { Filter };
// Fetch sends results to state[NAME].results
// see ContentList for render
export default (props) => (
  <Fetch {...props}
    name={NAME}
    endpoint="post"
    component={Filter}
    fetchOnMount={true}
    initialQuery={{
      image_rendition: IMAGE_RENDITION,
      program_id: props.programId || '',
      content_type: props.contentType.api_name,
      page_size: PAGE_SIZE,
      page: 1
    }} />
);
