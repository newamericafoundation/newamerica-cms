import { Component } from 'react';

export default class Subprograms extends Component {

  render(){
    let { program } = this.props;
    return (
      <div className="">
        {program.subprograms.map((s,i)=>(
          <h2 className="margin-25"><a href={s.url}>{s.title}</a></h2>
        ))}
      </div>
    );
  }
}
