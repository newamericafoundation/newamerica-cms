import { Component } from 'react';
import { connect } from 'react-redux';
import { NAME } from '../constants';
import Fetch from '../../api/components/Fetch';
import Heading from './Heading';

export const Select = ({ onchange, options, valueAccessor='id', nameAccessor='name', selected, allValue }) => (
  <select onChange={onchange}>
    <option value={allValue}>All</option>
    {options.map((o,i)=>(
      <option key={i} value={o[valueAccessor]} selected={o[valueAccessor]==selected}>
        {o[nameAccessor]}
      </option>
    ))}
  </select>
)

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

    return (
      <section className="container--medium content-filters">
        <Heading title={contentType.title} />
        <div className="content-filters__filter">
          <Select
            options={programs}
            selected={programId}
            allValue=""
            onchange={(e)=>{
              let val = e.target.value ? '/?program_id='+e.target.value : '/';
              history.push(match.path+val);
            }}
          />
        </div>
        <div className="content-filters__filter">
          <Select
            options={content_types}
            valueAccessor="slug"
            selected={contentType.slug}
            allValue="publications"
            onchange={(e)=>{
              history.push('/'+e.target.value+'/?'+this.getParams());
            }}
          />
        </div>
      </section>
    );
  }
}

const mapStateToProps = (state) => ({
  programs: state.programData.results || [],
  content_types: state.contentTypes.results || [],
  query: state[NAME].params ? state[NAME].params.query : {}
});

Filter = connect(mapStateToProps)(Filter);

export { Filter };
// Fetch sends results to state[NAME].results
// see ContentList for render
const Container = (props) => (
  <Fetch {...props}
    name={NAME}
    endpoint="post"
    component={Filter}
    fetchOnMount={true}
    initialQuery={{
      image_rendition: 'fill-225x125',
      program_id: props.programId || '',
      content_type: props.contentType.api_name,
      page_size: 15,
      page: 1
    }} />
);

export default Container;
