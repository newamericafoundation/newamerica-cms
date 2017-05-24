import { Component } from 'react';
import { connect } from 'react-redux';
import { NAME } from '../constants';
import Fetch from '../../api/components/Fetch';

const Select = ({ onchange, options }) => (
  <select onChange={onchange}>
    {options.map((o,i)=>(
      <option value={o.api_name}>{o.name}</option>
    ))}
  </select>
)

// inherits action/dispatch props from Fetch
class Filter extends Component {
  render() {
    let { programs, content_types, setParam } = this.props;
    return (
      <section className="container--medium content-filters">
        <div className="content-filters__filter">
          <Select
            onchange={(v)=>{ setParam('program', v); }}
            options={programs}
          />
        </div>
        <div className="content-filters__filter">
          <Select
            onchange={(v)=>{ setParam('content_type', v); }}
            options={content_types}
          />
        </div>
      </section>
    );
  }
}

const mapStateToProps = (state) => ({
  programs: [],
  content_types: []
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
