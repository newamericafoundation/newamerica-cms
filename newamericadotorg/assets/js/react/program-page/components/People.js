import { NAME } from '../constants';
import { Component } from 'react';
import { Fetch } from '../../components/API';
import { Person, PersonsList } from '../../components/People'
import Image from '../../components/Image';
import groupBy from '../../../utils/group-by';
import Separator from '../../components/Separator';
import InfiniteLoadMore from '../../components/InfiniteLoadMore';
import { LoadingDots } from '../../components/Icons';

class Fellows extends Component {
  groupFellows = () => {
    return groupBy(this.props.response.results, 'fellowship_year');
  }

  fellows = () => {
    let { response } = this.props;
    let fellowGroups = this.groupFellows();
    let components = []
    let i = 0;
    for(let k in fellowGroups){
      let y = new Date().getFullYear();
      let year = k === 'null' ? (fellowGroups[k][0].former ? 'Former ' : 'Related ') : (y == k ? 'Current ' : k + ' ');
      components.push(
        <div className="program__people__fellows__list margin-top-35" key={`fellows-${i}`} >
          <Separator text={`${year}Fellows`}/>
          <PersonsList people={fellowGroups[k]} response={response} className="margin-top-15"/>
        </div>
      );
      i++;
    }

    return components;
  }

  render(){
    if(this.props.response.isFetching) return ( <LoadingDots/> );
    return (
      <div className="program__people__fellows">
        {this.fellows()}
      </div>
    );
  }
}

class InfiniteFellowsList extends Component {
  nextPage = () => {
    let { setQueryParam, fetchAndAppend, response } = this.props;
    if(!response.hasNext) return false;

    setQueryParam('page', response.page+1);
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
  render(){
    if(!this.props.response.results.length > 0) return null;
    return (
      <div className="program__people__staff margin-top-35">
        <Separator text="Staff" />
        <PersonsList response={this.props.response} className="margin-top-15" />
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
          fetchOnMount={true}
          initialQuery={{
            [programType == 'program' ? 'program_id' : 'subprogram_id']: program.id,
            page_size: 100
          }}/>
          <Fetch name={`${NAME}.fellow`}
            endpoint="fellow"
            component={Fellows}
            fetchOnMount={true}
            initialQuery={{
              [programType == 'program' ? 'program_id' : 'subprogram_id']: program.id,
              page_size: 250,
              former: false
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
