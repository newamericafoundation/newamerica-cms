import { Component } from 'react';
import { connect } from 'react-redux';
import { NAME, PAGE_SIZE, IMAGE_RENDITION } from '../constants';
import { Fetch } from '../../components/API';
import Heading from './Heading';
import Select from '../../components/Select';
import DatePicker from './DatePicker';

// inherits action/dispatch setQuery prop from api.Fetch
class Filter extends Component {
  componentWillReceiveProps(nextProps){
    let { setQuery, contentType, programId, before, after } = this.props;

    if(
      nextProps.programId !== programId ||
      nextProps.contentType.api_name !== contentType.api_name ||
      nextProps.before !== before ||
      nextProps.after !== after
    ){
      setQuery({
        program_id: nextProps.programId || '',
        content_type: nextProps.contentType.api_name,
        before: nextProps.before || '',
        after: nextProps.after || '',
        page: 1
      }, true);
    }
  }

  getParams = () => {
    let { programId, before, after } = this.props;
    let params = new URLSearchParams();

    if( programId )
      params.set('program_id', programId);
    if(before)
      params.set('before', before);
    if(after)
      params.set('after', after);

    return params;
  }

  render() {
    let { programs, content_types, contentType, history, match, programId, before, after } = this.props;
    let program = programs.find(p =>(p.id==programId));

    return (
      <section className="">
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
              let params = this.getParams();
              let val = option ? params.set('program_id', option.id) : params.delete('program_id');
              history.push(match.path+'/?'+params.toString());
            }}/>
            <DatePicker
              startDate={after}
              endDate={before}
              onDatesChange={({startDate, endDate})=>{
                let params = this.getParams();
                if(startDate) params.set('after', startDate);
                else params.delete('after')
                if(endDate) params.set('before', endDate);
                else params.delete('before');
                history.push(match.url+'?'+params.toString());
              }}
            />
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
      before: props.before || '',
      after: props.after || '',
      page: 1
    }} />
);
