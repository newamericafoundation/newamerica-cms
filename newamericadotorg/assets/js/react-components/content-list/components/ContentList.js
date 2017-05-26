import { Component } from 'react';
import { connect } from 'react-redux';
import { NAME } from '../constants';
import ContentListItem from './ContentListItem';
import { LazyLoadImages } from '../../lazyload';
import Loading from '../../loading';
import { setParam, fetchAndAppend } from '../../api/actions';

const LoadMore = ({ onclick }) => (
  <div className="content-list__load-more">
    <a className="button transparent" onClick={onclick}>Load More</a>
  </div>
);

const LoadingIcon = () => (
  <div className="content-list__loading-icon-wrapper">
    <Loading />
  </div>
);

const NoResults = () => (
  <div className="content-list__no-results">
    <label className="active lg">No results found</label>
  </div>
);

const List = ({ results }) => (
  <LazyLoadImages>
    {results.map((r, i)=>(
      <ContentListItem post={r} key={`content-list-item-${i}`}/>
    ))}
  </LazyLoadImages>
);

class ContentList extends Component {
  el = null;
  isInfinite = false;
  /**
    dispatched isFetching prop doesn't update quickly enough for onscroll events.
    as in the next scroll tick happens before isFetching is updated.
    add isLoading flag that's updated in the right order in the call stack
  **/
  isLoading = false;
  shouldComponentUpdate(nextProps) {
    let { hasNext, results, params, isFetching } = this.props;
    /**
      since we're subscribing to scrollPosition,
      this component gets reevaluated with each tick (/rerendered on each tick)
      this causes sluggish scrolling when the results array gets large.
      here we check the results and only rerender if we have new data.
    **/
    if(this.isInfinite && hasNext && !this.isLoading)
      this.nextPageOnEnd();

    if(results[0] && nextProps.results[0]){
      // TODO better check for new data
      if(results[0].id !== nextProps.results[0].id){
        this.isInfinite = false;
        return true;
      }
    }

    if(isFetching !== nextProps.isFetching) return true;

    return results.length !== nextProps.results.length;
  }

  nextPage = () => {
    let { page, hasNext, setParam, fetchAndAppend } = this.props;
    if(hasNext && !this.isLoading){
      this.isLoading = true;
      setParam('page', page+1);
      fetchAndAppend(()=>{ this.isLoading = false; });
    }
  }

  loadMore = () => {
    this.isInfinite = true;
    this.nextPage();
  }

  nextPageOnEnd = () => {
    if(!this.el) return;

    let distanceFromTop = -this.el.getBoundingClientRect().top;
    let bottom = this.el.offsetHeight;
    let end = bottom - (document.documentElement.clientHeight*2.5);
    let limit = bottom + 50;

    if(distanceFromTop>end && distanceFromTop<limit)
      this.nextPage();

  }

  render(){
    let { results, hasNext, isFetching } = this.props;
    let classes = `${this.isInfinite ? 'is-infinite' : ''} ${this.isLoading ? 'is-loading' : '' } ${isFetching ? 'is-fetching' : ''}`;

    return (
      <section
        ref={(el) => { this.el = el; }}
        className={`content-list container ${classes}`}>

        <List results={results} />

        {(hasNext && !this.isInfinite) &&
          <LoadMore onclick={this.loadMore}/>

        }{(results.length===0 && !isFetching) &&
          <NoResults />

        }{isFetching &&
          <LoadingIcon />

        }
      </section>
    );
  }
}

const mapStateToProps = (state) => ({
  params: state[NAME].params || {},
  results: state[NAME].results || [],
  hasNext: state[NAME].hasNext || false,
  hasPrevious: state[NAME].hasPrevious || false,
  page: state[NAME].page || 1,
  isFetching: state[NAME].isFetching || false,
  siteScrollPosition: state.site.scrollPosition // forces reevaluation on scroll
});

const mapDispatchToProps = (dispatch) => ({
  setParam: (key, value) => {
    dispatch(setParam(NAME, {key, value}));
  },
  fetchAndAppend: (callback) => {
    dispatch(fetchAndAppend(NAME, callback));
  }
});

export default connect(mapStateToProps, mapDispatchToProps)(ContentList);
