import { NAME } from '../constants';
import React, { Component } from 'react';
import { Fetch } from '../../components/API';
import { Person, PersonsList } from '../../components/People'
import Image from '../../components/Image';
import groupBy from '../../../lib/utils/group-by';
import Separator from '../../components/Separator';
import InfiniteLoadMore from '../../components/InfiniteLoadMore';
import { LoadingDots } from '../../components/Icons';

const StaffGroup = ({ groupName, group}) => (
  <div className="program__people__fellows__list margin-top-35">
    <Separator text={`${groupName}`}/>
    <PersonsList people={group} response={{ results: [] }} className="margin-top-15"/>
  </div>
)

class Fellows extends Component {
  state = {
    sortOrder: {
      'Current Fellows': '2',
      'Returning Fellows': '1',
      'Former Fellows': '0'
    }
  }
  render(){
    let fellowsGroups = groupBy(this.props.response.results, 'group');
    let { sortOrder } = this.state;
    let keys = Object.keys(fellowsGroups).sort((a,b) => (sortOrder[a] || a) > (sortOrder[b] || b) ? -1 : 1);
    if(this.props.response.isFetching) return ( <LoadingDots/> );
    return (
      <div className="program__people__fellows">
        {keys.map((k,i)=>(
          <StaffGroup groupName={k} group={fellowsGroups[k]} key={i} />
        ))}
      </div>
    );
  }
}

class InfiniteFellowsList extends Component {
  nextPage = () => {
    let { setQuery, fetchAndAppend, response } = this.props;
    if(!response.hasNext) return false;

    setQuery(response.nextParams);
    return fetchAndAppend;
  }

  render(){
    let { results, hasNext, isFetching, page } = this.props.response;
    return (
      <InfiniteLoadMore
        onNextPage={this.nextPage}
				response={this.props.response}
        infiniteOnMount={true}
        bottomOffset={-document.documentElement.clientHeight*0.75}>
        <Fellows response={this.props.response} />
      </InfiniteLoadMore>
    );
  }
}

class StaffList extends Component {
  state = {
    sortOrder: {
      'Staff': 1,
      'Contributing Staff': 2,
      'Advisors': 3,
      'Current Fellows': 4,
      'Returning Fellows': 5
    }
  }
  render(){
    let { response, loading } = this.props;
    let { sortOrder } = this.state;
    let staffGroups = groupBy(response.results, 'group');
    let keys = Object.keys(staffGroups).sort((a,b) => sortOrder[a] - sortOrder[b]);

    return (
      <div className={`program__people__staff margin-top-35`}>
        {loading &&
          <div className="margin-top-60 margin-bottom-80" style={{ paddingBottom: '110px'}}>
            <LoadingDots />
          </div>}
        {response.results.length > 0 && keys.map((k,i)=>(
          <StaffGroup groupName={k} group={staffGroups[k]} key={i} />
        ))}{(response.results.length === 0 && !loading) && <h4 className="centered margin-top-60">None.</h4> }
      </div>
    );
  }
}


export default class People extends Component {
  state = {
    showAllFellows: false
  }

  showAllFellows = () => {
    this.setState({ showAllFellows: true });
  }

  render(){
    let { program, programType } = this.props;
    return (
      <div className="program__people">
        <Fetch name={`${NAME}.people`}
          endpoint="author"
          component={StaffList}
          loadingState={<StaffList response={{ results: [] }} loading={true}/>}
          fetchOnMount={true}
          initialQuery={{
            [programType == 'program' ? 'program_id' : 'subprogram_id']: program.id,
            page_size: 300,
            include_fellows: true
          }}/>
          {(!this.state.showAllFellows && (program.slug == 'fellows' || program.slug == 'ca')) &&
            <div className="program__publications-list-load-more margin-top-10">
              <a className={`button`} onClick={this.showAllFellows}>
                <span className="load-more-label">Former Fellows</span>
              </a>
            </div>
          }{this.state.showAllFellows &&
            <Fetch name={`${NAME}.allFellow`}
              endpoint="fellow"
              component={Fellows}
              fetchOnMount={true}
              initialQuery={{
                [programType == 'program' ? 'program_id' : 'subprogram_id']: program.id,
                page_size: 25,
                former: true
              }}/>
          }
      </div>
    );
  }
}
