import { Component } from 'react';
import { connect } from 'react-redux';
import { Response } from '../../components/API';
import Author from '../../components/Author';
import InfiniteLoadMore from '../../components/InfiniteLoadMore';
import { NAME } from '../constants';

const List = ({ people }) => (
	<div className="row">
		{people.map((p,i)=>(
			<div className="our-people__list__item col-sm-12 col-md-3">
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
        upperBoundOffset={-(document.documentElement.clientHeight*1.5)}>
        <section className='our-people__list container--wide'>
					<List people={results} />
        </section>
      </InfiniteLoadMore>
    );
  }
}

export default () => (
  <Response name={NAME} component={PeopleList} />
)
