import { Component } from 'react';
import { connect } from 'react-redux';
import { NAME } from '../constants';
import ContentListItem from './ContentListItem';
import { LazyLoadImages } from '../../lazyload';
import { setParam, fetchAndAppend } from '../../api/actions';

const LoadMore = ({ onclick }) => (
  <div className="content-list__load-more">
    <a className="button transparent" onClick={onclick}>Load More</a>
  </div>
);

class ContentList extends Component {
  el = null;
  isLoading = false;
  isInfinite = false;

  shouldComponentUpdate(nextProps) {
    let { hasNext, results, params } = this.props;
    /**
      since we're subscribing to scrollPosition,
      this component gets reevaluated with each tick (/rerendered on each tick)
      this causes sluggish scrolling when the results array gets large.
      here we check the results and only rerender if we have new data.
    **/
    if((this.isInfinite && hasNext) && !this.isLoading)
      this.nextPageOnEnd();

    if(results[0] && nextProps.results[0]){
      if(results[0].id !== nextProps.results[0].id){
        this.isLoading = false;
        this.isInfinite = false;
        return true;
      }
    }

    return results.length !== nextProps.results.length;
  }

  nextPage = () => {
    let { page, hasNext, setParam, fetchAndAppend } = this.props;
    if(hasNext){
      this.isLoading = true;
      setParam('page', page+1);
      fetchAndAppend(()=>{ this.isLoading = false; });
    }
  }

  nextPageOnEnd = () => {
    if(!this.el) return;

    let distanceFromTop = -this.el.getBoundingClientRect().top;
    let bottom = this.el.offsetHeight;
    let end = bottom - (document.documentElement.clientHeight*2);
    if(distanceFromTop>end)
      this.nextPage();
  }

  render(){
    let { results, hasNext } = this.props;

    return (
      <section className='content-list container' ref={(el) => { this.el = el; }}>
        <LazyLoadImages>
        {results.map((r, i)=>(
          <ContentListItem post={r} key={`content-list-item-${i}`}/>
        ))}
        </LazyLoadImages>
        {(hasNext && !this.isInfinite) &&
          <LoadMore onclick={()=>{
            this.isInfinite = true;
            this.nextPage();
          }}/>
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
