import { Component } from 'react';
import { connect } from 'react-redux';
import getNestedState from '../../../utils/get-nested-state';
import { NAME } from '../constants';
import { Fetch } from '../../components/API';
import Select from '../../components/Select';

// inherits action/dispatch setQuery prop from api.Fetch
class Filter extends Component {
  render() {
    let { content_types, response: { results } } = this.props;
    if(results.length===0) return null;
    return (
      <section className="container--medium content-filters">
        <h2 className="centered">Related Content</h2>
        <div className="content-filters">
          <Select
            name="Publication Type"
            className="content-filters__filter publication-type"
            options={content_types}
            valueAccessor="api_name"
            labelAccessor="title"
            onChange={(option)=>{
              let val = option ? option.api_name : '';
              this.props.setQueryParam('content_type', val, true);
            }}/>
        </div>
      </section>
    );
  }
}

const mapStateToProps = (state) => ({
  content_types: getNestedState(state, 'contentTypes.results')
});

Filter = connect(mapStateToProps)(Filter);

export default (props) => (
  <Fetch {...props}
    name={NAME + '.content'}
    endpoint="post"
    component={Filter}
    fetchOnMount={true}
    initialQuery={{
      image_rendition: 'min-650x200',
      topic_id: props.topicId,
      page_size: 10,
      page: 1
    }} />
);
