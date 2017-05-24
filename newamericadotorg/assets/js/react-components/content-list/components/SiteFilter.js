import { Component } from 'react';
import { connect } from 'react-redux';
import { NAME } from '../constants';
import Fetch from '../../api/components/Fetch';

const Select = ({ onchange, options, valueAccessor='id', nameAccessor='name' }) => (
  <select onChange={onchange}>
    <option value="">All</option>
    {options.map((o,i)=>(
      <option key={i} value={o[valueAccessor]}>{o[nameAccessor]}</option>
    ))}
  </select>
)

// inherits action/dispatch props from Fetch
class Filter extends Component {
  setParam = (key, value) => {
    let { setParams } = this.props;
    // reset page query parameter every time
    let query = { page: 1, [key]: value }
    setParams({ query });
  }
  render() {
    let { programs, content_types } = this.props;

    return (
      <section className="container--medium content-filters">
        <div className="content-filters__filter">
          <Select
            onchange={(e)=>{ this.setParam('program_id', e.target.value); }}
            options={programs}
          />
        </div>
        <div className="content-filters__filter">
          <Select
            onchange={(e)=>{ this.setParam('content_type', e.target.value); }}
            options={content_types}
            valueAccessor="api_name"
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

// Fetch sends results to state[NAME].results
// see ContentList for render
const Container = () => (
  <Fetch
    name={NAME}
    endpoint="post"
    eager={true}
    fetchOnMount={true}
    component={Filter}
    initialQuery={{
      image_rendition: 'fill-225x125'
    }}/>
);

export default Container;
