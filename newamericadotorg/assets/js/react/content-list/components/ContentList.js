import { Component } from 'react';
import { connect } from 'react-redux';
import { Response } from '../../components/API';
import InfiniteLoadMore from '../../components/InfiniteLoadMore';
import ContentListItem from './ContentListItem';
import { NAME } from '../constants';

export const List = ({ results }) => (
  <section className='content-list container--wide'>
    {results.map((r, i)=>(
      <ContentListItem post={r} key={`content-list-item-${i}`}/>
    ))}
  </section>
);

class ContentList extends Component {

  nextPage = () => {
    let { setQueryParam, fetchAndAppend, response } = this.props;
    if(!response.hasNext) return false;

    setQueryParam('page', response.page+1);
    return fetchAndAppend;
  }

  render(){
    let { results, hasNext, isFetching } = this.props.response;
    if(!results) return null;
    return (
      <InfiniteLoadMore
        onNextPage={this.nextPage}
        hasNext={hasNext}
        isFetching={isFetching}
        data={results}
        upperBoundOffset={-(document.documentElement.clientHeight*2.5)}>
        <List results={results} />
      </InfiniteLoadMore>
    );
  }
}

const mapStateToProps = (state) => ({
  siteScrollPosition: state.site.scrollPosition // forces reevaluation on scroll
});

ContentList = connect(mapStateToProps)(ContentList)

export default () => (
  <Response name={NAME} component={ContentList} />
)
