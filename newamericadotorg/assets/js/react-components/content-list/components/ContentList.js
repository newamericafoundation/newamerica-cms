import { Component } from 'react';
import { connect } from 'react-redux';
import { NAME } from '../constants';
import ContentListItem from './ContentListItem';
import { LazyLoadImages } from '../../../utils/lazyload';
import { setParam, fetchAndAppend } from '../../api/actions';

const LoadMore = ({ onclick }) => (
  <div className="content-list__load-more">
    <a className="button transparent" onClick={onclick}>Load More</a>
  </div>
);

class ContentList extends Component {
  nextPage = () => {
    let { page, hasNext, setParam, fetchAndAppend } = this.props;

    if(hasNext){
      setParam('page', page+1);
      fetchAndAppend();
    }

  }

  render(){
    let { results } = this.props;
    return (
      <section className='content-list container'>
        <LazyLoadImages>
        {results.map((r, i)=>(
          <ContentListItem post={r} key={`content-list-item-${i}`}/>
        ))}
        </LazyLoadImages>
        <LoadMore onclick={this.nextPage}/>
      </section>
    );
  }
}

const mapStateToProps = (state) => ({
  results: state[NAME].results || [],
  hasNext: state[NAME].hasNext || false,
  hasPrevious: state[NAME].hasPrevious || false,
  page: state[NAME].page || 1
});

const mapDispatchToProps = (dispatch) => ({
  setParam: (key, value) => {
    dispatch(setParam(NAME, {key, value}));
  },
  fetchAndAppend: () => {
    dispatch(fetchAndAppend(NAME));
  }
});

export default connect(mapStateToProps, mapDispatchToProps)(ContentList);
