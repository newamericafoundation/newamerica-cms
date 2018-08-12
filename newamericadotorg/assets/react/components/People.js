import Image from './Image';
import React, { Component } from 'react';
import { Person } from './ContentCards';

export class PersonsList extends Component {
  render(){
    let { response : { results, isFetching }, children, people, className } = this.props;
    let ppl = people || results;
    if(isFetching && !people) return null;
    return (
      <div className={`program__people__list row gutter-10 ${className||''}`}>
        {ppl.length > 0 && children}
        {ppl.map((person, i) => (
          <div key={`person-${i}`} className="col-lg-4 col-md-6 col-12">
            <Person person={person} />
          </div>
        ))}
      </div>
    );
  }
}
