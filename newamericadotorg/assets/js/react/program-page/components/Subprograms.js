import { Component } from 'react';
import { Arrow } from '../../components/Icons';

export default class Subprograms extends Component {

  render(){
    let { program } = this.props;
    return (
      <div className="menu-list margin-top-35">
        {program.subprograms.map((s,i)=>(
          <h2 key={`subprogram-${i}`}>
            <a href={s.url}>{s.title}</a>
            <Arrow direction="right" />
        </h2>
        ))}
      </div>
    );
  }
}
