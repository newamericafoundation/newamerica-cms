import { Component } from 'react';
import { connect } from 'react-redux';
import Response from '../../api/components/Response';
import Author from '../../author/components/Author';
import {InfiniteLoadMore} from '../../loading';
import { NAME } from '../constants';
import { LazyLoadImages } from '../../lazyload';

const List = ({ people, className }) => (
	<div className={"row person-grid__content "+ className}>
		{people.map((p,i)=>(
			<div className="col-sm-12 col-md-3">
        <Author author={p} classes="card" />
			</div>
		))}
	</div>
);

class PeopleList extends Component {

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
        infiniteOnMount={true}
        upperBoundOffset={-(document.documentElement.clientHeight*2.5)}>
        <section className='people-list container--wide'>
          <LazyLoadImages component={List} people={results} />
        </section>
      </InfiniteLoadMore>
    );
  }
}

export default () => (
  <Response name={NAME} component={PeopleList} />
)
