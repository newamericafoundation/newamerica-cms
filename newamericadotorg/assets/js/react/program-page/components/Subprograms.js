import { Component } from 'react';

export default class Subprograms extends Component {

  render(){
    let { program } = this.props;
    return (
      <div className="menu-list margin-top-35">
        {program.subprograms.map((s,i)=>(
          <h2 key={`subprogram-${i}`}>
            <a href={s.url}>{s.title}</a>
            <div className="icon-arrow">
              <div />
              <div />
              <div />
            </div>
        </h2>
        ))}
      </div>
    );
  }
}
