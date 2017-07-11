import { Component } from 'react';
import { Author, ContentListItem } from '../../components/Content';
import InfiniteLoadMore from '../../components/InfiniteLoadMore';
import { NAME } from '../constants';

const Result = ({ item }) => (
  <div className={`search__results__item search__${item.content_type.api_name}`}>
    <ContentListItem post={{
      ...item,
      story_image: item.image,
      story_excerpt: item.description
    }} />
  </div>
);

export default class ResultsPage extends Component {
  nextPage = () => {
    let { setQueryParam, fetchAndAppend, response } = this.props;
    if(!response.hasNext) return false;

    setQueryParam('page', response.page+1);
    return fetchAndAppend;
  }

  render() {
    let { response: { results, hasNext, isFetching }} = this.props;
    return(
      <InfiniteLoadMore
        onNextPage={this.nextPage}
        hasNext={hasNext}
        isFetching={isFetching}
        data={results}
        upperBoundOffset={-(document.documentElement.clientHeight*2.5)}>
        <div className="search__results-page content-list container--wide">
          {results && results.map((p,i)=>(
            <Result item={p.specific} />
          ))}
        </div>
      </InfiniteLoadMore>
    );
  }
}
