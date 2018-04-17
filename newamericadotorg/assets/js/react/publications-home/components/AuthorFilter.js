import { Component } from 'react';
import { connect } from 'react-redux';
import { NAME, PAGE_SIZE, IMAGE_RENDITION } from '../constants';
import { Fetch } from '../../components/API';
import Heading from './Heading';
import Select from '../../components/Select';

// inherits action/dispatch setQuery prop from api.Fetch
class Filter extends Component {
  componentWillReceiveProps(nextProps){
    let { setQuery, contentTypeAPIName } = this.props;

    if(
      nextProps.contentTypeAPIName!== contentTypeAPIName
    ){
      setQuery({
        content_type: nextProps.contentTypeAPIName || '',
        page: 1
      }, true);
    }
  }

  getParams = () => {
    let { contentTypeAPIName } = this.props;
    let params = new URLSearchParams();

    if( programId )
      params.append('content_type', contentTypeAPIName);

    return params.toString();
  }

  render() {
    let { match, content_types, contentTypeAPIName, history } = this.props;
    let contentType = content_types.find(c =>(c.api_name==contentTypeAPIName));

    return (
      <section className="content-list__heading-filter-wrapper">
        <div className="content-list__filters">
          <Select
            name="Publication Type"
            className="content-list__filters__filter publication-type"
            options={content_types}
            defaultOption={contentType}
            valueAccessor="api_name"
            labelAccessor="title"
            onChange={(option)=>{
              let val = option ? `/?publication_type=${option.api_name}` : '/'
              history.push('/our-people/'+match.params.authorSlug+val);
            }}/>
        </div>
      </section>
    );
  }
}

const mapStateToProps = (state) => ({
  content_types: state.contentTypes.results || []
});

Filter = connect(mapStateToProps)(Filter);

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
      author_slug: props.match.params.authorSlug,
      content_type: props.contentTypeAPIName || '',
      page_size: PAGE_SIZE,
      page: 1
    }} />
);
