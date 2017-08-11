import { Component } from 'react';
import { connect } from 'react-redux';
import { Response } from '../../components/API';
import InfiniteLoadMore from '../../components/InfiniteLoadMore';
import ContentListItem from './ContentListItem';
import { NAME } from '../constants';

export const List = ({ items }) => (
  <div className='content-list__results container--wide'>
    {items.map((r, i)=>(
      <ContentListItem post={r} key={`content-list-item-${i}`}/>
    ))}
  </div>
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
        className='content-list__results container--medium'
        onNextPage={this.nextPage}
        response={this.props.response}
        promptToLoadMore={true}
        upperBoundOffset={-(document.documentElement.clientHeight*2.5)}>
        {results.map((r, i)=>(
          <ContentListItem post={r} key={`content-list-item-${i}`}/>
        ))}
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
