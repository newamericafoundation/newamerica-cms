import Image from './Image';
import { Component } from 'react';

export class PersonsList extends Component {
  render(){
    let { response : { results, isFetching }, children } = this.props;
    if(results.length===0) return null;
    return (
      <div className="program__people__list row gutter-10">
        {children}
        {results.map((person, i) => (
          <div key={`person-${i}`} className="col-md-4 col-12">
            <Person person={person} />
          </div>
        ))}
      </div>
    );
  }
}
