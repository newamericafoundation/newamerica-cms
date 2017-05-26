import { Component } from 'react';
import { connect } from 'react-redux';
import { NAME } from '../constants';
import Fetch from '../../api/components/Fetch';
import { Redirect } from 'react-router-dom';
import Heading from './Heading';

export const Select = ({ onchange, options, valueAccessor='id', nameAccessor='name', selected, all }) => (
  <select onChange={onchange}>
    <option value={all}>All</option>
    {options.map((o,i)=>(
      <option key={i} value={o[valueAccessor]} selected={o[valueAccessor]==selected}>
        {o[nameAccessor]}
      </option>
    ))}
  </select>
)

// inherits action/dispatch setParam props from api.Fetch
class Filter extends Component {
  componentWillMount(){
    let { setParam, contentType, programId } = this.props;

    if(programId)
      setParam('program_id', programId, false);

    setParam('content_type', contentType.api_name);
  }

  componentWillReceiveProps(nextProps){
    let { setParam, contentType, programId, fetchData } = this.props;

    let shouldFetch = false;

    if(nextProps.contentType.api_name !== contentType.api_name){
      setParam('content_type', nextProps.contentType.api_name, false);
      shouldFetch = true;
    }

    if(nextProps.programId != programId){
      setParam('program_id', nextProps.programId || '', false);
      shouldFetch = true;
    }

    if(shouldFetch)
      setParam('page', 1);

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
            all=''
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
            all="publications"
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
  <Fetch
    name={NAME}
    endpoint="post"
    eager={true}
    fetchOnMount={false}
    component={Filter}
    initialQuery={{
      image_rendition: 'fill-225x125',
      page_size: 15
    }}
    {...props}
    />
);

export default Container;
