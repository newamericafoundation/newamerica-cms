import React, { Component } from 'react';
import { Arrow } from '../../components/Icons';

export default class Subprograms extends Component {
  groupSubprograms = () => {
    let { program } = this.props;
    let subprograms = {
      Initiative: [],
      Project: []
    }

    program.subprograms.forEach((s)=>{
      subprograms[s.type || 'Initiative'].push(s);
    })

    return subprograms;

  }
  render(){
    let subprograms = this.groupSubprograms();
    return (
      <div className="initiatives-and-projects">
        <div className="initiatives margin-top-35">
          {subprograms.Project.length > 0 && <h6 className="margin-bottom-15">Initiatives</h6>}
          <div className="menu-list">
            {subprograms.Initiative.map((s,i)=>(
              <h2 key={`subprogram-${i}`}>
                <a href={s.url}>{s.title}</a>
                <Arrow direction="right" />
            </h2>
            ))}
          </div>
        </div>
        {subprograms.Project.length > 0 && <div className="projects margin-top-60">
          <h6 className="margin-bottom-15">Projects</h6>
          <div className="menu-list">
            {subprograms.Project.map((s,i)=>(
              <h2 key={`subprogram-${i}`}>
                <a href={s.url}>{s.title}</a>
                <Arrow direction="right" />
              </h2>
            ))}
          </div>
        </div>}
      </div>
    );
  }
}
